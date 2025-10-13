#!/usr/bin/env python3
"""
LLM/Transformer Schema for HyperGNN Framework
============================================

This module creates a schema for an LLM/transformer model that maps the perspective
of each agent to an attention head and uses analogous features to tokenize the
timeline of events like parts of speech in a sentence.

The transformer architecture enables self-attention and cross-attention mechanisms
to correlate all agent perspectives against all others in the timeline analysis.

Key Concepts:
- Agent perspectives → Attention heads
- Timeline events → Tokens (with POS-like features)
- Self-attention → Intra-agent perspective correlation
- Cross-attention → Inter-agent perspective correlation
- Timeline sequence → Token sequence processing
"""

import numpy as np
from typing import Dict, List, Set, Tuple, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
from abc import ABC, abstractmethod

from .hypergnn_core import (
    Agent,
    TimelineTensor,
    DiscreteEvent,
    TensorType,
    AgentType,
    EventType,
)


class TokenType(Enum):
    """Token types analogous to parts of speech for timeline events"""

    # Action tokens (verbs)
    ACTION_COMMUNICATION = "action_communication"  # like VERB
    ACTION_TRANSACTION = "action_transaction"  # like VERB
    ACTION_DECISION = "action_decision"  # like VERB
    ACTION_MEETING = "action_meeting"  # like VERB

    # Entity tokens (nouns)
    ENTITY_AGENT = "entity_agent"  # like NOUN
    ENTITY_RESOURCE = "entity_resource"  # like NOUN
    ENTITY_LOCATION = "entity_location"  # like NOUN

    # Modifier tokens (adjectives/adverbs)
    MODIFIER_TEMPORAL = "modifier_temporal"  # like ADJECTIVE
    MODIFIER_INTENSITY = "modifier_intensity"  # like ADVERB
    MODIFIER_RELATIONSHIP = "modifier_relationship"  # like ADJECTIVE

    # Connection tokens (prepositions/conjunctions)
    CONNECTION_CAUSAL = "connection_causal"  # like CONJUNCTION
    CONNECTION_TEMPORAL = "connection_temporal"  # like PREPOSITION
    CONNECTION_SPATIAL = "connection_spatial"  # like PREPOSITION

    # Special tokens
    SEQUENCE_START = "sequence_start"  # [CLS] equivalent
    SEQUENCE_END = "sequence_end"  # [SEP] equivalent
    PADDING = "padding"  # [PAD] equivalent
    UNKNOWN = "unknown"  # [UNK] equivalent


@dataclass
class EventToken:
    """Represents a tokenized timeline event with NLP-style features"""

    token_id: str
    token_type: TokenType
    timestamp: datetime
    embedding: np.ndarray
    attention_mask: bool = True

    # POS-style features
    semantic_role: str = ""  # Subject, Object, Predicate, etc.
    dependency_relation: str = ""  # ROOT, compound, nmod, etc.
    named_entity_type: str = ""  # PERSON, ORG, DATE, etc.

    # Domain-specific features
    agent_perspective: str = ""  # Which agent's perspective this token represents
    evidence_strength: float = 1.0  # Confidence/reliability score
    motive_relevance: float = 0.0  # Relevance to motive analysis
    means_relevance: float = 0.0  # Relevance to means analysis
    opportunity_relevance: float = 0.0  # Relevance to opportunity analysis

    # Contextual features
    preceding_tokens: List[str] = field(default_factory=list)
    following_tokens: List[str] = field(default_factory=list)
    concurrent_tokens: List[str] = field(default_factory=list)  # Same timestamp

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttentionHead:
    """Represents an attention head mapped to an agent's perspective"""

    head_id: str
    agent_id: str
    agent_perspective: str  # "victim", "perpetrator", "witness", "investigator", etc.

    # Attention parameters
    query_weights: np.ndarray
    key_weights: np.ndarray
    value_weights: np.ndarray

    # Perspective-specific filters
    focus_token_types: Set[TokenType] = field(default_factory=set)
    temporal_window: Optional[Tuple[datetime, datetime]] = None
    relationship_bias: Dict[str, float] = field(default_factory=dict)

    # Learned parameters
    attention_patterns: Dict[str, np.ndarray] = field(default_factory=dict)
    bias_vector: np.ndarray = field(default_factory=lambda: np.zeros(512))

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransformerBlock:
    """A transformer block for processing agent perspectives and timeline sequences"""

    block_id: str
    attention_heads: List[AttentionHead]

    # Multi-head attention parameters
    num_heads: int = 8
    embed_dim: int = 512
    head_dim: int = 64  # embed_dim // num_heads

    # Feed-forward network parameters
    ff_hidden_dim: int = 2048
    ff_weights_1: np.ndarray = field(
        default_factory=lambda: np.random.randn(512, 2048) * 0.1
    )
    ff_weights_2: np.ndarray = field(
        default_factory=lambda: np.random.randn(2048, 512) * 0.1
    )
    ff_bias_1: np.ndarray = field(default_factory=lambda: np.zeros(2048))
    ff_bias_2: np.ndarray = field(default_factory=lambda: np.zeros(512))

    # Layer normalization parameters
    ln1_weight: np.ndarray = field(default_factory=lambda: np.ones(512))
    ln1_bias: np.ndarray = field(default_factory=lambda: np.zeros(512))
    ln2_weight: np.ndarray = field(default_factory=lambda: np.ones(512))
    ln2_bias: np.ndarray = field(default_factory=lambda: np.zeros(512))

    # Dropout parameters
    attention_dropout: float = 0.1
    ff_dropout: float = 0.1


class TimelineTokenizer:
    """Tokenizes timeline events into transformer-compatible sequences"""

    def __init__(self, vocab_size: int = 10000, embed_dim: int = 512):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.token_to_id: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}
        self.embedding_matrix = np.random.randn(vocab_size, embed_dim) * 0.1
        self.special_tokens = {
            "[CLS]": TokenType.SEQUENCE_START,
            "[SEP]": TokenType.SEQUENCE_END,
            "[PAD]": TokenType.PADDING,
            "[UNK]": TokenType.UNKNOWN,
        }
        self._initialize_special_tokens()

    def _initialize_special_tokens(self):
        """Initialize special tokens in vocabulary"""
        for token, token_type in self.special_tokens.items():
            token_id = len(self.token_to_id)
            self.token_to_id[token] = token_id
            self.id_to_token[token_id] = token

    def tokenize_timeline_events(
        self, events: List[DiscreteEvent], agents: Dict[str, Agent]
    ) -> List[EventToken]:
        """Tokenize a sequence of timeline events"""
        tokens = []

        # Add sequence start token
        start_token = EventToken(
            token_id="[CLS]",
            token_type=TokenType.SEQUENCE_START,
            timestamp=(
                min(event.timestamp for event in events) if events else datetime.now()
            ),
            embedding=self.get_embedding("[CLS]"),
        )
        tokens.append(start_token)

        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        for i, event in enumerate(sorted_events):
            # Create main event token
            event_token = self._create_event_token(event, agents, i, sorted_events)
            tokens.append(event_token)

            # Create actor tokens for each participating agent
            for actor_id in event.actors:
                if actor_id in agents:
                    actor_token = self._create_actor_token(
                        event, agents[actor_id], i, sorted_events
                    )
                    tokens.append(actor_token)

        # Add sequence end token
        end_token = EventToken(
            token_id="[SEP]",
            token_type=TokenType.SEQUENCE_END,
            timestamp=(
                max(event.timestamp for event in events) if events else datetime.now()
            ),
            embedding=self.get_embedding("[SEP]"),
        )
        tokens.append(end_token)

        return tokens

    def _create_event_token(
        self,
        event: DiscreteEvent,
        agents: Dict[str, Agent],
        position: int,
        all_events: List[DiscreteEvent],
    ) -> EventToken:
        """Create a token for a discrete event"""
        # Map event type to token type
        token_type_mapping = {
            EventType.COMMUNICATION: TokenType.ACTION_COMMUNICATION,
            EventType.TRANSACTION: TokenType.ACTION_TRANSACTION,
            EventType.DECISION: TokenType.ACTION_DECISION,
            EventType.MEETING: TokenType.ACTION_MEETING,
            EventType.ACTION: TokenType.ACTION_COMMUNICATION,  # Default
            EventType.EVIDENCE: TokenType.ENTITY_RESOURCE,
        }

        token_type = token_type_mapping.get(
            event.event_type, TokenType.ACTION_COMMUNICATION
        )
        token_id = f"event_{event.event_id}"

        # Create embedding
        embedding = self.get_embedding(token_id)

        # Determine semantic role
        semantic_role = "ROOT"  # Events are typically root nodes in dependency trees

        # Calculate contextual features
        preceding_tokens = [
            f"event_{all_events[j].event_id}"
            for j in range(max(0, position - 3), position)
        ]
        following_tokens = [
            f"event_{all_events[j].event_id}"
            for j in range(position + 1, min(len(all_events), position + 4))
        ]

        # Find concurrent events (same timestamp)
        concurrent_tokens = [
            f"event_{e.event_id}"
            for e in all_events
            if e.timestamp == event.timestamp and e.event_id != event.event_id
        ]

        # Calculate MMO relevance scores
        motive_relevance = self._calculate_motive_relevance(event, agents)
        means_relevance = self._calculate_means_relevance(event, agents)
        opportunity_relevance = self._calculate_opportunity_relevance(event, agents)

        return EventToken(
            token_id=token_id,
            token_type=token_type,
            timestamp=event.timestamp,
            embedding=embedding,
            semantic_role=semantic_role,
            dependency_relation="ROOT",
            named_entity_type="EVENT",
            evidence_strength=1.0,  # Could be calculated from evidence quality
            motive_relevance=motive_relevance,
            means_relevance=means_relevance,
            opportunity_relevance=opportunity_relevance,
            preceding_tokens=preceding_tokens,
            following_tokens=following_tokens,
            concurrent_tokens=concurrent_tokens,
            metadata={
                "event_type": event.event_type.value,
                "description": event.description,
                "actors": event.actors,
                "evidence_refs": event.evidence_refs,
            },
        )

    def _create_actor_token(
        self,
        event: DiscreteEvent,
        agent: Agent,
        position: int,
        all_events: List[DiscreteEvent],
    ) -> EventToken:
        """Create a token for an agent participating in an event"""
        token_id = f"agent_{agent.agent_id}_in_{event.event_id}"

        embedding = self.get_embedding(token_id)

        # Determine agent's role in the event
        semantic_role = self._determine_agent_semantic_role(agent, event)

        return EventToken(
            token_id=token_id,
            token_type=TokenType.ENTITY_AGENT,
            timestamp=event.timestamp,
            embedding=embedding,
            semantic_role=semantic_role,
            dependency_relation="nsubj" if semantic_role == "Subject" else "dobj",
            named_entity_type=(
                "PERSON" if agent.agent_type == AgentType.INDIVIDUAL else "ORG"
            ),
            agent_perspective=agent.agent_id,
            evidence_strength=1.0,
            metadata={
                "agent_name": agent.name,
                "agent_type": agent.agent_type.value,
                "event_participation": True,
            },
        )

    def _calculate_motive_relevance(
        self, event: DiscreteEvent, agents: Dict[str, Agent]
    ) -> float:
        """Calculate how relevant an event is to motive analysis"""
        relevance = 0.0

        # Financial events have high motive relevance
        if event.event_type in [EventType.TRANSACTION]:
            relevance += 0.8

        # Communication events have moderate relevance
        if event.event_type == EventType.COMMUNICATION:
            relevance += 0.4

        # Events with specific motive analysis
        if event.motive_analysis:
            relevance += 0.6

        return min(relevance, 1.0)

    def _calculate_means_relevance(
        self, event: DiscreteEvent, agents: Dict[str, Agent]
    ) -> float:
        """Calculate how relevant an event is to means analysis"""
        relevance = 0.0

        # Decision and action events have high means relevance
        if event.event_type in [EventType.DECISION, EventType.ACTION]:
            relevance += 0.7

        # Events with means analysis
        if event.means_analysis:
            relevance += 0.6

        return min(relevance, 1.0)

    def _calculate_opportunity_relevance(
        self, event: DiscreteEvent, agents: Dict[str, Agent]
    ) -> float:
        """Calculate how relevant an event is to opportunity analysis"""
        relevance = 0.0

        # Meeting events create opportunities
        if event.event_type == EventType.MEETING:
            relevance += 0.8

        # Multiple actors create opportunities
        if len(event.actors) > 1:
            relevance += 0.5

        # Events with opportunity analysis
        if event.opportunity_analysis:
            relevance += 0.6

        return min(relevance, 1.0)

    def _determine_agent_semantic_role(self, agent: Agent, event: DiscreteEvent) -> str:
        """Determine the semantic role of an agent in an event"""
        # Simple heuristic - first actor is subject, others are objects
        if event.actors and event.actors[0] == agent.agent_id:
            return "Subject"
        else:
            return "Object"

    def get_embedding(self, token: str) -> np.ndarray:
        """Get embedding vector for a token"""
        if token in self.token_to_id:
            token_id = self.token_to_id[token]
        else:
            # Add new token to vocabulary if space available
            if len(self.token_to_id) < self.vocab_size:
                token_id = len(self.token_to_id)
                self.token_to_id[token] = token_id
                self.id_to_token[token_id] = token
            else:
                # Use unknown token
                token_id = self.token_to_id["[UNK]"]

        return self.embedding_matrix[token_id].copy()


class LLMTransformerSchema:
    """
    Main LLM/Transformer schema that integrates with HyperGNN framework
    Maps agent perspectives to attention heads and processes timeline sequences
    """

    def __init__(
        self,
        case_id: str,
        num_layers: int = 6,
        embed_dim: int = 512,
        num_heads: int = 8,
    ):
        self.case_id = case_id
        self.num_layers = num_layers
        self.embed_dim = embed_dim
        self.num_heads = num_heads

        # Core components
        self.tokenizer = TimelineTokenizer(embed_dim=embed_dim)
        self.attention_heads: Dict[str, AttentionHead] = {}
        self.transformer_blocks: List[TransformerBlock] = []

        # Agent-to-head mappings
        self.agent_to_head: Dict[str, str] = {}
        self.head_to_agent: Dict[str, str] = {}

        # Timeline processing
        self.tokenized_timeline: List[EventToken] = []
        self.attention_matrices: Dict[str, np.ndarray] = {}
        # Cross-attention matrices
        self.cross_attention_matrices: Dict[str, np.ndarray] = {}

        # Initialize transformer blocks
        self._initialize_transformer_blocks()

    def _initialize_transformer_blocks(self):
        """Initialize transformer blocks"""
        for layer_idx in range(self.num_layers):
            block = TransformerBlock(
                block_id=f"block_{layer_idx}",
                attention_heads=[],
                num_heads=self.num_heads,
                embed_dim=self.embed_dim,
            )
            self.transformer_blocks.append(block)

    def create_attention_head_for_agent(
        self, agent: Agent, perspective: str = "default"
    ) -> AttentionHead:
        """Create an attention head for an agent's perspective"""
        head_id = f"head_{agent.agent_id}_{perspective}"

        # Initialize attention weights
        head_dim = self.embed_dim // self.num_heads
        query_weights = np.random.randn(self.embed_dim, head_dim) * 0.1
        key_weights = np.random.randn(self.embed_dim, head_dim) * 0.1
        value_weights = np.random.randn(self.embed_dim, head_dim) * 0.1

        # Determine focus token types based on agent type and perspective
        focus_token_types = self._determine_focus_tokens(agent, perspective)

        # Create relationship bias based on agent connections
        relationship_bias = self._create_relationship_bias(agent)

        attention_head = AttentionHead(
            head_id=head_id,
            agent_id=agent.agent_id,
            agent_perspective=perspective,
            query_weights=query_weights,
            key_weights=key_weights,
            value_weights=value_weights,
            focus_token_types=focus_token_types,
            relationship_bias=relationship_bias,
            metadata={
                "agent_name": agent.name,
                "agent_type": agent.agent_type.value,
                "creation_timestamp": datetime.now().isoformat(),
            },
        )

        self.attention_heads[head_id] = attention_head
        self.agent_to_head[agent.agent_id] = head_id
        self.head_to_agent[head_id] = agent.agent_id

        return attention_head

    def _determine_focus_tokens(self, agent: Agent, perspective: str) -> Set[TokenType]:
        """Determine which token types an agent's perspective should focus on"""
        focus_tokens = set()

        # Base focus tokens for all agents
        focus_tokens.add(TokenType.ENTITY_AGENT)
        focus_tokens.add(TokenType.ACTION_COMMUNICATION)

        # Perspective-specific focus
        if perspective == "victim":
            focus_tokens.update(
                [
                    TokenType.ACTION_TRANSACTION,
                    TokenType.MODIFIER_INTENSITY,
                    TokenType.CONNECTION_CAUSAL,
                ]
            )
        elif perspective == "perpetrator":
            focus_tokens.update(
                [
                    TokenType.ACTION_DECISION,
                    TokenType.CONNECTION_TEMPORAL,
                    TokenType.MODIFIER_RELATIONSHIP,
                ]
            )
        elif perspective == "witness":
            focus_tokens.update(
                [
                    TokenType.ACTION_MEETING,
                    TokenType.MODIFIER_TEMPORAL,
                    TokenType.CONNECTION_SPATIAL,
                ]
            )
        elif perspective == "investigator":
            focus_tokens.update(
                [
                    TokenType.ENTITY_RESOURCE,
                    TokenType.CONNECTION_CAUSAL,
                    TokenType.ACTION_DECISION,
                ]
            )

        return focus_tokens

    def _create_relationship_bias(self, agent: Agent) -> Dict[str, float]:
        """Create relationship bias for attention computation"""
        bias = {}

        # Strong bias towards professional connections
        for prof_link in agent.professional_links:
            bias[prof_link] = 0.8

        # Moderate bias towards social connections
        for social_link in agent.social_links:
            bias[social_link] = 0.4

        return bias

    def process_timeline_with_attention(
        self, events: List[DiscreteEvent], agents: Dict[str, Agent]
    ) -> Dict[str, Any]:
        """Process timeline events using transformer attention mechanisms"""

        # Tokenize timeline
        self.tokenized_timeline = self.tokenizer.tokenize_timeline_events(
            events, agents
        )

        # Create attention heads for each agent
        for agent in agents.values():
            if agent.agent_id not in self.agent_to_head:
                self.create_attention_head_for_agent(agent)

        # Compute self-attention for each agent perspective
        self_attention_results = {}
        for head_id, attention_head in self.attention_heads.items():
            attention_matrix = self._compute_self_attention(attention_head)
            self.attention_matrices[head_id] = attention_matrix
            self_attention_results[head_id] = self._analyze_attention_patterns(
                attention_matrix
            )

        # Compute cross-attention between agent perspectives
        cross_attention_results = {}
        agent_heads = list(self.attention_heads.keys())
        for i, head1_id in enumerate(agent_heads):
            for head2_id in agent_heads[i + 1 :]:
                if head1_id != head2_id:
                    cross_attention_matrix = self._compute_cross_attention(
                        self.attention_heads[head1_id], self.attention_heads[head2_id]
                    )
                    key_str = f"{head1_id}_vs_{head2_id}"  # Convert tuple to string
                    self.cross_attention_matrices[key_str] = cross_attention_matrix
                    cross_attention_results[key_str] = (
                        self._analyze_cross_attention_patterns(
                            cross_attention_matrix, head1_id, head2_id
                        )
                    )

        return {
            "tokenized_sequence_length": len(self.tokenized_timeline),
            "attention_heads": len(self.attention_heads),
            "self_attention_analysis": self_attention_results,
            "cross_attention_analysis": cross_attention_results,
            "perspective_correlations": self._compute_perspective_correlations(),
            "timeline_insights": self._extract_timeline_insights(),
        }

    def _compute_self_attention(self, attention_head: AttentionHead) -> np.ndarray:
        """Compute self-attention for a specific agent perspective"""
        sequence_length = len(self.tokenized_timeline)

        if sequence_length == 0:
            return np.array([])

        # Create input matrix from token embeddings
        input_matrix = np.stack([token.embedding for token in self.tokenized_timeline])

        # Compute queries, keys, and values
        queries = input_matrix @ attention_head.query_weights
        keys = input_matrix @ attention_head.key_weights
        values = input_matrix @ attention_head.value_weights

        # Compute attention scores
        attention_scores = queries @ keys.T

        # Apply scaling
        head_dim = attention_head.query_weights.shape[1]
        attention_scores = attention_scores / np.sqrt(head_dim)

        # Apply attention mask and perspective bias
        for i, token in enumerate(self.tokenized_timeline):
            if not token.attention_mask:
                attention_scores[i, :] = -np.inf
                attention_scores[:, i] = -np.inf

            # Apply token type focus
            if token.token_type not in attention_head.focus_token_types:
                attention_scores[i, :] *= 0.5  # Reduce attention to unfocused tokens

            # Apply relationship bias
            if token.agent_perspective in attention_head.relationship_bias:
                bias = attention_head.relationship_bias[token.agent_perspective]
                attention_scores[i, :] *= 1.0 + bias

        # Apply softmax to get attention weights
        attention_weights = self._softmax(attention_scores)

        return attention_weights

    def _compute_cross_attention(
        self, head1: AttentionHead, head2: AttentionHead
    ) -> np.ndarray:
        """Compute cross-attention between two agent perspectives"""
        sequence_length = len(self.tokenized_timeline)

        if sequence_length == 0:
            return np.array([])

        input_matrix = np.stack([token.embedding for token in self.tokenized_timeline])

        # Queries from head1, keys and values from head2
        queries = input_matrix @ head1.query_weights
        keys = input_matrix @ head2.key_weights
        values = input_matrix @ head2.value_weights

        # Compute attention scores
        attention_scores = queries @ keys.T

        # Apply scaling
        head_dim = head1.query_weights.shape[1]
        attention_scores = attention_scores / np.sqrt(head_dim)

        # Apply cross-perspective bias
        for i, token in enumerate(self.tokenized_timeline):
            # Boost attention between tokens from different perspectives
            if (
                token.agent_perspective == head1.agent_id
                or token.agent_perspective == head2.agent_id
            ):
                attention_scores[i, :] *= 1.2

        # Apply softmax
        attention_weights = self._softmax(attention_scores)

        return attention_weights

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Compute softmax activation"""
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    def _analyze_attention_patterns(
        self, attention_matrix: np.ndarray
    ) -> Dict[str, Any]:
        """Analyze patterns in attention matrix"""
        if attention_matrix.size == 0:
            return {"status": "no_data"}

        return {
            "max_attention_score": float(np.max(attention_matrix)),
            "min_attention_score": float(np.min(attention_matrix)),
            "attention_entropy": self._compute_attention_entropy(attention_matrix),
            "focus_distribution": self._compute_focus_distribution(attention_matrix),
            "temporal_attention_pattern": self._analyze_temporal_attention(
                attention_matrix
            ),
        }

    def _analyze_cross_attention_patterns(
        self, attention_matrix: np.ndarray, head1_id: str, head2_id: str
    ) -> Dict[str, Any]:
        """Analyze cross-attention patterns between two perspectives"""
        if attention_matrix.size == 0:
            return {"status": "no_data"}

        agent1_id = self.head_to_agent[head1_id]
        agent2_id = self.head_to_agent[head2_id]

        return {
            "perspective_correlation": float(np.mean(attention_matrix)),
            "mutual_focus_strength": self._compute_mutual_focus(attention_matrix),
            "agreement_score": self._compute_perspective_agreement(attention_matrix),
            "conflict_indicators": self._detect_perspective_conflicts(attention_matrix),
            "agent_pair": (agent1_id, agent2_id),
        }

    def _compute_attention_entropy(self, attention_matrix: np.ndarray) -> float:
        """Compute entropy of attention distribution"""
        # Flatten and normalize
        flattened = attention_matrix.flatten()
        flattened = flattened + 1e-8  # Avoid log(0)
        flattened = flattened / np.sum(flattened)

        # Compute entropy
        entropy = -np.sum(flattened * np.log(flattened))
        return float(entropy)

    def _compute_focus_distribution(
        self, attention_matrix: np.ndarray
    ) -> Dict[str, float]:
        """Compute how attention is distributed across different token types"""
        distribution = {}

        for token_type in TokenType:
            relevant_indices = [
                i
                for i, token in enumerate(self.tokenized_timeline)
                if token.token_type == token_type
            ]

            if relevant_indices:
                type_attention = np.mean(
                    [attention_matrix[i, :].sum() for i in relevant_indices]
                )
                distribution[token_type.value] = float(type_attention)

        return distribution

    def _analyze_temporal_attention(
        self, attention_matrix: np.ndarray
    ) -> Dict[str, Any]:
        """Analyze how attention varies over time in the sequence"""
        sequence_length = len(self.tokenized_timeline)

        if sequence_length < 3:
            return {"status": "insufficient_data"}

        # Compute attention strength at different temporal positions
        early_attention = np.mean(attention_matrix[: sequence_length // 3, :])
        middle_attention = np.mean(
            attention_matrix[sequence_length // 3 : 2 * sequence_length // 3, :]
        )
        late_attention = np.mean(attention_matrix[2 * sequence_length // 3 :, :])

        return {
            "early_period_focus": float(early_attention),
            "middle_period_focus": float(middle_attention),
            "late_period_focus": float(late_attention),
            "temporal_consistency": float(
                np.std([early_attention, middle_attention, late_attention])
            ),
        }

    def _compute_mutual_focus(self, cross_attention_matrix: np.ndarray) -> float:
        """Compute mutual focus strength between perspectives"""
        return float(np.mean(cross_attention_matrix * cross_attention_matrix.T))

    def _compute_perspective_agreement(
        self, cross_attention_matrix: np.ndarray
    ) -> float:
        """Compute agreement score between perspectives"""
        # High agreement when both perspectives attend to similar tokens
        diagonal_strength = np.mean(np.diag(cross_attention_matrix))
        return float(diagonal_strength)

    def _detect_perspective_conflicts(
        self, cross_attention_matrix: np.ndarray
    ) -> List[Dict[str, Any]]:
        """Detect conflicts between perspectives"""
        conflicts = []

        # Look for opposing attention patterns
        diff_matrix = cross_attention_matrix - cross_attention_matrix.T
        high_diff_indices = np.where(np.abs(diff_matrix) > 0.5)

        for i, j in zip(high_diff_indices[0], high_diff_indices[1]):
            if i < len(self.tokenized_timeline) and j < len(self.tokenized_timeline):
                conflicts.append(
                    {
                        "token_i": self.tokenized_timeline[i].token_id,
                        "token_j": self.tokenized_timeline[j].token_id,
                        "attention_difference": float(diff_matrix[i, j]),
                        "conflict_type": "attention_asymmetry",
                    }
                )

        return conflicts[:10]  # Limit to top 10 conflicts

    def _compute_perspective_correlations(self) -> Dict[str, float]:
        """Compute correlations between different agent perspectives"""
        correlations = {}

        for key_str, cross_attention in self.cross_attention_matrices.items():
            if cross_attention.size > 0:
                correlation = np.corrcoef(
                    cross_attention.flatten(), cross_attention.T.flatten()
                )[0, 1]

                correlations[key_str] = (
                    float(correlation) if not np.isnan(correlation) else 0.0
                )

        return correlations

    def _extract_timeline_insights(self) -> Dict[str, Any]:
        """Extract insights from the timeline analysis"""
        insights = {
            "most_attended_tokens": [],
            "perspective_divergences": [],
            "temporal_focus_shifts": [],
            "mmo_attention_distribution": {},
        }

        # Find most attended tokens across all perspectives
        if self.attention_matrices:
            combined_attention = np.zeros(
                (len(self.tokenized_timeline), len(self.tokenized_timeline))
            )
            for attention_matrix in self.attention_matrices.values():
                if attention_matrix.size > 0:
                    combined_attention += attention_matrix

            # Get top attended tokens
            attention_sums = np.sum(combined_attention, axis=1)
            top_indices = np.argsort(attention_sums)[-5:][::-1]

            for idx in top_indices:
                if idx < len(self.tokenized_timeline):
                    token = self.tokenized_timeline[idx]
                    insights["most_attended_tokens"].append(
                        {
                            "token_id": token.token_id,
                            "token_type": token.token_type.value,
                            "attention_score": float(attention_sums[idx]),
                            "timestamp": token.timestamp.isoformat(),
                        }
                    )

        # Analyze MMO attention distribution
        mmo_categories = [
            "motive_relevance",
            "means_relevance",
            "opportunity_relevance",
        ]
        for category in mmo_categories:
            category_attention = 0.0
            category_count = 0

            for token in self.tokenized_timeline:
                relevance = getattr(token, category, 0.0)
                if relevance > 0:
                    category_attention += relevance
                    category_count += 1

            if category_count > 0:
                insights["mmo_attention_distribution"][category] = (
                    category_attention / category_count
                )

        return insights

    def export_transformer_analysis(self) -> Dict[str, Any]:
        """Export comprehensive transformer analysis"""
        return {
            "case_id": self.case_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "transformer_config": {
                "num_layers": self.num_layers,
                "embed_dim": self.embed_dim,
                "num_heads": self.num_heads,
                "vocab_size": self.tokenizer.vocab_size,
            },
            "attention_heads": {
                head_id: {
                    "agent_id": head.agent_id,
                    "agent_perspective": head.agent_perspective,
                    "focus_token_types": [t.value for t in head.focus_token_types],
                    "relationship_bias_count": len(head.relationship_bias),
                }
                for head_id, head in self.attention_heads.items()
            },
            "timeline_analysis": {
                "total_tokens": len(self.tokenized_timeline),
                "token_type_distribution": self._get_token_type_distribution(),
                "attention_matrices_computed": len(self.attention_matrices),
                "cross_attention_pairs": len(self.cross_attention_matrices),
            },
            "perspective_insights": self._compute_perspective_correlations(),
            "timeline_insights": (
                self._extract_timeline_insights()
                if hasattr(self, "attention_matrices")
                else {}
            ),
        }

    def _get_token_type_distribution(self) -> Dict[str, int]:
        """Get distribution of token types in the timeline"""
        distribution = {}
        for token in self.tokenized_timeline:
            token_type = token.token_type.value
            distribution[token_type] = distribution.get(token_type, 0) + 1
        return distribution


def create_sample_transformer_schema() -> LLMTransformerSchema:
    """Create a sample transformer schema for demonstration"""
    from hypergnn_core import create_sample_framework

    # Get sample framework
    hypergnn_framework = create_sample_framework()

    # Create transformer schema
    transformer_schema = LLMTransformerSchema(
        case_id=hypergnn_framework.case_id,
        num_layers=4,
        embed_dim=256,  # Smaller for demo
        num_heads=4,
    )

    # Process the timeline with transformer attention
    events = list(hypergnn_framework.events.values())
    agents = hypergnn_framework.agents

    if events and agents:
        analysis = transformer_schema.process_timeline_with_attention(events, agents)
        print("Transformer Analysis Results:")
        print(json.dumps(analysis, indent=2, default=str))

    return transformer_schema


if __name__ == "__main__":
    # Demonstrate transformer schema capabilities
    schema = create_sample_transformer_schema()
    report = schema.export_transformer_analysis()
    print("\nTransformer Schema Export:")
    print(json.dumps(report, indent=2, default=str))
