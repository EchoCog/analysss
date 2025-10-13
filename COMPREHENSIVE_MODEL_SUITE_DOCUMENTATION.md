# Comprehensive Model Suite Documentation

## Overview

This repository implements a comprehensive suite of analytical models for complex case analysis and investigation. The suite consists of five integrated model types that work together to provide multi-dimensional insights and cross-validated analysis.

## Model Types

### 1. Agent-Based Models (HyperGNN Framework)

**Location**: `frameworks/hypergnn_core.py`

**Purpose**: Models individual agents (people, organizations) and their interactions within a complex system.

**Key Features**:
- Individual agent behavior modeling
- Social and professional relationship networks
- Multi-agent interaction simulation
- Timeline tensor state management
- Motive, means, opportunity (MMO) analysis

**Usage Example**:
```python
from frameworks.hypergnn_core import Agent, AgentType, create_sample_framework

# Create agents
agent = Agent("agent_001", AgentType.INDIVIDUAL, "John Doe")
framework = create_sample_framework()
```

**Integration Points**: 
- Provides agent definitions for all other models
- Relationship networks feed into hypergraph structures
- Behavioral patterns inform LLM attention mechanisms

### 2. Discrete Event Models

**Location**: `discrete_event_model.py`

**Purpose**: Models events as discrete occurrences in time with state transitions and knowledge tensors.

**Key Features**:
- Timeline-based event modeling
- Event state management (pending, in-progress, completed)
- Knowledge tensor generation
- Evidence tracking and requirements
- Agent state integration

**Usage Example**:
```python
from discrete_event_model import DiscreteEventModel

model = DiscreteEventModel("case_001")
# Add timeline entries and generate analysis
report = model.generate_evidence_report()
```

**Integration Points**:
- Events become nodes in hypergraph models
- Timeline provides temporal context for system dynamics
- Event sequences inform LLM tokenization

### 3. System Dynamics Models

**Location**: `frameworks/system_dynamics.py`

**Purpose**: Tracks flows and accumulations of resources, information, and influence over time.

**Key Features**:
- Stock and flow modeling
- Financial transaction tracking
- Information and influence flows
- Deception pattern detection
- Risk assessment and MMO analysis

**Usage Example**:
```python
from frameworks.system_dynamics import SystemDynamicsModel, Stock, StockType

model = SystemDynamicsModel("case_001")
stock = Stock("financial_assets", StockType.FINANCIAL, "owner", 10000.0, 
             "USD", "Financial resources", datetime.now())
model.add_stock(stock)
```

**Integration Points**:
- Financial flows inform agent motivations
- Resource levels affect hypergraph edge weights
- Flow patterns provide evidence for discrete events

### 4. Hypergraph Models

**Location**: `frameworks/hypergraph_model.py`

**Purpose**: Represents complex multi-way relationships between entities using hypergraphs where edges can connect multiple nodes simultaneously.

**Key Features**:
- Multi-way relationship modeling
- Complex network analysis (centrality, communities, cliques)
- Suspicious pattern detection
- Temporal relationship tracking
- Evidence-based relationship weighting

**Usage Example**:
```python
from frameworks.hypergraph_model import HypergraphModel, HypergraphNode, Hyperedge, HyperedgeType

model = HypergraphModel("case_001")
node = HypergraphNode("entity_001", "agent", "John Doe")
model.add_node(node)

# Multi-way relationship
hyperedge = Hyperedge("meeting_001", {"agent1", "agent2", "agent3"}, 
                     HyperedgeType.MEETING, datetime.now(), strength=0.8)
model.add_hyperedge(hyperedge)
```

**Integration Points**:
- Agents from agent-based models become nodes
- Events from discrete models create hyperedges
- Relationship strengths informed by system dynamics flows

### 5. LLM/Transformer Models

**Location**: `frameworks/llm_transformer_schema.py`

**Purpose**: Uses transformer architecture to analyze agent perspectives and timeline events through attention mechanisms.

**Key Features**:
- Agent perspective mapping to attention heads
- Timeline event tokenization
- Self-attention and cross-attention analysis
- Perspective correlation detection
- Multi-head attention for different viewpoints

**Usage Example**:
```python
from frameworks.llm_transformer_schema import LLMTransformerSchema

model = LLMTransformerSchema("case_001", embed_dim=512, num_heads=8)
# Create attention head for agent perspective
model.create_attention_head_for_agent(agent, "victim")
```

**Integration Points**:
- Agent perspectives from agent-based models
- Event sequences from discrete event models  
- Attention weights can inform relationship strengths

## Unified Integration Framework

**Location**: `unified_model_framework.py`

**Purpose**: Orchestrates all model types to work together, providing unified analysis and cross-validation.

**Key Features**:
- Unified model configuration and initialization
- Cross-model data sharing and validation
- Integrated analysis across all model types
- Pattern detection across models
- Confidence scoring and recommendations

**Usage Example**:
```python
from unified_model_framework import UnifiedModelFramework, UnifiedAnalysisConfiguration, AnalysisMode, ModelType

config = UnifiedAnalysisConfiguration(
    case_id="comprehensive_case",
    analysis_mode=AnalysisMode.COMPREHENSIVE,
    enabled_models={ModelType.AGENT_BASED, ModelType.HYPERGRAPH, ModelType.LLM_TRANSFORMER}
)

framework = UnifiedModelFramework(config)
results = framework.run_comprehensive_analysis()
```

## Model Synergies

The models are designed to complement each other:

1. **Agent-Based ↔ Hypergraph**: Agent relationships validate hypergraph structures
2. **Discrete Events ↔ System Dynamics**: Events trigger flows, flows explain event patterns  
3. **Hypergraph ↔ LLM**: Network structure informs attention patterns
4. **System Dynamics ↔ Agent-Based**: Resource flows explain agent motivations
5. **All Models ↔ Validation**: Cross-model consistency checks ensure reliability

## Testing and Validation

### Test Suite
**Location**: `test_all_models.py`

Comprehensive test suite that validates each model individually and tests integration:

```bash
python test_all_models.py
```

### Comprehensive Demonstration  
**Location**: `comprehensive_model_demo.py`

Full demonstration showing all models working together on a realistic case:

```bash
python comprehensive_model_demo.py
```

## Analysis Modes

The unified framework supports different analysis modes:

### Basic Mode
- Individual models run independently  
- No cross-validation
- Quick analysis for simple cases

### Integrated Mode
- Models share data
- Basic cross-validation
- Enhanced insights from model interactions

### Comprehensive Mode (Recommended)
- Full integration across all models
- Extensive cross-validation
- Pattern detection across models
- Confidence scoring and recommendations

### Investigative Mode
- Focus on suspicious pattern detection
- Enhanced anomaly detection
- Priority on high-risk entities and behaviors

## Configuration Options

### Model Selection
Enable/disable specific models based on case requirements:
```python
enabled_models = {
    ModelType.AGENT_BASED,      # Always recommended
    ModelType.DISCRETE_EVENT,   # For temporal analysis
    ModelType.SYSTEM_DYNAMICS,  # For resource/flow analysis
    ModelType.HYPERGRAPH,       # For complex relationships
    ModelType.LLM_TRANSFORMER   # For perspective analysis
}
```

### Analysis Parameters
- `confidence_threshold`: Minimum confidence for conclusions (default: 0.7)
- `temporal_window`: Time window for analysis (default: 365 days)
- `enable_cross_validation`: Cross-model validation (default: True)
- `enable_pattern_detection`: Suspicious pattern detection (default: True)

## Output Formats

### Summary Format
- High-level findings and recommendations
- Key metrics and confidence scores
- Priority actions

### Detailed Format  
- Individual model results
- Cross-validation results
- Detailed pattern analysis

### Comprehensive Format (Recommended)
- Complete analysis from all models
- Integration summary
- Cross-model validation
- Suspicious pattern detection
- Actionable recommendations

## Performance Considerations

### Model Complexity
- **Agent-Based**: O(n²) for n agents (relationship networks)
- **Discrete Event**: O(n log n) for n events (temporal sorting)
- **System Dynamics**: O(n) for n stocks/flows (linear processing)
- **Hypergraph**: O(n³) for n nodes (matrix operations)
- **LLM Transformer**: O(n²d) for n tokens, d dimensions (attention)

### Optimization Tips
1. **Selective Model Usage**: Enable only needed models for simple cases
2. **Temporal Windowing**: Limit analysis to relevant time periods
3. **Batch Processing**: Process multiple cases together when possible
4. **Caching**: Cache intermediate results for repeated analysis

## Use Cases

### Legal Case Analysis
- Multi-party litigation with complex relationships
- Evidence correlation across different sources
- Timeline reconstruction and validation
- Motive, means, opportunity analysis

### Financial Investigation
- Transaction flow analysis
- Relationship network mapping
- Suspicious pattern detection
- Cross-validation of evidence sources

### Corporate Investigation
- Internal relationship analysis
- Communication pattern analysis
- Resource flow tracking
- Behavioral pattern detection

### Research and Academic Applications
- Complex system modeling
- Multi-agent simulation
- Network analysis research
- Machine learning model integration

## Future Enhancements

### Planned Features
1. **Real-time Analysis**: Streaming data processing
2. **Machine Learning Integration**: Automated pattern recognition
3. **Visualization Tools**: Interactive network and timeline visualization
4. **API Endpoints**: REST API for external integration
5. **Database Integration**: Persistent storage and retrieval

### Research Directions
1. **Advanced Attention Mechanisms**: Hierarchical and sparse attention
2. **Temporal Graph Neural Networks**: Time-aware graph processing
3. **Federated Analysis**: Multi-organization collaborative analysis
4. **Explainable AI**: Better interpretability of model decisions

## Conclusion

This comprehensive model suite provides a powerful, integrated approach to complex case analysis. By combining five complementary modeling approaches, it offers:

- **Multi-dimensional Analysis**: Different perspectives on the same data
- **Cross-validation**: Enhanced confidence through model agreement
- **Pattern Detection**: Discovery of subtle relationships and anomalies
- **Scalability**: Applicable to cases of varying complexity
- **Flexibility**: Configurable for different use cases and requirements

The unified framework ensures that insights from each model inform and validate the others, providing a robust foundation for complex analytical tasks.

---

## Quick Start Guide

1. **Install Dependencies**:
   ```bash
   pip install numpy networkx torch transformers matplotlib
   ```

2. **Run Tests**:
   ```bash
   python test_all_models.py
   ```

3. **Run Demonstration**:
   ```bash
   python comprehensive_model_demo.py
   ```

4. **Create Your Own Analysis**:
   ```python
   from unified_model_framework import UnifiedModelFramework, UnifiedAnalysisConfiguration, AnalysisMode, ModelType
   
   config = UnifiedAnalysisConfiguration(
       case_id="your_case_id",
       analysis_mode=AnalysisMode.COMPREHENSIVE,
       enabled_models={ModelType.AGENT_BASED, ModelType.HYPERGRAPH}
   )
   
   framework = UnifiedModelFramework(config)
   # Add your agents, events, and data
   results = framework.run_comprehensive_analysis()
   ```

For detailed examples and advanced usage, see the demonstration files and test suite.