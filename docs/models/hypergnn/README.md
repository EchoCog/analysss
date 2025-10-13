# HyperGNN Framework Documentation

## Overview

The HyperGNN (Hypergraph Neural Network) Framework is an advanced multi-layer network
modeling system designed for complex case analysis with timeline tensor integration.

## Core Components

### Agent Modeling
- Multi-dimensional agent representation
- Agent type classification (individual, organization, entity)
- Attribute tracking and evolution
- Behavioral pattern analysis

### Hypergraph Network
- Node and hyperedge construction
- Multi-way relationship modeling
- Network topology analysis
- Relationship strength computation

### Knowledge Tensors
- Multi-dimensional knowledge representation
- Temporal knowledge tracking
- Knowledge gap identification
- Evidence-knowledge mapping

### Timeline Integration
- Event-agent relationship tracking
- Temporal sequence analysis
- Critical path identification
- Timeline tensor generation

## Implementation Files

**Core Framework:**
- `frameworks/hypergnn_core_enhanced.py` - Enhanced framework implementation
- `src/api/hypergnn_core.py` - API integration layer
- `frameworks/hypergraph_model.py` - Hypergraph modeling

**Supporting Code:**
- `src/models/hypergnn_framework_improved.py` - Improved framework
- `src/simulations/hypergnn_case_integration.py` - Case integration

## Usage

### Basic Usage

```python
from frameworks.hypergnn_core import HyperGNNFramework

# Initialize framework
framework = HyperGNNFramework(case_id="case_001")

# Add agents
framework.add_agent(agent)

# Add events
framework.add_event(event)

# Generate analysis
results = framework.analyze()
```

### Advanced Features

```python
# Knowledge tensor generation
tensors = framework.generate_knowledge_tensors()

# Hypergraph construction
hypergraph = framework.build_hypergraph()

# Timeline integration
framework.integrate_timeline(timeline_entries)
```

## Documentation

- [HYPERGNN_COMPREHENSIVE_SCHEMA.md](../../../HYPERGNN_COMPREHENSIVE_SCHEMA.md) - Comprehensive schema
- [CASE_HYPERGRAPH_DOCUMENTATION.md](../../../CASE_HYPERGRAPH_DOCUMENTATION.md) - Case hypergraph docs

## Examples

See `examples/hypergraphql_hypergnn_integration.py` for complete examples.

## Performance

- Suitable for networks up to 10,000 nodes
- Memory usage: ~100MB per 1,000 nodes
- Analysis time: ~1-5 seconds per 1,000 nodes

## Testing

Tests located in:
- `tests/unit/test_hypergnn.py` - Unit tests
- `tests/integration/test_hypergnn_integration.py` - Integration tests
