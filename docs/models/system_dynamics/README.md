# System Dynamics Model Documentation

## Overview

System Dynamics modeling for flow optimization and equilibrium analysis,
providing insights into system behavior and feedback loops.

## Core Components

### Stock and Flow Modeling
- Stock variable tracking
- Flow rate computation
- Accumulation analysis
- Balance equations

### Feedback Loops
- Positive feedback identification
- Negative feedback analysis
- Loop dominance
- System stability

### Equilibrium Analysis
- Equilibrium point computation
- Stability analysis
- Sensitivity testing
- Policy simulation

## Implementation Files

**Core Implementation:**
- `frameworks/system_dynamics.py` - Framework implementation
- `src/api/system_dynamics.py` - API integration

**Supporting Scripts:**
- `scripts/run_system_dynamics_simulation.py` - Simulation runner

## Usage

### Basic Usage

```python
from frameworks.system_dynamics import SystemDynamicsModel

# Initialize model
model = SystemDynamicsModel(case_id="case_001")

# Define stocks and flows
model.add_stock("evidence_count", initial_value=0)
model.add_flow("evidence_collection_rate", rate=5)

# Run simulation
results = model.simulate(duration=100, dt=1)
```

### Advanced Features

```python
# Feedback loop analysis
loops = model.identify_feedback_loops()

# Equilibrium computation
equilibrium = model.find_equilibrium()

# Sensitivity analysis
sensitivity = model.sensitivity_analysis(parameter="collection_rate")

# Policy simulation
policy_results = model.simulate_policy(policy_changes)
```

## Model Components

### Stocks
- Evidence accumulation
- Knowledge base
- Case complexity
- Resource levels

### Flows
- Evidence collection rate
- Information processing rate
- Resource consumption rate
- Case progress rate

### Feedback Loops
- Evidence → Analysis → More Evidence
- Complexity → Time → Resources
- Knowledge → Efficiency → More Knowledge

## Documentation

- System dynamics theory
- Model equations
- Calibration procedures
- Interpretation guidelines

## Performance

- Efficient for moderate-sized models (<1000 variables)
- Fast simulation (milliseconds per time step)
- Low memory requirements
- Parallelizable for large models

## Testing

Tests located in:
- `tests/unit/test_system_dynamics.py` - Unit tests
- `tests/integration/test_system_dynamics_integration.py` - Integration tests

## Examples

See `scripts/run_system_dynamics_simulation.py` for complete examples.

## Applications

- Resource planning
- Timeline prediction
- Workload analysis
- Policy evaluation
- Scenario planning
