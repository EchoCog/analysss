# OpenCog HGNNQL Case-LLM

## Overview

The OpenCog HGNNQL Case-LLM is a comprehensive AI-powered case analysis system that combines:

1. **OpenCog-inspired Knowledge Representation**: AtomSpace for flexible knowledge graphs
2. **HGNNQL Query Language**: HyperGraph Neural Network Query Language for intuitive queries
3. **Hyper-Holmes Inference Engine**: Automated reasoning and pattern detection
4. **Super-Sleuth Introspection Trainer**: Pattern learning and lead generation
5. **Case-LLM**: Neural network-based semantic understanding

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 OpenCog HGNNQL Case-LLM                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  AtomSpace   │  │   HGNNQL     │  │  Case-LLM    │      │
│  │   (Knowledge │◄─┤   Query      │◄─┤  (Semantic   │      │
│  │    Base)     │  │   Engine     │  │   Reasoning) │      │
│  └──────┬───────┘  └──────────────┘  └──────────────┘      │
│         │                                                     │
│         │                                                     │
│  ┌──────▼─────────────────┐  ┌──────────────────────┐      │
│  │   Hyper-Holmes         │  │  Super-Sleuth        │      │
│  │   Inference Engine     │  │  Introspection       │      │
│  │   • Forward chaining   │  │  Trainer             │      │
│  │   • Backward chaining  │  │  • Pattern learning  │      │
│  │   • Pattern detection  │  │  • Lead generation   │      │
│  │   • Hypothesis gen.    │  │  • Anomaly detection │      │
│  └────────────────────────┘  └──────────────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. AtomSpace (Knowledge Representation)

The AtomSpace is an OpenCog-inspired knowledge base that stores information as atoms in a hypergraph structure.

**Atom Types:**
- `CONCEPT`: Abstract concepts and ideas
- `PREDICATE`: Properties and predicates
- `ENTITY`: Real-world entities (people, organizations)
- `EVENT`: Timeline events
- `RELATIONSHIP`: Connections between entities
- `PATTERN`: Detected patterns
- `EVIDENCE`: Evidence items
- `INFERENCE`: Inferred knowledge

**Truth Values:**
Each atom has a probabilistic truth value with:
- `strength`: Probability that the statement is true (0.0-1.0)
- `confidence`: Confidence in the strength estimate (0.0-1.0)

### 2. HGNNQL (Query Language)

HGNNQL provides a high-level query interface for case analysis.

**Query Commands:**
```sql
-- Find all entities
FIND ENTITY

-- Find events in date range
FIND EVENT WHERE timestamp > "2025-01-01"

-- Find relationships
FIND RELATIONSHIP WHERE type = "financial"

-- Link entities
LINK entity_alice TO entity_bob AS "colleagues"

-- Infer patterns
INFER pattern FROM evidence
```

**Python API:**
```python
# Query by type
entities = system.query_entities(entity_type="person")
events = system.query_events(start_date=start, end_date=end)

# Query relationships
relationships = system.query_relationships("alice", "bob")

# Execute HGNNQL
result = system.query_hgnnql("FIND ENTITY")
```

### 3. Hyper-Holmes Inference Engine

Automated reasoning system for deriving new knowledge.

**Features:**
- **Forward Chaining**: Apply rules to derive new facts
- **Backward Chaining**: Work backwards from goals to find support
- **Pattern Detection**: Identify patterns in case data
- **Hypothesis Generation**: Generate explanations for evidence
- **Anomaly Detection**: Detect unusual patterns

**Inference Rules:**
- Deduction: A→B, B→C ⇒ A→C
- Induction: Multiple instances ⇒ pattern
- Abduction: Effect observed ⇒ hypothesize cause
- Temporal: Before/after relationships
- Causal: Cause-effect relationships

**Usage:**
```python
# Run forward chaining inference
results = system.run_inference(method="forward", max_iterations=10)

# Detect patterns
patterns = system.detect_patterns()

# Generate hypotheses
hypotheses = system.generate_hypotheses(["evidence_001", "evidence_002"])
```

### 4. Super-Sleuth Introspection Trainer

Learning system that improves over time by analyzing case data.

**Pattern Categories:**
- `TEMPORAL`: Timing patterns
- `FINANCIAL`: Financial transaction patterns
- `BEHAVIORAL`: Entity behavior patterns
- `RELATIONSHIP`: Relationship patterns
- `ANOMALY`: Anomalous patterns
- `CAUSAL`: Causal relationships

**Features:**
- **Pattern Learning**: Automatically discover patterns
- **Introspection**: Analyze knowledge quality
- **Lead Generation**: Generate investigation leads
- **Confidence Calibration**: Improve confidence estimates
- **Knowledge Gap Detection**: Identify missing information

**Usage:**
```python
# Train on case data
training_summary = system.train_introspection()

# Get introspection report
report = system.introspect()

# Get investigation leads
leads = system.get_investigation_leads()

# Get learned patterns
patterns = system.get_learned_patterns()
```

### 5. Case-LLM (Neural Reasoning)

LLM-based semantic understanding and natural language interaction.

**Features:**
- **Semantic Embeddings**: Neural embeddings for atoms
- **Similarity Search**: Find semantically similar concepts
- **Natural Language QA**: Answer questions about the case
- **Context-Aware Reasoning**: Use case context for answers

**Usage:**
```python
# Ask natural language questions
response = system.ask_llm("What entities are involved in this case?")

# Find similar concepts
similar = system.find_similar_concepts("fraud", top_k=5)
```

## Installation

The OpenCog HGNNQL Case-LLM is included in the analysis repository:

```bash
# Clone the repository
git clone https://github.com/rzonedevops/analysis.git
cd analysis

# Install dependencies
pip install -e .
```

## Quick Start

### Basic Usage

```python
from frameworks.opencog_case_llm import OpenCogCaseLLM

# Initialize system
system = OpenCogCaseLLM(case_id="case_001", output_dir="./output")

# Add entities
system.add_entity("alice", "Alice Johnson", "person")
system.add_entity("company_a", "Company A", "organization")

# Add events
from datetime import datetime
system.add_event("event_001", "Meeting", datetime(2025, 1, 15), 
                participants=["alice"])

# Add relationships
system.add_relationship("alice", "company_a", "investigates")

# Add evidence
system.add_evidence("evidence_001", "Bank records", 
                   related_entities=["company_a"],
                   verification_status="verified")
```

### Query the Knowledge Base

```python
# Find entities
entities = system.query_entities(entity_type="person")

# Find events in date range
events = system.query_events(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 12, 31)
)

# Execute HGNNQL queries
result = system.query_hgnnql("FIND ENTITY")
print(f"Found {result['count']} entities")
```

### Run Analysis Pipeline

```python
# Run complete analysis
report = system.run_complete_analysis()

# The analysis includes:
# - Forward chaining inference
# - Pattern detection
# - Introspection training
# - Lead generation

print(f"Analysis complete!")
print(f"Inferences: {report['summary']['total_inferences']}")
print(f"Patterns: {report['summary']['patterns_detected']}")
print(f"Leads: {report['summary']['leads_generated']}")
```

### Get Investigation Leads

```python
# Train introspection system
training_summary = system.train_introspection()

# Get generated leads
leads = system.get_investigation_leads()

for lead in leads:
    print(f"[{lead['priority']}] {lead['description']}")
    print(f"Confidence: {lead['confidence']:.2f}")
    for action in lead['recommended_actions']:
        print(f"  • {action}")
```

### Ask Natural Language Questions

```python
# Ask questions about the case
response = system.ask_llm("What suspicious activities have been detected?")
print(response['answer'])
print(f"Confidence: {response['confidence']:.2f}")
```

## Integration with HyperGNN

The OpenCog Case-LLM integrates seamlessly with the existing HyperGNN framework:

```python
from frameworks.hypergnn_core import HyperGNNFramework
from frameworks.opencog_case_llm import OpenCogCaseLLM

# Create HyperGNN framework
hypergnn = HyperGNNFramework("case_001")
# ... add agents, events, flows to hypergnn ...

# Initialize OpenCog Case-LLM
system = OpenCogCaseLLM("case_001")

# Load data from HyperGNN
stats = system.load_case_from_hypergnn(hypergnn)
print(f"Loaded {stats['entities_added']} entities")
print(f"Loaded {stats['events_added']} events")
print(f"Loaded {stats['relationships_added']} relationships")

# Now use OpenCog capabilities on HyperGNN data
system.run_complete_analysis()
```

## Example: Complete Analysis

See `examples/opencog_case_llm_demo.py` for a comprehensive demonstration:

```bash
python examples/opencog_case_llm_demo.py
```

This demo shows:
1. System initialization
2. Adding entities, events, relationships, and evidence
3. HGNNQL queries
4. Inference engine usage
5. Introspection training
6. Natural language interaction
7. Complete analysis pipeline
8. Result export

## Output Files

The system generates several output files:

- `knowledge_base_<case_id>.json`: Complete AtomSpace export
- `training_results_<case_id>.json`: Super-Sleuth training results
- `opencog_case_llm_analysis_<case_id>.json`: Complete analysis report

## Advanced Usage

### Custom Inference Rules

```python
from frameworks.hyper_holmes_inference import InferenceRule, RuleType
from frameworks.opencog_hgnnql import TruthValue

# Create custom rule
custom_rule = InferenceRule(
    rule_id="custom_rule_001",
    rule_type=RuleType.DEDUCTION,
    name="Custom Deduction Rule",
    description="Custom inference logic",
    premises=[{"atom_type": AtomType.ENTITY}],
    conclusion={"atom_type": AtomType.PATTERN, "name": "custom_pattern"}
)

# Add to inference engine
system.inference_engine.add_rule(custom_rule)

# Run inference with custom rule
results = system.run_inference()
```

### Pattern Learning

```python
# Train on specific pattern categories
trainer = system.trainer

# Analyze specific patterns
timing_patterns = trainer._analyze_timing_patterns()
financial_patterns = trainer._analyze_financial_patterns()

# Get pattern statistics
stats = trainer.pattern_statistics
print(stats)
```

### Export and Visualization

```python
# Export knowledge base
system.export_knowledge_base("my_case_kb.json")

# Export training results
system.export_training_results("training_results.json")

# Get system status
status = system.get_system_status()
print(json.dumps(status, indent=2))
```

## Benefits

1. **Unified Knowledge Representation**: All case knowledge in one hypergraph
2. **Automated Reasoning**: Derive new insights automatically
3. **Pattern Learning**: System improves over time
4. **Natural Language Interface**: Ask questions in plain English
5. **Investigation Leads**: Automatically generate leads
6. **Scalable**: Handles complex cases with many entities and events
7. **Explainable**: All inferences are traceable
8. **Integrable**: Works with existing HyperGNN framework

## Performance Considerations

- **AtomSpace Size**: Performance scales with number of atoms (typically O(n log n))
- **Inference Iterations**: Set appropriate max_iterations to balance completeness vs. speed
- **Pattern Learning**: Training time increases with data size
- **LLM Embeddings**: Can be pre-computed and cached for better performance

## Future Enhancements

- Integration with actual LLM backends (GPT, Claude, Llama)
- Graph visualization of knowledge base
- Real-time inference updates
- Distributed AtomSpace for very large cases
- Integration with external knowledge bases
- Advanced causal reasoning algorithms

## References

- OpenCog Framework: http://opencog.org/
- HyperGraph Neural Networks: Research on hypergraph learning
- Probabilistic Logic Networks: OpenCog's inference system
- Knowledge Graphs: Graph-based knowledge representation

## Support

For questions and issues:
- GitHub Issues: https://github.com/rzonedevops/analysis/issues
- Documentation: See other docs in `docs/` directory
- Examples: See `examples/` directory

---

*This system represents a significant advancement in AI-powered case analysis,
combining symbolic reasoning, neural networks, and knowledge graphs into a
unified framework.*
