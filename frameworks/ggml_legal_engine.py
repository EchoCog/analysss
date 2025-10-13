#!/usr/bin/env python3
"""
GGML Legal Analysis Engine
=========================

Implements efficient machine learning inference engines using GGML principles
(Georgi Gerganov Machine Learning) for legal document analysis, pattern recognition,
and cross-jurisdictional reasoning.

GGML Design Principles:
1. Efficient tensor operations for legal text analysis
2. Quantized neural networks for resource optimization
3. CPU-optimized inference for scalable deployment
4. Custom operators for legal domain patterns
5. Memory-efficient attention mechanisms

Key Features:
- Legal document classification and summarization
- Entity relationship extraction from legal texts
- Cross-jurisdictional legal pattern matching
- Fraud detection and risk assessment
- Evidence strength quantification
"""

import logging
import math
import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GGMLTensorType(Enum):
    """GGML tensor types for legal analysis"""
    LEGAL_DOCUMENT = "legal_document"
    ENTITY_EMBEDDING = "entity_embedding"
    RELATIONSHIP_MATRIX = "relationship_matrix"
    ATTENTION_WEIGHTS = "attention_weights"
    CLASSIFICATION_LOGITS = "classification_logits"


class GGMLOperatorType(Enum):
    """Custom GGML operators for legal domain"""
    LEGAL_ATTENTION = "legal_attention"
    JURISDICTION_MERGE = "jurisdiction_merge"
    EVIDENCE_WEIGHTING = "evidence_weighting"
    PATTERN_MATCHING = "pattern_matching"
    RELEVANCE_SCORING = "relevance_scoring"


@dataclass
class GGMLTensor:
    """GGML tensor for efficient legal computations"""
    name: str
    tensor_type: GGMLTensorType
    shape: Tuple[int, ...]
    dtype: str = "float32"
    data: Optional[np.ndarray] = None
    quantized: bool = False
    quantization_bits: int = 8
    
    def __post_init__(self):
        if self.data is None:
            if self.dtype == "float32":
                self.data = np.zeros(self.shape, dtype=np.float32)
            elif self.dtype == "int8":
                self.data = np.zeros(self.shape, dtype=np.int8)
            elif self.dtype == "int32":
                self.data = np.zeros(self.shape, dtype=np.int32)
    
    def quantize(self, bits: int = 8) -> 'GGMLTensor':
        """Quantize tensor for efficient storage and computation"""
        if self.data is None or self.quantized:
            return self
        
        if bits == 8:
            # Quantize to int8
            data_min = self.data.min()
            data_max = self.data.max()
            
            # Handle case where all values are the same
            if data_max == data_min:
                scale = 1.0
                quantized_data = np.zeros_like(self.data, dtype=np.int8)
            else:
                scale = (data_max - data_min) / 255.0
                quantized_data = ((self.data - data_min) / scale).astype(np.int8)
            
            result = GGMLTensor(
                name=f"{self.name}_q{bits}",
                tensor_type=self.tensor_type,
                shape=self.shape,
                dtype="int8",
                data=quantized_data,
                quantized=True,
                quantization_bits=bits
            )
            result._scale = scale
            result._offset = data_min
            return result
        
        return self
    
    def dequantize(self) -> 'GGMLTensor':
        """Dequantize tensor back to float32"""
        if not self.quantized:
            return self
        
        if hasattr(self, '_scale') and hasattr(self, '_offset'):
            dequantized_data = (self.data.astype(np.float32) * self._scale + self._offset)
            return GGMLTensor(
                name=self.name.replace(f"_q{self.quantization_bits}", ""),
                tensor_type=self.tensor_type,
                shape=self.shape,
                dtype="float32",
                data=dequantized_data,
                quantized=False
            )
        
        return self


@dataclass
class GGMLOperator:
    """GGML operator for legal domain computations"""
    name: str
    operator_type: GGMLOperatorType
    input_specs: List[Dict[str, Any]]
    output_spec: Dict[str, Any]
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def execute(self, inputs: List[GGMLTensor]) -> GGMLTensor:
        """Execute the operator on input tensors"""
        if len(inputs) != len(self.input_specs):
            raise ValueError(f"Expected {len(self.input_specs)} inputs, got {len(inputs)}")
        
        if self.operator_type == GGMLOperatorType.LEGAL_ATTENTION:
            return self._legal_attention(inputs)
        elif self.operator_type == GGMLOperatorType.JURISDICTION_MERGE:
            return self._jurisdiction_merge(inputs)
        elif self.operator_type == GGMLOperatorType.EVIDENCE_WEIGHTING:
            return self._evidence_weighting(inputs)
        elif self.operator_type == GGMLOperatorType.PATTERN_MATCHING:
            return self._pattern_matching(inputs)
        elif self.operator_type == GGMLOperatorType.RELEVANCE_SCORING:
            return self._relevance_scoring(inputs)
        else:
            raise ValueError(f"Unknown operator type: {self.operator_type}")
    
    def _legal_attention(self, inputs: List[GGMLTensor]) -> GGMLTensor:
        """Compute legal-domain attention weights"""
        query, key, value = inputs[0], inputs[1], inputs[2]
        
        # Compute attention scores with legal domain bias
        scores = np.matmul(query.data, key.data.T)
        
        # Apply legal domain scaling factors
        legal_terms_boost = self.parameters.get("legal_terms_boost", 1.2)
        evidence_terms_boost = self.parameters.get("evidence_terms_boost", 1.5)
        
        # Simple legal term detection (in practice, would use trained weights)
        legal_mask = np.ones_like(scores) * legal_terms_boost
        scores = scores * legal_mask
        
        # Softmax attention
        exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        attention_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        
        # Apply attention to values
        output_data = np.matmul(attention_weights, value.data)
        
        return GGMLTensor(
            name="legal_attention_output",
            tensor_type=GGMLTensorType.ATTENTION_WEIGHTS,
            shape=output_data.shape,
            data=output_data
        )
    
    def _jurisdiction_merge(self, inputs: List[GGMLTensor]) -> GGMLTensor:
        """Merge analysis from multiple jurisdictions"""
        za_tensor, uk_tensor = inputs[0], inputs[1]
        
        # Weighted merge based on jurisdiction relevance
        za_weight = self.parameters.get("za_weight", 0.5)
        uk_weight = self.parameters.get("uk_weight", 0.5)
        
        # Normalize weights
        total_weight = za_weight + uk_weight
        za_weight /= total_weight
        uk_weight /= total_weight
        
        merged_data = za_weight * za_tensor.data + uk_weight * uk_tensor.data
        
        return GGMLTensor(
            name="jurisdiction_merged",
            tensor_type=GGMLTensorType.CLASSIFICATION_LOGITS,
            shape=merged_data.shape,
            data=merged_data
        )
    
    def _evidence_weighting(self, inputs: List[GGMLTensor]) -> GGMLTensor:
        """Apply evidence strength weighting"""
        evidence_tensor = inputs[0]
        
        # Evidence type weights
        documentary_weight = self.parameters.get("documentary_weight", 1.0)
        financial_weight = self.parameters.get("financial_weight", 0.9)
        testimonial_weight = self.parameters.get("testimonial_weight", 0.7)
        
        # Apply weights (simplified - in practice would use learned embeddings)
        weighted_data = evidence_tensor.data * documentary_weight
        
        return GGMLTensor(
            name="evidence_weighted",
            tensor_type=evidence_tensor.tensor_type,
            shape=evidence_tensor.shape,
            data=weighted_data
        )
    
    def _pattern_matching(self, inputs: List[GGMLTensor]) -> GGMLTensor:
        """Pattern matching for legal document analysis"""
        document_tensor, pattern_tensor = inputs[0], inputs[1]
        
        # Compute similarity scores
        similarity = np.dot(document_tensor.data, pattern_tensor.data.T)
        
        # Apply threshold
        threshold = self.parameters.get("similarity_threshold", 0.7)
        matches = (similarity > threshold).astype(np.float32)
        
        return GGMLTensor(
            name="pattern_matches",
            tensor_type=GGMLTensorType.CLASSIFICATION_LOGITS,
            shape=matches.shape,
            data=matches
        )
    
    def _relevance_scoring(self, inputs: List[GGMLTensor]) -> GGMLTensor:
        """Compute relevance scores for legal analysis"""
        content_tensor = inputs[0]
        
        # Multi-factor relevance scoring
        legal_significance = self.parameters.get("legal_significance", 1.0)
        evidence_strength = self.parameters.get("evidence_strength", 1.0)
        cross_jurisdiction = self.parameters.get("cross_jurisdiction", 1.0)
        
        # Compute weighted relevance - ensure compatible shapes
        weights = np.array([legal_significance, evidence_strength, cross_jurisdiction])
        if len(content_tensor.data.shape) == 1 and content_tensor.data.shape[0] >= len(weights):
            # Use first n elements if tensor is longer
            relevance_data = content_tensor.data[:len(weights)] * weights
        else:
            # Broadcast or resize as needed
            relevance_data = content_tensor.data * np.mean(weights)
        
        # Normalize to [0, 1]
        relevance_scores = 1.0 / (1.0 + np.exp(-relevance_data))
        
        return GGMLTensor(
            name="relevance_scores",
            tensor_type=GGMLTensorType.CLASSIFICATION_LOGITS,
            shape=relevance_scores.shape,
            data=relevance_scores
        )


class GGMLLegalEngine:
    """
    Main GGML engine for legal analysis with efficient CPU inference.
    Implements GGML principles for legal domain applications.
    """
    
    def __init__(self, quantization_enabled: bool = True, quantization_bits: int = 8):
        self.quantization_enabled = quantization_enabled
        self.quantization_bits = quantization_bits
        self.operators: Dict[str, GGMLOperator] = {}
        self.tensors: Dict[str, GGMLTensor] = {}
        self._initialize_legal_operators()
        logger.info("Initialized GGML Legal Engine")
    
    def _initialize_legal_operators(self):
        """Initialize standard legal analysis operators"""
        
        # Legal attention operator
        self.operators["legal_attention"] = GGMLOperator(
            name="legal_attention",
            operator_type=GGMLOperatorType.LEGAL_ATTENTION,
            input_specs=[
                {"name": "query", "type": GGMLTensorType.LEGAL_DOCUMENT},
                {"name": "key", "type": GGMLTensorType.LEGAL_DOCUMENT},
                {"name": "value", "type": GGMLTensorType.LEGAL_DOCUMENT}
            ],
            output_spec={"type": GGMLTensorType.ATTENTION_WEIGHTS},
            parameters={
                "legal_terms_boost": 1.3,
                "evidence_terms_boost": 1.6
            }
        )
        
        # Jurisdiction merge operator
        self.operators["jurisdiction_merge"] = GGMLOperator(
            name="jurisdiction_merge", 
            operator_type=GGMLOperatorType.JURISDICTION_MERGE,
            input_specs=[
                {"name": "za_analysis", "type": GGMLTensorType.CLASSIFICATION_LOGITS},
                {"name": "uk_analysis", "type": GGMLTensorType.CLASSIFICATION_LOGITS}
            ],
            output_spec={"type": GGMLTensorType.CLASSIFICATION_LOGITS},
            parameters={"za_weight": 0.5, "uk_weight": 0.5}
        )
        
        # Evidence weighting operator
        self.operators["evidence_weighting"] = GGMLOperator(
            name="evidence_weighting",
            operator_type=GGMLOperatorType.EVIDENCE_WEIGHTING,
            input_specs=[
                {"name": "evidence", "type": GGMLTensorType.LEGAL_DOCUMENT}
            ],
            output_spec={"type": GGMLTensorType.LEGAL_DOCUMENT},
            parameters={
                "documentary_weight": 1.0,
                "financial_weight": 0.95,
                "testimonial_weight": 0.8
            }
        )
        
        # Pattern matching operator
        self.operators["pattern_matching"] = GGMLOperator(
            name="pattern_matching",
            operator_type=GGMLOperatorType.PATTERN_MATCHING,
            input_specs=[
                {"name": "document", "type": GGMLTensorType.LEGAL_DOCUMENT},
                {"name": "pattern", "type": GGMLTensorType.LEGAL_DOCUMENT}
            ],
            output_spec={"type": GGMLTensorType.CLASSIFICATION_LOGITS},
            parameters={"similarity_threshold": 0.75}
        )
        
        # Relevance scoring operator
        self.operators["relevance_scoring"] = GGMLOperator(
            name="relevance_scoring",
            operator_type=GGMLOperatorType.RELEVANCE_SCORING,
            input_specs=[
                {"name": "content", "type": GGMLTensorType.LEGAL_DOCUMENT}
            ],
            output_spec={"type": GGMLTensorType.CLASSIFICATION_LOGITS},
            parameters={
                "legal_significance": 1.0,
                "evidence_strength": 1.0,
                "cross_jurisdiction": 1.2
            }
        )
    
    def create_tensor(self, name: str, tensor_type: GGMLTensorType, 
                     shape: Tuple[int, ...], data: Optional[np.ndarray] = None) -> GGMLTensor:
        """Create and register a new tensor"""
        tensor = GGMLTensor(
            name=name,
            tensor_type=tensor_type,
            shape=shape,
            data=data
        )
        
        # Store the original tensor first
        self.tensors[name] = tensor
        
        # Quantize if enabled and return quantized version
        if self.quantization_enabled and data is not None:
            quantized_tensor = tensor.quantize(self.quantization_bits)
            self.tensors[quantized_tensor.name] = quantized_tensor
            return quantized_tensor
        
        return tensor
    
    def execute_operator(self, operator_name: str, input_names: List[str]) -> GGMLTensor:
        """Execute a named operator on specified input tensors"""
        if operator_name not in self.operators:
            raise ValueError(f"Unknown operator: {operator_name}")
        
        operator = self.operators[operator_name]
        inputs = [self.tensors[name] for name in input_names]
        
        # Dequantize inputs if needed
        if self.quantization_enabled:
            inputs = [tensor.dequantize() if tensor.quantized else tensor for tensor in inputs]
        
        result = operator.execute(inputs)
        
        # Quantize result if enabled
        if self.quantization_enabled:
            result = result.quantize(self.quantization_bits)
        
        return result
    
    def analyze_legal_document(self, document_text: str, document_type: str = "general") -> Dict[str, Any]:
        """Analyze a legal document using GGML inference"""
        
        # Convert text to tensor representation (simplified)
        # In practice, would use proper tokenization and embeddings
        text_embedding = self._text_to_embedding(document_text)
        doc_tensor = self.create_tensor(
            name="input_document",
            tensor_type=GGMLTensorType.LEGAL_DOCUMENT,
            shape=text_embedding.shape,
            data=text_embedding
        )
        
        # Apply evidence weighting
        weighted_tensor = self.execute_operator("evidence_weighting", ["input_document"])
        self.tensors["weighted_document"] = weighted_tensor
        
        # Compute relevance scores
        relevance_tensor = self.execute_operator("relevance_scoring", ["weighted_document"])
        
        # Extract results
        relevance_scores = relevance_tensor.dequantize().data if relevance_tensor.quantized else relevance_tensor.data
        
        return {
            "document_type": document_type,
            "relevance_score": float(np.mean(relevance_scores)),
            "legal_significance": float(np.max(relevance_scores)),
            "evidence_strength": float(relevance_scores[1]) if len(relevance_scores) > 1 else 0.0,
            "analysis_timestamp": datetime.now().isoformat(),
            "ggml_optimized": True
        }
    
    def cross_jurisdictional_analysis(self, za_features: np.ndarray, uk_features: np.ndarray) -> Dict[str, Any]:
        """Perform cross-jurisdictional analysis using GGML operators"""
        
        # Create jurisdiction tensors
        za_tensor = self.create_tensor(
            name="za_analysis",
            tensor_type=GGMLTensorType.CLASSIFICATION_LOGITS,
            shape=za_features.shape,
            data=za_features
        )
        
        uk_tensor = self.create_tensor(
            name="uk_analysis", 
            tensor_type=GGMLTensorType.CLASSIFICATION_LOGITS,
            shape=uk_features.shape,
            data=uk_features
        )
        
        # Merge jurisdictional analyses
        merged_tensor = self.execute_operator("jurisdiction_merge", ["za_analysis", "uk_analysis"])
        merged_scores = merged_tensor.dequantize().data if merged_tensor.quantized else merged_tensor.data
        
        return {
            "merged_score": float(np.mean(merged_scores)),
            "za_contribution": float(np.mean(za_features)),
            "uk_contribution": float(np.mean(uk_features)),
            "cross_jurisdictional_strength": float(np.max(merged_scores)),
            "ggml_optimized": True,
            "quantization_applied": self.quantization_enabled
        }
    
    def detect_fraud_patterns(self, document_features: np.ndarray, 
                            known_patterns: List[np.ndarray]) -> Dict[str, Any]:
        """Detect fraud patterns using GGML pattern matching"""
        
        # Create document tensor
        doc_tensor = self.create_tensor(
            name="fraud_document",
            tensor_type=GGMLTensorType.LEGAL_DOCUMENT,
            shape=document_features.shape,
            data=document_features
        )
        
        pattern_matches = []
        
        for i, pattern in enumerate(known_patterns):
            # Create pattern tensor
            pattern_tensor = self.create_tensor(
                name=f"fraud_pattern_{i}",
                tensor_type=GGMLTensorType.LEGAL_DOCUMENT,
                shape=pattern.shape,
                data=pattern
            )
            
            # Execute pattern matching
            match_tensor = self.execute_operator("pattern_matching", 
                                               ["fraud_document", f"fraud_pattern_{i}"])
            
            match_scores = match_tensor.dequantize().data if match_tensor.quantized else match_tensor.data
            pattern_matches.append({
                "pattern_id": i,
                "match_score": float(np.mean(match_scores)),
                "confidence": float(np.max(match_scores))
            })
        
        # Overall fraud detection result
        max_match = max(pattern_matches, key=lambda x: x["match_score"]) if pattern_matches else None
        
        return {
            "fraud_detected": max_match["match_score"] > 0.7 if max_match else False,
            "confidence_score": max_match["confidence"] if max_match else 0.0,
            "best_matching_pattern": max_match["pattern_id"] if max_match else None,
            "all_pattern_matches": pattern_matches,
            "ggml_optimized": True
        }
    
    def _text_to_embedding(self, text: str) -> np.ndarray:
        """Convert text to embedding representation (simplified)"""
        # This is a simplified embedding - in practice would use proper NLP models
        words = text.lower().split()
        
        # Create simple bag-of-words style embedding
        # Focus on legal and financial terms
        legal_keywords = {
            "fraud", "fiduciary", "duty", "breach", "evidence", "contract",
            "payment", "transaction", "financial", "invoice", "debt", "amount",
            "company", "director", "jurisdiction", "court", "law", "legal"
        }
        
        embedding = np.zeros(len(legal_keywords) + 10)  # Extra dimensions
        
        for i, keyword in enumerate(legal_keywords):
            embedding[i] = sum(1 for word in words if keyword in word) / len(words)
        
        # Add document length and complexity features
        embedding[-3] = min(1.0, len(words) / 1000)  # Normalized length
        embedding[-2] = len(set(words)) / len(words) if words else 0  # Vocabulary diversity
        embedding[-1] = sum(1 for word in words if len(word) > 6) / len(words) if words else 0  # Complexity
        
        return embedding.astype(np.float32)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get GGML engine performance statistics"""
        total_tensors = len(self.tensors)
        quantized_tensors = sum(1 for tensor in self.tensors.values() if tensor.quantized)
        
        total_memory = sum(
            tensor.data.nbytes if tensor.data is not None else 0
            for tensor in self.tensors.values()
        )
        
        return {
            "total_tensors": total_tensors,
            "quantized_tensors": quantized_tensors,
            "quantization_ratio": quantized_tensors / total_tensors if total_tensors > 0 else 0,
            "total_memory_bytes": total_memory,
            "memory_mb": total_memory / (1024 * 1024),
            "quantization_bits": self.quantization_bits,
            "operators_available": len(self.operators)
        }


__all__ = [
    "GGMLTensorType",
    "GGMLOperatorType", 
    "GGMLTensor",
    "GGMLOperator",
    "GGMLLegalEngine"
]