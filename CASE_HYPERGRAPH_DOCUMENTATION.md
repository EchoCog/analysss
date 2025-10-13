# Case Hypergraph System Documentation

## Overview

The Case Hypergraph System provides a comprehensive framework for representing and analyzing complex relationships in case data. Unlike traditional graphs that connect pairs of nodes, hypergraphs can connect any number of nodes through hyperedges, making them ideal for representing multi-party relationships, group activities, and complex evidence linkages.

## System Components

### 1. Case Hypergraph Constructor (`case_hypergraph_constructor.py`)

The main module for building hypergraphs from case data.

#### Key Classes:

- **`HyperedgeType`**: Enum defining types of relationships
  - `COMMUNICATION`: Email, phone, or other communications
  - `TRANSACTION`: Financial or asset transfers
  - `LEGAL_PROCEEDING`: Court actions, filings, orders
  - `ORGANIZATIONAL`: Employment, membership relationships
  - `TEMPORAL_CLUSTER`: Events occurring in same time window
  - `EVIDENCE_LINK`: Entities mentioned in same evidence
  - `CONTROL_STRUCTURE`: Control or authority relationships
  - `KNOWLEDGE_SHARING`: Information exchange patterns

- **`Hyperedge`**: Represents a multi-way relationship
  - Connects 2 or more nodes
  - Has a type, weight, and timestamp
  - Tracks verification status and evidence references

- **`HypergraphNode`**: Represents an entity in the case
  - Can be a person, organization, email address, etc.
  - Tracks degree (number of hyperedges)
  - Maintains weighted degree for importance

- **`CaseHypergraph`**: Main hypergraph structure
  - Stores nodes and hyperedges
  - Builds incidence matrix representation
  - Provides analysis methods:
    - Community detection
    - Centrality measures
    - Temporal pattern finding
    - Similarity matrices

### 2. Hypergraph Visualizer (`hypergraph_visualizer.py`)

Provides comprehensive visualization capabilities.

#### Visualization Types:

1. **Network Projection** (`projection.png`)
   - Projects hypergraph to regular graph
   - Shows all entities and their connections
   - Node size indicates importance (weighted degree)
   - Color indicates entity type

2. **Incidence Matrix** (`incidence_matrix.png`)
   - Shows which nodes belong to which hyperedges
   - Useful for seeing participation patterns

3. **Node Similarity Matrix** (`similarity_matrix.png`)
   - Shows how similar nodes are based on shared hyperedges
   - Helps identify closely related entities

4. **Community Structure** (`communities.png`)
   - Detects and visualizes communities/clusters
   - Shows groups of tightly connected entities

5. **Temporal Evolution** (`temporal.png`)
   - Shows how the hypergraph grows over time
   - Tracks new hyperedges and cumulative nodes

6. **Centrality Analysis** (`centrality.png`)
   - Identifies most important nodes by various measures:
     - Degree: Most connected
     - Weighted degree: Highest total edge weights
     - Eigenvector: Connected to important nodes
     - Betweenness: Bridge between communities

7. **Hyperedge Distribution** (`distributions.png`)
   - Shows distribution of hyperedge types
   - Displays hyperedge size distribution

### 3. Case Data Loader Integration

The system integrates with the existing `case_data_loader.py` to:
- Extract entities from case documents
- Identify relationships and events
- Track verification status
- Build hypergraph structure

## Usage

### Basic Usage

```python
from case_data_loader import CaseDataLoader
from case_hypergraph_constructor import CaseHypergraphBuilder

# Load case data
loader = CaseDataLoader("case_2025_137857")
loader.load_case_documents()

# Build hypergraph
builder = CaseHypergraphBuilder(loader)
hypergraph = builder.build()

# Save hypergraph
hypergraph.save_to_file("case_hypergraph.json")
```

### Visualization

```python
from hypergraph_visualizer import HypergraphVisualizer

# Load hypergraph
hypergraph = CaseHypergraph.load_from_file("case_hypergraph.json")

# Create visualizer
visualizer = HypergraphVisualizer(hypergraph)

# Generate all visualizations
visualizer.save_all_visualizations("hypergraph_visualizations")
```

### Analysis Examples

```python
# Find communities
communities = hypergraph.detect_communities()

# Compute centrality
centrality = hypergraph.compute_centrality_measures()
top_nodes = sorted(centrality['eigenvector'].items(), 
                  key=lambda x: x[1], reverse=True)[:10]

# Find temporal patterns
patterns = hypergraph.find_temporal_patterns(window_days=7)

# Find overlapping hyperedges
overlaps = hypergraph.find_overlapping_hyperedges(min_overlap=3)
```

## Hypergraph Analysis Insights

### Key Metrics from Case Analysis

Based on the constructed hypergraph:

- **Nodes**: 1,262 entities identified
- **Hyperedges**: 84 multi-way relationships
- **Communities**: 4 major clusters detected
- **Key Entities** (by centrality):
  - Peter Faucitt: Highest degree (10 hyperedges)
  - Danie Bantjies: 9 hyperedges
  - Rynette Farrar: 8 hyperedges
  - Daniel Faucitt: 8 hyperedges

### Temporal Patterns

The system identified 13 temporal patterns, with the most active period on 2025-06-06 involving:
- 14 hyperedges
- 32 participants
- Multiple types: legal proceedings, communications, evidence links

### Overlapping Relationships

Found 219 overlapping hyperedge pairs, indicating complex interconnections between different aspects of the case.

## Mathematical Foundation

### Incidence Matrix

The incidence matrix H is an n×m matrix where:
- n = number of nodes
- m = number of hyperedges
- H[i,j] = weight if node i is in hyperedge j, 0 otherwise

### Node Similarity

Node similarity is computed as: S = H × H^T

Where S[i,j] represents how many weighted hyperedges nodes i and j share.

### Hyperedge Similarity

Hyperedge similarity is computed as: T = H^T × H

Where T[i,j] represents how many nodes hyperedges i and j share.

## Benefits of Hypergraph Representation

1. **Multi-party Relationships**: Can represent communications involving multiple people
2. **Temporal Clustering**: Groups events occurring in same time window
3. **Evidence Linkage**: Shows which entities appear in same documents
4. **Community Detection**: Identifies groups of related entities
5. **Pattern Recognition**: Finds recurring structures and anomalies

## File Formats

### Hypergraph JSON Format

```json
{
  "case_id": "case_2025_137857",
  "metadata": {
    "node_count": 1262,
    "hyperedge_count": 84,
    "creation_time": "2025-09-30T..."
  },
  "nodes": {
    "node_id": {
      "node_id": "string",
      "node_type": "person|organization|email_address",
      "label": "Display name",
      "attributes": {},
      "hyperedges": ["edge_id1", "edge_id2"],
      "degree": 5,
      "weighted_degree": 7.5
    }
  },
  "hyperedges": {
    "edge_id": {
      "edge_id": "string",
      "nodes": ["node_id1", "node_id2", "node_id3"],
      "edge_type": "communication",
      "weight": 1.0,
      "timestamp": "2025-06-06T...",
      "attributes": {},
      "evidence_refs": ["doc1.md"],
      "verification_status": "verified"
    }
  },
  "analysis": {
    "communities": {},
    "centrality": {},
    "temporal_patterns": [],
    "overlapping_edges": []
  }
}
```

## Performance Considerations

- The system efficiently handles thousands of nodes and hundreds of hyperedges
- Incidence matrix operations use NumPy for performance
- Community detection uses the Louvain algorithm
- Visualization automatically adjusts for large graphs

## Future Enhancements

1. **Interactive Visualizations**: Web-based interactive hypergraph explorer
2. **Real-time Updates**: Stream processing for new evidence
3. **Machine Learning**: Anomaly detection and prediction models
4. **Query Language**: Hypergraph query language for complex searches
5. **Distributed Processing**: Handle larger case datasets

## Conclusion

The Case Hypergraph System provides a powerful framework for understanding complex relationships in case data. By representing multi-way relationships and providing comprehensive analysis tools, it enables investigators to uncover patterns and connections that might be missed in traditional pairwise analysis.