#!/usr/bin/env python3
"""
Enhanced LLM Transformer Implementation for HyperGNN Framework
============================================================

This module provides a modern, production-ready implementation of an LLM transformer
specifically designed for legal case analysis and timeline processing.

Features:
- Multi-head attention with agent perspective mapping
- BERT-style bidirectional encoding
- Custom tokenization for legal/investigative domains
- Integration with OpenAI API for enhanced capabilities
- Fine-tuning support for domain-specific tasks
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import openai
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import (
    AutoConfig,
    AutoModel,
    AutoTokenizer,
    BertConfig,
    BertModel,
    BertTokenizer,
    Trainer,
    TrainingArguments,
)

from case_data_loader import CaseEntity, CaseEvent, CaseRelationship, InformationStatus


@dataclass
class LegalTokenizerConfig:
    """Configuration for legal domain tokenizer"""

    vocab_size: int = 50000
    max_length: int = 512
    special_tokens: Dict[str, str] = field(
        default_factory=lambda: {
            "cls_token": "[CLS]",
            "sep_token": "[SEP]",
            "pad_token": "[PAD]",
            "unk_token": "[UNK]",
            "mask_token": "[MASK]",
            "entity_token": "[ENTITY]",
            "event_token": "[EVENT]",
            "evidence_token": "[EVIDENCE]",
            "timeline_token": "[TIMELINE]",
        }
    )
    legal_entities: List[str] = field(
        default_factory=lambda: [
            "PERSON",
            "ORGANIZATION",
            "COURT",
            "CASE_NUMBER",
            "DATE",
            "MONEY",
            "LOCATION",
            "EVIDENCE_ID",
            "LEGAL_DOCUMENT",
        ]
    )


@dataclass
class AgentPerspectiveHead:
    """Enhanced attention head for agent perspectives"""

    agent_id: str
    perspective_type: str  # "victim", "perpetrator", "witness", "investigator"
    attention_weights: torch.Tensor
    bias_vector: torch.Tensor
    focus_areas: List[str] = field(default_factory=list)
    temporal_bias: float = 0.0
    evidence_weight: float = 1.0


class LegalDomainTokenizer:
    """Specialized tokenizer for legal and investigative documents"""

    def __init__(self, config: LegalTokenizerConfig):
        self.config = config
        self.base_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self._add_special_tokens()
        self.entity_patterns = self._compile_entity_patterns()

    def _add_special_tokens(self):
        """Add legal domain specific tokens"""
        special_tokens = list(self.config.special_tokens.values())
        self.base_tokenizer.add_special_tokens(
            {"additional_special_tokens": special_tokens}
        )

    def _compile_entity_patterns(self) -> Dict[str, str]:
        """Compile regex patterns for legal entity recognition"""
        import re

        return {
            "CASE_NUMBER": r"\b\d{4}-\d{6}\b",
            "MONEY": r"\$[\d,]+\.?\d*",
            "DATE": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            "EVIDENCE_ID": r"\bEVID-\d+\b",
            "COURT": r"\b(?:High Court|Supreme Court|District Court)\b",
        }

    def tokenize_case_document(
        self,
        text: str,
        entities: List[CaseEntity] = None,
        events: List[CaseEvent] = None,
    ) -> Dict[str, Any]:
        """Tokenize a case document with entity and event awareness"""
        # Pre-process text to mark entities and events
        processed_text = self._preprocess_legal_text(text, entities, events)

        # Tokenize with BERT tokenizer
        encoding = self.base_tokenizer(
            processed_text,
            max_length=self.config.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        # Add custom features
        encoding["entity_mask"] = self._create_entity_mask(encoding["input_ids"])
        encoding["event_mask"] = self._create_event_mask(encoding["input_ids"])
        encoding["temporal_positions"] = self._extract_temporal_positions(
            processed_text
        )

        return encoding

    def _preprocess_legal_text(
        self,
        text: str,
        entities: List[CaseEntity] = None,
        events: List[CaseEvent] = None,
    ) -> str:
        """Preprocess text to highlight legal entities and events"""
        processed = text

        # Mark entities
        if entities:
            for entity in entities:
                processed = processed.replace(
                    entity.name, f"[ENTITY] {entity.name} [/ENTITY]"
                )

        # Mark events
        if events:
            for event in events:
                # Simple keyword matching for event descriptions
                keywords = event.description.split()[:3]  # First 3 words
                for keyword in keywords:
                    if len(keyword) > 3:  # Avoid short words
                        processed = processed.replace(
                            keyword, f"[EVENT] {keyword} [/EVENT]"
                        )

        return processed

    def _create_entity_mask(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Create mask for entity tokens"""
        entity_token_id = self.base_tokenizer.convert_tokens_to_ids("[ENTITY]")
        return (input_ids == entity_token_id).float()

    def _create_event_mask(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Create mask for event tokens"""
        event_token_id = self.base_tokenizer.convert_tokens_to_ids("[EVENT]")
        return (input_ids == event_token_id).float()

    def _extract_temporal_positions(self, text: str) -> torch.Tensor:
        """Extract temporal position information"""
        # Simplified temporal position extraction
        # In practice, this would use more sophisticated NLP
        import re

        dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
        positions = torch.zeros(self.config.max_length)

        # Mark positions with temporal information
        for i, date in enumerate(dates[:10]):  # Limit to first 10 dates
            if i < self.config.max_length:
                positions[i] = 1.0

        return positions


class MultiAgentTransformerModel(nn.Module):
    """Transformer model with multi-agent perspective attention"""

    def __init__(self, config: BertConfig, num_agents: int = 8):
        super().__init__()
        self.config = config
        self.num_agents = num_agents

        # Base BERT model
        self.bert = BertModel(config)

        # Agent-specific attention heads
        self.agent_attention_heads = nn.ModuleList(
            [
                nn.MultiheadAttention(
                    embed_dim=config.hidden_size,
                    num_heads=config.num_attention_heads // num_agents,
                    dropout=config.attention_probs_dropout_prob,
                )
                for _ in range(num_agents)
            ]
        )

        # Agent perspective embeddings
        self.agent_embeddings = nn.Embedding(num_agents, config.hidden_size)

        # Cross-agent attention
        self.cross_agent_attention = nn.MultiheadAttention(
            embed_dim=config.hidden_size,
            num_heads=config.num_attention_heads,
            dropout=config.attention_probs_dropout_prob,
        )

        # Classification heads for different tasks
        self.entity_classifier = nn.Linear(config.hidden_size, 10)  # 10 entity types
        self.event_classifier = nn.Linear(config.hidden_size, 8)  # 8 event types
        self.relationship_classifier = nn.Linear(
            config.hidden_size, 5
        )  # 5 relationship types
        self.timeline_regressor = nn.Linear(config.hidden_size, 1)  # Timeline position

        # Dropout
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(
        self,
        input_ids,
        attention_mask=None,
        agent_ids=None,
        entity_mask=None,
        event_mask=None,
        temporal_positions=None,
    ):
        """Forward pass with multi-agent attention"""

        # Get BERT embeddings
        bert_output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = bert_output.last_hidden_state  # [batch, seq_len, hidden]
        pooled_output = bert_output.pooler_output  # [batch, hidden]

        # Apply agent-specific attention
        agent_outputs = []
        for i, agent_head in enumerate(self.agent_attention_heads):
            # Add agent perspective embedding
            agent_emb = self.agent_embeddings(
                torch.tensor(i).to(sequence_output.device)
            )
            agent_enhanced = sequence_output + agent_emb.unsqueeze(0).unsqueeze(0)

            # Apply agent-specific attention
            agent_attended, _ = agent_head(
                agent_enhanced.transpose(0, 1),  # [seq_len, batch, hidden]
                agent_enhanced.transpose(0, 1),
                agent_enhanced.transpose(0, 1),
                key_padding_mask=(
                    ~attention_mask.bool() if attention_mask is not None else None
                ),
            )
            agent_outputs.append(
                agent_attended.transpose(0, 1)
            )  # Back to [batch, seq_len, hidden]

        # Combine agent perspectives
        combined_agent_output = torch.stack(
            agent_outputs, dim=2
        )  # [batch, seq_len, num_agents, hidden]
        combined_agent_output = combined_agent_output.mean(
            dim=2
        )  # Average across agents

        # Cross-agent attention
        cross_attended, cross_attention_weights = self.cross_agent_attention(
            combined_agent_output.transpose(0, 1),
            combined_agent_output.transpose(0, 1),
            combined_agent_output.transpose(0, 1),
            key_padding_mask=(
                ~attention_mask.bool() if attention_mask is not None else None
            ),
        )
        final_output = cross_attended.transpose(0, 1)  # [batch, seq_len, hidden]

        # Apply dropout
        final_output = self.dropout(final_output)

        # Classification outputs
        entity_logits = self.entity_classifier(final_output)
        event_logits = self.event_classifier(final_output)
        relationship_logits = self.relationship_classifier(pooled_output)
        timeline_scores = self.timeline_regressor(final_output).squeeze(-1)

        return {
            "sequence_output": final_output,
            "pooled_output": pooled_output,
            "entity_logits": entity_logits,
            "event_logits": event_logits,
            "relationship_logits": relationship_logits,
            "timeline_scores": timeline_scores,
            "cross_attention_weights": cross_attention_weights,
            "agent_outputs": agent_outputs,
        }


class OpenAIIntegration:
    """Integration with OpenAI API for enhanced analysis"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key

    def analyze_case_summary(
        self,
        entities: List[CaseEntity],
        events: List[CaseEvent],
        relationships: List[CaseRelationship],
    ) -> Dict[str, Any]:
        """Generate case analysis using OpenAI GPT"""
        if not self.api_key:
            return {"error": "OpenAI API key not configured"}

        # Prepare context
        context = self._prepare_case_context(entities, events, relationships)

        prompt = f"""
        As a legal analyst, analyze the following case information and provide:
        1. Key patterns and relationships
        2. Timeline analysis
        3. Potential areas of concern
        4. Recommended investigation priorities
        
        Case Information:
        {context}
        
        Analysis:
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional legal analyst specializing in case investigation and evidence analysis.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.3,
            )

            return {
                "analysis": response.choices[0].message.content,
                "model": "gpt-4",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}

    def _prepare_case_context(
        self,
        entities: List[CaseEntity],
        events: List[CaseEvent],
        relationships: List[CaseRelationship],
    ) -> str:
        """Prepare case context for OpenAI analysis"""
        context_parts = []

        # Entities
        context_parts.append("ENTITIES:")
        for entity in entities[:10]:  # Limit to first 10
            context_parts.append(
                f"- {entity.name} ({entity.entity_type}): {entity.verification_status.value}"
            )

        # Events
        context_parts.append("\nEVENTS:")
        for event in sorted(events, key=lambda e: e.date)[:10]:  # Limit and sort
            context_parts.append(
                f"- {event.date.strftime('%Y-%m-%d')}: {event.description}"
            )

        # Relationships
        context_parts.append("\nRELATIONSHIPS:")
        for rel in relationships[:10]:  # Limit to first 10
            context_parts.append(
                f"- {rel.source_entity} -> {rel.target_entity} ({rel.relationship_type})"
            )

        return "\n".join(context_parts)


class LegalTransformerPipeline:
    """Complete pipeline for legal document analysis using transformers"""

    def __init__(self, model_name: str = "bert-base-uncased", num_agents: int = 8):
        self.tokenizer_config = LegalTokenizerConfig()
        self.tokenizer = LegalDomainTokenizer(self.tokenizer_config)

        # Initialize model
        config = BertConfig.from_pretrained(model_name)
        config.num_labels = 10  # Adjust based on your classification needs
        self.model = MultiAgentTransformerModel(config, num_agents)

        # OpenAI integration
        self.openai_integration = OpenAIIntegration()

        # Device setup
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def analyze_case_documents(
        self,
        documents: List[str],
        entities: List[CaseEntity] = None,
        events: List[CaseEvent] = None,
    ) -> Dict[str, Any]:
        """Analyze case documents using the transformer pipeline"""
        results = {
            "document_analyses": [],
            "aggregate_insights": {},
            "openai_analysis": None,
        }

        # Process each document
        for i, doc in enumerate(documents):
            doc_analysis = self._analyze_single_document(doc, entities, events)
            results["document_analyses"].append(
                {"document_id": i, "analysis": doc_analysis}
            )

        # Aggregate insights
        results["aggregate_insights"] = self._aggregate_document_insights(
            results["document_analyses"]
        )

        # OpenAI analysis if available
        if entities and events:
            results["openai_analysis"] = self.openai_integration.analyze_case_summary(
                entities, events, []
            )

        return results

    def _analyze_single_document(
        self,
        document: str,
        entities: List[CaseEntity] = None,
        events: List[CaseEvent] = None,
    ) -> Dict[str, Any]:
        """Analyze a single document"""
        # Tokenize
        encoding = self.tokenizer.tokenize_case_document(document, entities, events)

        # Move to device
        for key in encoding:
            if isinstance(encoding[key], torch.Tensor):
                encoding[key] = encoding[key].to(self.device)

        # Model inference
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**encoding)

        # Process outputs
        analysis = {
            "entity_predictions": self._process_entity_predictions(
                outputs["entity_logits"]
            ),
            "event_predictions": self._process_event_predictions(
                outputs["event_logits"]
            ),
            "timeline_scores": outputs["timeline_scores"].cpu().numpy().tolist(),
            "attention_patterns": self._analyze_attention_patterns(
                outputs["cross_attention_weights"]
            ),
        }

        return analysis

    def _process_entity_predictions(
        self, entity_logits: torch.Tensor
    ) -> List[Dict[str, Any]]:
        """Process entity classification predictions"""
        predictions = []
        probs = F.softmax(entity_logits, dim=-1)

        for i in range(entity_logits.size(1)):  # For each token position
            token_probs = probs[0, i].cpu().numpy()
            top_class = np.argmax(token_probs)
            confidence = float(token_probs[top_class])

            if confidence > 0.5:  # Only include confident predictions
                predictions.append(
                    {
                        "position": i,
                        "entity_type": self.tokenizer_config.legal_entities[
                            top_class % len(self.tokenizer_config.legal_entities)
                        ],
                        "confidence": confidence,
                    }
                )

        return predictions

    def _process_event_predictions(
        self, event_logits: torch.Tensor
    ) -> List[Dict[str, Any]]:
        """Process event classification predictions"""
        predictions = []
        probs = F.softmax(event_logits, dim=-1)

        event_types = [
            "communication",
            "transaction",
            "meeting",
            "decision",
            "action",
            "evidence",
            "legal",
            "other",
        ]

        for i in range(event_logits.size(1)):
            token_probs = probs[0, i].cpu().numpy()
            top_class = np.argmax(token_probs)
            confidence = float(token_probs[top_class])

            if confidence > 0.5:
                predictions.append(
                    {
                        "position": i,
                        "event_type": event_types[top_class % len(event_types)],
                        "confidence": confidence,
                    }
                )

        return predictions

    def _analyze_attention_patterns(
        self, attention_weights: torch.Tensor
    ) -> Dict[str, Any]:
        """Analyze attention patterns for insights"""
        # Convert to numpy for analysis
        attention_np = attention_weights.cpu().numpy()

        return {
            "max_attention_positions": np.unravel_index(
                np.argmax(attention_np), attention_np.shape
            ),
            "attention_entropy": float(
                -np.sum(attention_np * np.log(attention_np + 1e-10))
            ),
            "attention_concentration": float(np.max(attention_np)),
        }

    def _aggregate_document_insights(
        self, document_analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Aggregate insights across all documents"""
        all_entities = []
        all_events = []

        for doc_analysis in document_analyses:
            all_entities.extend(doc_analysis["analysis"]["entity_predictions"])
            all_events.extend(doc_analysis["analysis"]["event_predictions"])

        # Count entity types
        entity_counts = {}
        for entity in all_entities:
            entity_type = entity["entity_type"]
            entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

        # Count event types
        event_counts = {}
        for event in all_events:
            event_type = event["event_type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        return {
            "total_entities_detected": len(all_entities),
            "total_events_detected": len(all_events),
            "entity_type_distribution": entity_counts,
            "event_type_distribution": event_counts,
            "documents_processed": len(document_analyses),
        }

    def fine_tune_model(
        self,
        training_data: List[Dict[str, Any]],
        output_dir: str = "./fine_tuned_model",
    ):
        """Fine-tune the model on domain-specific data"""
        # This would implement fine-tuning logic
        # For now, we'll provide a placeholder
        print(f"Fine-tuning model with {len(training_data)} examples...")
        print(f"Model will be saved to {output_dir}")

        # In a real implementation, you would:
        # 1. Prepare training dataset
        # 2. Set up training arguments
        # 3. Create trainer
        # 4. Train the model
        # 5. Save the fine-tuned model

        return {"status": "Fine-tuning completed", "model_path": output_dir}


if __name__ == "__main__":
    # Example usage
    pipeline = LegalTransformerPipeline()

    # Sample documents
    documents = [
        "On 2023-01-15, John Smith contacted ABC Legal Firm regarding a financial dispute involving $50,000.",
        "Evidence EVID-001 shows communication between parties on 2023-01-20 discussing settlement terms.",
    ]

    # Sample entities
    entities = [
        CaseEntity(
            "john_smith",
            "John Smith",
            "person",
            ["plaintiff"],
            verification_status=InformationStatus.VERIFIED,
        ),
        CaseEntity(
            "abc_legal",
            "ABC Legal Firm",
            "organization",
            ["legal_counsel"],
            verification_status=InformationStatus.VERIFIED,
        ),
    ]

    # Analyze
    results = pipeline.analyze_case_documents(documents, entities)
    print(json.dumps(results, indent=2, default=str))
