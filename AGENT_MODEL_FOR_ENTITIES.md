# Agent Model Implementation for Entities

## Overview

This document describes the agent-based modeling implementation for `CaseEntity` objects in the analysis framework. This enhancement enables each entity (person, organization, system) to be modeled as an intelligent agent with behavioral properties, decision-making rules, strategic goals, and state management capabilities.

## Key Features

### 1. Behavioral Properties

Each entity can be initialized with quantitative behavioral properties on a scale of 0.0 to 1.0:

- **legal_aggression**: Propensity to use legal mechanisms aggressively
- **control_seeking**: Desire to maintain or gain control over situations
- **evidence_dismissal**: Tendency to dismiss or ignore contradictory evidence
- **vulnerability_to_pressure**: Susceptibility to external legal or social pressure
- **ethical_compliance**: Level of adherence to ethical standards

### 2. Behavioral Rules

Entities can have rule-based decision logic in the form:
```
IF <condition> THEN <action>
```

Examples:
- `IF challenged THEN escalate through legal mechanisms`
- `IF evidence contradicts claims THEN ignore and escalate`
- `IF attacked THEN provide evidence`

### 3. Strategic Goals

Entities maintain a list of strategic objectives that guide their behavior:
- "Maintain control over financial resources"
- "Protect personal interests"
- "Expose financial misconduct"
- "Maintain credibility as witness"

### 4. State Management

Entities track their current state and maintain a history of state changes:
- **current_state**: Current status, events participated, decisions made, relationships
- **state_history**: Complete history of state transitions with timestamps

### 5. Relationship Management

Entities can maintain relationship strengths (0.0 to 1.0) with other entities, tracking:
- Professional relationships
- Adversarial relationships
- Neutral relationships

### 6. Decision Making

Entities can make decisions based on:
- Behavioral rules (if-then logic)
- Behavioral properties (when no rule matches)
- Current context and state

## Usage

### Basic Initialization

```python
from case_data_loader import CaseEntity, InformationStatus

# Create a basic entity
entity = CaseEntity(
    entity_id="person_001",
    name="John Doe",
    entity_type="person",
    roles=["witness"]
)

# Initialize agent model
entity.initialize_agent_model(
    legal_aggression=0.5,
    control_seeking=0.4,
    evidence_dismissal=0.3,
    vulnerability_to_pressure=0.6,
    ethical_compliance=0.8
)
```

### Adding Rules and Goals

```python
# Add behavioral rules
entity.add_behavioral_rule("challenged", "provide supporting documentation")
entity.add_behavioral_rule("evidence presented", "analyze and respond")

# Add strategic goals
entity.add_strategic_goal("Maintain credibility")
entity.add_strategic_goal("Support legal process")
```

### State Management

```python
# Update state based on events
entity.update_state("event_001", {
    'status': 'provided_evidence',
    'cooperation_level': 'high'
})

# Check state
print(f"Events participated: {entity.current_state['events_participated']}")
print(f"State history entries: {len(entity.state_history)}")
```

### Decision Making

```python
# Make a decision based on context
context = {
    'event': 'evidence presented',
    'type': 'contradictory',
    'severity': 'high'
}

decision = entity.make_decision(context)
print(f"Decision: {decision['decision']}")
print(f"Reasoning: {decision['reasoning']}")
```

### Relationship Management

```python
# Update relationship with another entity
entity.update_relationship("entity_002", 0.3)  # Strengthen relationship

# Get relationship strength
strength = entity.get_relationship_strength("entity_002")
print(f"Relationship strength: {strength}")
```

### Converting to HyperGNN Agent

```python
# Convert CaseEntity to Agent for use in HyperGNN framework
agent = entity.to_agent()

# The agent can now be used in:
# - HyperGNN Framework
# - Discrete Event Models
# - System Dynamics Models
# - Timeline Tensor Generation
```

## Predefined Agent Profiles

The `AgentModelFactory` class provides predefined profiles based on the agent-based model analysis in `models/frameworks/agent_based_model_updated.md`:

### Primary Agents

```python
from case_data_loader import AgentModelFactory, CaseEntity

# Create Peter Faucitt profile
entity = CaseEntity(
    entity_id="peter_faucitt",
    name="Peter Faucitt",
    entity_type="person",
    roles=["defendant"]
)
entity = AgentModelFactory.create_primary_agent(entity, "peter_faucitt")
# High legal_aggression (0.9), control_seeking (0.95)
# Rules: escalate when challenged, ignore contradictory evidence
# Goals: Maintain control, neutralize witnesses, establish dominance

# Create Jacqueline Faucitt profile
entity = AgentModelFactory.create_primary_agent(entity, "jacqueline_faucitt")
# High vulnerability_to_pressure (0.8), ethical_compliance (0.7)
# Rules: provide evidence when attacked, partial compliance when coerced
# Goals: Protect interests, expose misconduct, resist control

# Create Daniel Faucitt profile
entity = AgentModelFactory.create_primary_agent(entity, "daniel_faucitt")
# Very high ethical_compliance (0.9), evidence_provision
# Rules: provide comprehensive evidence, strategic compliance
# Goals: Expose crimes, maintain credibility, resist control
```

### Secondary Agents

```python
# Elliott Attorneys profile
entity = AgentModelFactory.create_secondary_agent(entity, "elliott_attorneys")
# Low ethical_compliance (0.3), high legal creativity
# Goals: Serve client regardless of ethics, generate fees

# ENS Africa profile
entity = AgentModelFactory.create_secondary_agent(entity, "ens_africa")
# Medium ethical_compliance (0.6)
# Goals: Maintain client relationship, limit liability

# Medical Professionals profile
entity = AgentModelFactory.create_secondary_agent(entity, "medical_professionals")
# Low professional independence, high financial motivation
# Goals: Generate fees, maintain referrals
```

### Institutional Agents

```python
# Court System profile
entity = AgentModelFactory.create_institutional_agent(entity, "court_system")
# High ethical_compliance (0.8), procedural adherence
# Goals: Uphold procedures, process cases efficiently

# Forensic Investigators profile
entity = AgentModelFactory.create_institutional_agent(entity, "forensic_investigators")
# Medium ethical_compliance (0.7)
# Goals: Complete investigation within parameters, maintain reputation
```

## Integration with Existing Frameworks

### HyperGNN Framework Integration

```python
from frameworks.hypergnn_core_enhanced import HyperGNNFramework

# Create framework
framework = HyperGNNFramework(case_id="case_001")

# Add entities as agents
entity = CaseEntity(...)
entity.initialize_agent_model(...)
agent = entity.to_agent()
framework.add_agent(agent)
```

### Discrete Event Model Integration

The agent model seamlessly integrates with the discrete event model in `src/models/discrete_event_model.py`:

```python
from src.models.discrete_event_model import DiscreteEventModel

# Agent states are automatically tracked
# Events update agent states
# Decision making is based on agent behavioral properties
```

### LLM Transformer Integration

Agent perspectives can be used in the transformer model:

```python
from src.models.enhanced_llm_transformer import MultiAgentTransformerModel

# Agent perspectives map to attention heads
# Each agent has a unique perspective on events
```

## Testing

Comprehensive unit tests are provided in `tests/unit/test_agent_model_entity.py`:

```bash
# Run tests
python -m unittest tests.unit.test_agent_model_entity -v

# All 15 tests should pass:
# - Agent model initialization
# - Behavioral rule management
# - Strategic goal management  
# - State management and history
# - Decision making
# - Relationship management
# - Agent conversion
# - Predefined profile creation
```

## Demonstration

A demonstration script is available at `demo_agent_model_entities.py`:

```bash
python demo_agent_model_entities.py
```

This demonstrates:
1. Basic agent model initialization
2. Behavioral rules
3. Strategic goals
4. State management
5. Decision making
6. Relationship management
7. Predefined agent profiles
8. Converting to HyperGNN Agent

## Benefits

1. **Realistic Modeling**: Entities behave according to documented behavioral patterns
2. **Predictive Analysis**: Agent decisions can be simulated and analyzed
3. **Interaction Modeling**: Relationship dynamics can be tracked over time
4. **State Tracking**: Complete history of agent states and decisions
5. **Framework Integration**: Seamless conversion to existing framework types
6. **Evidence-Based**: Profiles based on actual case analysis documentation

## Future Enhancements

Potential future enhancements include:

1. **Learning Mechanisms**: Agents that adapt based on experience
2. **Game-Theoretic Models**: Strategic interaction analysis
3. **Network Effects**: Modeling influence propagation through agent networks
4. **Temporal Evolution**: Dynamic behavioral property changes over time
5. **Multi-Agent Simulation**: Running complete case simulations with all agents
6. **Visualization**: Interactive agent network and decision tree visualization

## References

- `models/frameworks/agent_based_model_updated.md`: Source of behavioral patterns and profiles
- `frameworks/hypergnn_core_enhanced.py`: HyperGNN Agent class definition
- `src/models/discrete_event_model.py`: Discrete event model integration
- `HYPERGNN_COMPREHENSIVE_SCHEMA.md`: Overall framework architecture
