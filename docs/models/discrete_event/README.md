# Discrete Event Model Documentation

## Overview

Discrete Event Modeling for timeline and sequence analysis, providing event-driven
simulation capabilities for case analysis.

## Core Components

### Event Modeling
- Event type classification
- Event state tracking
- Actor involvement tracking
- Evidence requirement mapping

### Timeline Analysis
- Temporal sequence analysis
- Event cascade simulation
- Critical path identification
- Dependency tracking

### Simulation Engine
- Discrete event simulation
- Timing optimization
- What-if analysis
- Scenario modeling

## Implementation Files

**Core Implementation:**
- `src/models/discrete_event_model.py` - Main implementation

**Supporting Scripts:**
- `scripts/run_discrete_event_simulation.py` - Simulation runner

## Usage

### Basic Usage

```python
from src.models.discrete_event_model import DiscreteEventModel

# Initialize model
model = DiscreteEventModel(case_id="case_001")

# Add events
model.add_event(event)

# Process timeline
results = model.process_timeline(timeline_entries)

# Generate evidence report
report = model.generate_evidence_report()
```

### Advanced Features

```python
# Event cascade analysis
cascades = model.analyze_cascades()

# Critical path identification
critical_path = model.find_critical_path()

# What-if analysis
scenario_results = model.simulate_scenario(changes)
```

## Event Types

- **LEGAL_ACTION**: Court filings, hearings, judgments
- **TRANSACTION**: Financial transactions
- **COMMUNICATION**: Emails, calls, messages
- **MEETING**: In-person or virtual meetings
- **DOCUMENT**: Document creation or signing
- **EVIDENCE_DISCOVERY**: Evidence collection
- **STATUS_CHANGE**: Status updates

## Documentation

- [DISCRETE_EVENT_MODEL_SUMMARY.md](../../../DISCRETE_EVENT_MODEL_SUMMARY.md) - Complete summary

## Performance

- Fast execution for large timelines (10,000+ events)
- Low memory footprint
- Suitable for real-time analysis
- Efficient cascade detection

## Testing

Tests located in:
- `tests/unit/test_discrete_event_model.py` - Unit tests
- `tests/integration/test_discrete_event_integration.py` - Integration tests

## Examples

See `scripts/run_discrete_event_simulation.py` for complete examples.
