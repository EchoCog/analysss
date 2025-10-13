# LLM/Transformer Schema for HyperGNN Framework

## Overview

This document describes the LLM/Transformer schema extension to the HyperGNN Framework that maps agent perspectives to attention heads and tokenizes timeline events using NLP-style features. This enables sophisticated analysis of multi-agent interactions through transformer attention mechanisms.

## Core Concept

The transformer schema creates a bridge between investigative case analysis and modern NLP techniques by:

1. **Agent Perspectives → Attention Heads**: Each agent's viewpoint becomes a specialized attention head that focuses on relevant aspects of the timeline
2. **Timeline Events → Tokens**: Events are tokenized with features analogous to parts of speech, enabling sequence analysis
3. **Self-Attention**: Analyzes how each agent's perspective correlates with different parts of the timeline
4. **Cross-Attention**: Compares different agent perspectives to identify agreements, conflicts, and correlations

## Architecture Components

### 1. TokenType Enum

Defines token types analogous to parts of speech in NLP:

```python
class TokenType(Enum):
    # Action tokens (like verbs)
    ACTION_COMMUNICATION = "action_communication"
    ACTION_TRANSACTION = "action_transaction"
    ACTION_DECISION = "action_decision"
    ACTION_MEETING = "action_meeting"
    
    # Entity tokens (like nouns)
    ENTITY_AGENT = "entity_agent"
    ENTITY_RESOURCE = "entity_resource"
    ENTITY_LOCATION = "entity_location"
    
    # Modifier tokens (like adjectives/adverbs)
    MODIFIER_TEMPORAL = "modifier_temporal"
    MODIFIER_INTENSITY = "modifier_intensity"
    MODIFIER_RELATIONSHIP = "modifier_relationship"
    
    # Connection tokens (like prepositions/conjunctions)
    CONNECTION_CAUSAL = "connection_causal"
    CONNECTION_TEMPORAL = "connection_temporal"
    CONNECTION_SPATIAL = "connection_spatial"
    
    # Special tokens
    SEQUENCE_START = "sequence_start"  # [CLS] equivalent
    SEQUENCE_END = "sequence_end"      # [SEP] equivalent
    PADDING = "padding"               # [PAD] equivalent
    UNKNOWN = "unknown"               # [UNK] equivalent
```

### 2. EventToken Class

Represents a tokenized timeline event with rich features:

```python
@dataclass
class EventToken:
    token_id: str
    token_type: TokenType
    timestamp: datetime
    embedding: np.ndarray
    attention_mask: bool = True
    
    # POS-style linguistic features
    semantic_role: str = ""           # Subject, Object, Predicate
    dependency_relation: str = ""     # ROOT, compound, nmod
    named_entity_type: str = ""       # PERSON, ORG, DATE
    
    # Domain-specific investigative features
    agent_perspective: str = ""       # Which agent's perspective
    evidence_strength: float = 1.0    # Confidence/reliability
    motive_relevance: float = 0.0     # MMO framework integration
    means_relevance: float = 0.0
    opportunity_relevance: float = 0.0
    
    # Contextual sequence features
    preceding_tokens: List[str] = field(default_factory=list)
    following_tokens: List[str] = field(default_factory=list)
    concurrent_tokens: List[str] = field(default_factory=list)
```

### 3. AttentionHead Class

Maps agent perspectives to transformer attention mechanisms:

```python
@dataclass
class AttentionHead:
    head_id: str
    agent_id: str
    agent_perspective: str  # "victim", "perpetrator", "witness", etc.
    
    # Standard transformer attention weights
    query_weights: np.ndarray
    key_weights: np.ndarray
    value_weights: np.ndarray
    
    # Perspective-specific configuration
    focus_token_types: Set[TokenType]     # What this perspective focuses on
    temporal_window: Optional[Tuple[datetime, datetime]]  # Time constraints
    relationship_bias: Dict[str, float]   # Bias toward related agents
    
    # Learned attention patterns
    attention_patterns: Dict[str, np.ndarray]
    bias_vector: np.ndarray
```

### 4. LLMTransformerSchema Class

Main orchestrator that integrates with HyperGNN framework:

```python
class LLMTransformerSchema:
    def __init__(self, case_id: str, num_layers: int = 6, 
                 embed_dim: int = 512, num_heads: int = 8):
        # Core transformer configuration
        # Timeline tokenization
        # Agent-to-head mappings
        # Attention computation engines
```

## Key Features

### Agent Perspective Mapping

Each agent type gets specialized attention focus:

- **Victim Perspective**: Focuses on transactions, intensity modifiers, causal connections
- **Perpetrator Perspective**: Focuses on decisions, temporal connections, relationships
- **Witness Perspective**: Focuses on meetings, temporal modifiers, spatial connections
- **Investigator Perspective**: Focuses on resources, causal connections, decisions

### Timeline Tokenization Process

1. **Event Parsing**: Convert DiscreteEvent objects into EventTokens
2. **Feature Extraction**: Calculate MMO relevance, semantic roles, dependencies
3. **Sequence Formation**: Add special tokens ([CLS], [SEP]) and create attention masks
4. **Contextual Enrichment**: Link tokens with preceding/following/concurrent context

### Attention Mechanisms

#### Self-Attention
Each agent perspective analyzes the timeline sequence:
```python
attention_scores = queries @ keys.T / sqrt(head_dim)
attention_weights = softmax(attention_scores + bias)
```

#### Cross-Attention
Compare different agent perspectives:
```python
# Queries from Agent A, Keys/Values from Agent B
cross_attention = softmax(Q_A @ K_B.T / sqrt(head_dim))
```

### MMO Framework Integration

The transformer schema enhances Motive, Means, Opportunity analysis:

- **Motive Relevance**: Transaction events get high scores, communications moderate
- **Means Relevance**: Decision and action events get high scores
- **Opportunity Relevance**: Meeting events and multi-actor events get high scores

## Usage Examples

### Basic Setup

```python
from frameworks.hypergnn_core import HyperGNNFramework
from frameworks.llm_transformer_schema import LLMTransformerSchema

# Create frameworks
hypergnn = HyperGNNFramework("case_001")
transformer = LLMTransformerSchema("case_001", embed_dim=512, num_heads=8)

# Add agents with different perspectives
victim = Agent("victim_001", AgentType.INDIVIDUAL, "Alice")
perpetrator = Agent("perp_001", AgentType.INDIVIDUAL, "Bob")

hypergnn.add_agent(victim)
hypergnn.add_agent(perpetrator)

# Create specialized attention heads
transformer.create_attention_head_for_agent(victim, "victim")
transformer.create_attention_head_for_agent(perpetrator, "perpetrator")
```

### Timeline Analysis

```python
# Add events to timeline
events = [
    DiscreteEvent("contact", datetime.now(), EventType.COMMUNICATION, 
                 ["victim_001", "perp_001"], "Initial contact"),
    DiscreteEvent("transaction", datetime.now() + timedelta(days=1), 
                 EventType.TRANSACTION, ["perp_001"], "Financial transfer"),
    # ... more events
]

for event in events:
    hypergnn.add_event(event)

# Run transformer analysis
analysis = transformer.process_timeline_with_attention(
    list(hypergnn.events.values()), 
    hypergnn.agents
)
```

### Analysis Results

The transformer analysis provides:

```python
{
    "tokenized_sequence_length": 15,
    "attention_heads": 2,
    "self_attention_analysis": {
        "head_victim_001_victim": {
            "max_attention_score": 0.85,
            "attention_entropy": 2.3,
            "focus_distribution": {...},
            "temporal_attention_pattern": {...}
        }
    },
    "cross_attention_analysis": {
        "victim_vs_perpetrator": {
            "perspective_correlation": 0.42,
            "mutual_focus_strength": 0.31,
            "agreement_score": 0.28,
            "conflict_indicators": [...]
        }
    },
    "perspective_correlations": {...},
    "timeline_insights": {...}
}
```

## Integration with HyperGNN

The transformer schema integrates seamlessly with existing HyperGNN components:

### 1. Agent Integration
- Transforms HyperGNN Agents into attention heads
- Preserves professional/social link information as relationship bias
- Maps agent types to appropriate perspective configurations

### 2. Event Integration
- Converts DiscreteEvents into EventTokens
- Preserves evidence references and MMO analysis
- Maintains temporal ordering and actor relationships

### 3. Analysis Enhancement
- Provides attention-weighted MMO analysis
- Validates deception patterns with cross-attention
- Generates perspective correlation insights

## Advanced Features

### 1. Temporal Attention Patterns
Analyzes how attention changes over time:
- Early period focus
- Middle period focus  
- Late period focus
- Temporal consistency metrics

### 2. Conflict Detection
Identifies conflicting perspectives:
- Attention asymmetries between agents
- Disagreement on event importance
- Perspective divergence indicators

### 3. Evidence Correlation
Links attention patterns to evidence strength:
- High-attention events with strong evidence
- Low-attention events requiring investigation
- Evidence gaps highlighted by attention patterns

## Performance Considerations

### Memory Usage
- Attention matrices: O(sequence_length²) per head
- Token embeddings: O(sequence_length × embed_dim)
- Cross-attention: O(num_heads²) additional matrices

### Computational Complexity
- Self-attention: O(n²d) where n=sequence length, d=embed dimension
- Cross-attention: O(h²n²d) where h=number of heads
- Total: O(Lh²n²d) where L=number of layers

### Optimization Strategies
- Use smaller embed dimensions for large cases
- Implement attention dropout to prevent overfitting
- Cache attention matrices for repeated analysis
- Use sparse attention for very long sequences

## Testing and Validation

The schema includes comprehensive tests:

```bash
# Run all transformer tests
python3 test_transformer_schema.py

# Run integration demonstration
python3 hypergnn_transformer_integration.py
```

### Test Coverage
- ✓ Token creation and properties
- ✓ Attention head configuration
- ✓ Timeline tokenization accuracy
- ✓ Self-attention computation
- ✓ Cross-attention mechanisms
- ✓ MMO relevance calculations
- ✓ Full integration pipeline

## Future Enhancements

### 1. Pre-trained Embeddings
- Integrate legal domain word embeddings
- Use case-specific vocabulary training
- Transfer learning from similar cases

### 2. Advanced Attention Patterns
- Implement sparse attention for efficiency
- Add hierarchical attention for multi-scale analysis
- Develop causal attention for temporal dependencies

### 3. Multi-modal Integration
- Image/document attention for evidence analysis
- Audio/video timeline integration
- Cross-modal attention mechanisms

### 4. Interpretability Tools
- Attention visualization dashboards
- Perspective conflict heatmaps
- Timeline attention flow diagrams

## Conclusion

The LLM/Transformer schema provides a powerful extension to the HyperGNN framework, enabling sophisticated multi-perspective analysis of complex investigative cases. By mapping agent viewpoints to attention heads and treating timeline events as linguistic tokens, we can leverage the full power of transformer architectures for case analysis while maintaining the professional investigative standards of the HyperGNN framework.

This approach opens new possibilities for:
- Automated perspective conflict detection
- Evidence-guided attention weighting
- Cross-case pattern recognition
- Predictive timeline analysis

The schema is designed to be extensible, efficient, and fully integrated with existing HyperGNN workflows, making it a valuable addition to any comprehensive case analysis toolkit.