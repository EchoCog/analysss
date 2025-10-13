# HyperGraphQL API Documentation

## Overview

The HyperGraphQL API provides a comprehensive GraphQL-based interface for managing and querying hypergraph structures that map to the HyperGNN framework. It enables org-aware repository management with support for multi-level scaling from individual repos to enterprise organizations.

## Key Features

### 1. **Org-Aware Schema Management**
- Support for REPO, ORG, and ENTERPRISE level operations
- Hierarchical organization structure mapping
- Cross-repo entity and relation aggregation

### 2. **GitHub Repository Integration**
- Project entities and relations to/from GitHub repo folder structures
- Automatic folder structure initialization
- Bidirectional sync between schema and repository files

### 3. **Scalability**
- **Scale Up**: Aggregate data from multiple repos into org-level views
- **Scale Down**: Compress repos for efficient storage
- **Enterprise Level**: Cross-org analysis and unified schemas

### 4. **HyperGNN Framework Integration**
- Direct mapping from HyperGNN agents, events, and flows
- Timeline tensor support
- Evidence-based relationship tracking

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                        │
│              (analysis-frontend/apiService.js)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  HyperGraphQL API                        │
│              (src/api/hypergraphql_api.py)              │
│                                                          │
│  - GraphQL Query Endpoint                               │
│  - REST Endpoints                                       │
│  - GitHub Integration Routes                            │
└────────┬───────────────────────────┬────────────────────┘
         │                           │
         ▼                           ▼
┌─────────────────────┐    ┌─────────────────────────────┐
│   Schema Module     │    │   Resolver Module           │
│  (schema.py)        │◄───┤  (resolvers.py)             │
│                     │    │                             │
│  - Node Types       │    │  - Query Resolvers          │
│  - Edge Types       │    │  - Mutation Resolvers       │
│  - Org Mappings     │    │  - HyperGNN Integration     │
└─────────────────────┘    └─────────────┬───────────────┘
                                         │
                                         ▼
                           ┌──────────────────────────────┐
                           │   GitHub Integration         │
                           │   (github.py)                │
                           │                              │
                           │  - Repo Projection           │
                           │  - Org Management            │
                           │  - Compression/Scaling       │
                           └──────────────────────────────┘
```

## Core Components

### 1. HyperGraphQL Schema (`src/api/hypergraphql_schema.py`)

Defines the core data structures and GraphQL schema.

#### Entity Types
- `PERSON` - Individual entities
- `ORGANIZATION` - Organizational entities
- `EVENT` - Event nodes
- `EVIDENCE` - Evidence nodes
- `LOCATION` - Location nodes
- `DOCUMENT` - Document nodes
- `TRANSACTION` - Transaction nodes
- `AGENT` - Agent nodes (from HyperGNN)

#### Relation Types
- `PARTICIPATES_IN` - Participation relationships
- `OWNS` - Ownership relationships
- `CONTROLS` - Control relationships
- `COMMUNICATES_WITH` - Communication relationships
- `TRANSACTS_WITH` - Transaction relationships
- `LOCATED_AT` - Location relationships
- `EVIDENCES` - Evidence relationships
- `RELATED_TO` - General relationships
- `PARENT_OF` - Parent-child relationships
- `MEMBER_OF` - Membership relationships

#### Organization Levels
- `REPO` - Repository level (single repo)
- `ORG` - Organization level (multiple repos)
- `ENTERPRISE` - Enterprise level (multiple orgs)

### 2. HyperGraphQL Resolvers (`src/api/hypergraphql_resolvers.py`)

Implements query and mutation resolvers.

#### Key Methods
- `resolve_node(node_id)` - Get a single node
- `resolve_nodes(node_type, org_level)` - Get filtered nodes
- `resolve_edge(edge_id)` - Get a single edge
- `resolve_edges(edge_type, org_level)` - Get filtered edges
- `resolve_connected_nodes(node_id)` - Get connected nodes
- `load_from_hypergnn(case_id)` - Load from HyperGNN framework
- `load_from_repo_structure(repo_path, org_name)` - Load from GitHub repo

### 3. GitHub Integration (`src/api/hypergraphql_github.py`)

Manages GitHub repository projection and org-aware operations.

#### GitHubRepoProjection Class
```python
projection = GitHubRepoProjection("/path/to/repo")
projection.initialize_repo_structure()  # Create folder structure
projection.project_schema(schema)       # Project schema to files
stats = projection.get_repo_stats()     # Get statistics
```

#### OrgAwareManager Class
```python
manager = OrgAwareManager("my-org", OrgLevel.ORG)
manager.register_repo("repo1", "/path/to/repo1")
manager.register_repo("repo2", "/path/to/repo2")
aggregated = manager.aggregate_schemas()  # Combine repos
stats = manager.get_org_stats()          # Get org stats
```

## API Endpoints

### GraphQL Endpoint

**POST** `/api/v1/hypergraphql/query`

Execute GraphQL queries.

```json
{
  "query": "query { nodes(nodeType: \"person\") { id name } }",
  "variables": {}
}
```

### REST Endpoints

#### Nodes

**GET** `/api/v1/hypergraphql/nodes`
- Query params: `type`, `orgLevel`
- Returns: List of nodes

**GET** `/api/v1/hypergraphql/nodes/{node_id}`
- Returns: Single node

**POST** `/api/v1/hypergraphql/nodes`
- Body: Node data
- Returns: Created node

#### Edges

**GET** `/api/v1/hypergraphql/edges`
- Query params: `type`, `orgLevel`
- Returns: List of edges

**GET** `/api/v1/hypergraphql/edges/{edge_id}`
- Returns: Single edge

**POST** `/api/v1/hypergraphql/edges`
- Body: Edge data
- Returns: Created edge

#### GitHub Integration

**POST** `/api/v1/hypergraphql/github/repo/init`
```json
{
  "repoPath": "/path/to/repo"
}
```

**POST** `/api/v1/hypergraphql/github/repo/project`
```json
{
  "repoPath": "/path/to/repo"
}
```

**POST** `/api/v1/hypergraphql/github/repo/load`
```json
{
  "repoPath": "/path/to/repo",
  "orgName": "my-org"
}
```

**POST** `/api/v1/hypergraphql/github/org/register`
```json
{
  "orgName": "my-org",
  "orgLevel": "ORG"
}
```

**POST** `/api/v1/hypergraphql/github/org/{org_name}/repos`
```json
{
  "repoName": "repo1",
  "repoPath": "/path/to/repo1"
}
```

**POST** `/api/v1/hypergraphql/github/org/{org_name}/aggregate`
- Aggregates schemas from all repos in the org

**GET** `/api/v1/hypergraphql/github/org/{org_name}/stats`
- Returns org statistics

**POST** `/api/v1/hypergraphql/github/repo/compress`
```json
{
  "orgName": "my-org",
  "repoName": "repo1",
  "outputPath": "/path/to/output"
}
```

**GET** `/api/v1/hypergraphql/export`
- Query param: `orgLevel` (optional)
- Returns: Full schema export

## Frontend Integration

The frontend API service has been extended with HyperGraphQL methods:

```javascript
import apiService from './services/apiService'

// Get GraphQL schema
const schema = await apiService.getGraphQLSchema()

// Execute GraphQL query
const result = await apiService.executeGraphQLQuery(
  'query { nodes { id name } }',
  {}
)

// Get nodes
const nodes = await apiService.getHGQLNodes('person', 'repo')

// Get a specific node
const node = await apiService.getHGQLNode('person_123')

// Create a node
const newNode = await apiService.createHGQLNode({
  nodeType: 'person',
  name: 'John Doe',
  properties: { age: 30 },
  orgLevel: 'repo'
})

// GitHub operations
await apiService.initGitHubRepoStructure('/path/to/repo')
await apiService.projectSchemaToRepo('/path/to/repo')
await apiService.loadFromGitHubRepo('/path/to/repo', 'my-org')

// Org management
await apiService.registerGitHubOrg('my-org', 'ORG')
await apiService.registerRepoToOrg('my-org', 'repo1', '/path/to/repo1')
const aggregated = await apiService.aggregateOrgSchemas('my-org')
const stats = await apiService.getOrgStats('my-org')
```

## Repository Folder Structure

When a schema is projected to a GitHub repository, the following structure is created:

```
repo/
├── README.md
├── entities/
│   ├── person/
│   │   ├── README.md
│   │   ├── person_1.json
│   │   ├── person_2.json
│   │   └── ...
│   ├── organization/
│   │   ├── README.md
│   │   ├── org_1.json
│   │   └── ...
│   ├── event/
│   ├── evidence/
│   ├── location/
│   ├── document/
│   ├── transaction/
│   └── agent/
└── relations/
    ├── participates_in/
    │   ├── README.md
    │   ├── relation_1.json
    │   └── ...
    ├── owns/
    ├── controls/
    ├── communicates_with/
    └── ...
```

### Entity File Format

```json
{
  "id": "person_123",
  "name": "John Doe",
  "properties": {
    "age": 30,
    "role": "analyst"
  },
  "metadata": {
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00",
    "org_level": "repo"
  }
}
```

### Relation File Format

```json
{
  "id": "relation_456",
  "type": "owns",
  "source": "person_123",
  "targets": ["org_789"],
  "strength": 0.9,
  "properties": {
    "since": "2020-01-01"
  },
  "evidence_refs": ["evidence_1", "evidence_2"],
  "timestamp": "2025-01-01T00:00:00",
  "metadata": {
    "org_level": "repo"
  }
}
```

## Use Cases

### 1. Single Repository Analysis

```python
from src.api.hypergraphql_schema import HyperGraphQLSchema
from src.api.hypergraphql_github import GitHubRepoProjection

# Create and populate schema
schema = HyperGraphQLSchema()
# ... add nodes and edges ...

# Project to repository
projection = GitHubRepoProjection("/path/to/repo")
projection.project_schema(schema)
```

### 2. Multi-Repository Organization

```python
from src.api.hypergraphql_github import OrgAwareManager, OrgLevel

# Create org manager
manager = OrgAwareManager("my-org", OrgLevel.ORG)

# Register repos
manager.register_repo("case1", "/path/to/case1")
manager.register_repo("case2", "/path/to/case2")

# Aggregate schemas
aggregated_schema = manager.aggregate_schemas()

# Get org statistics
stats = manager.get_org_stats()
```

### 3. Enterprise-Level Scaling

```python
# Create multiple org managers
org1_manager = OrgAwareManager("org1", OrgLevel.ORG)
org2_manager = OrgAwareManager("org2", OrgLevel.ORG)

# Register repos to each org
# ...

# Scale up to enterprise
enterprise_schema = org1_manager.scale_up_to_enterprise([org2_manager])
```

### 4. HyperGNN Integration

```python
from src.api.hypergnn_core import HyperGNNFramework
from src.api.hypergraphql_resolvers import HyperGraphQLResolver

# Create HyperGNN framework
framework = HyperGNNFramework("case_123")
# ... add agents, events, flows ...

# Load into HyperGraphQL
resolver = HyperGraphQLResolver()
resolver.set_hypergnn_framework("case_123", framework)
resolver.load_from_hypergnn("case_123")
```

### 5. Compression for Storage

```python
# Compress a repo
archive_path = manager.compress_repo("repo1", "/path/to/archives")

# Later, decompress
manager.decompress_repo(archive_path, "/path/to/restore")
```

## GraphQL Schema Definition

The complete GraphQL schema is available via the `/api/v1/hypergraphql/schema` endpoint.

Key types:
- `HyperGraphQLNode` - Entity nodes
- `HyperGraphQLEdge` - Relation edges
- `HyperGraphQLOrgMapping` - Organization mappings
- `Query` - Query operations
- `Mutation` - Mutation operations

## Testing

Unit tests are available in:
- `tests/unit/test_hypergraphql_schema.py`
- `tests/integration/test_hypergraphql_integration.py`

Run tests with:
```bash
pytest tests/unit/test_hypergraphql_schema.py
pytest tests/integration/test_hypergraphql_integration.py
```

## Performance Considerations

1. **Caching**: Schema exports and aggregations are computed on-demand
2. **File I/O**: Repository projections involve file system operations
3. **Scaling**: Enterprise-level operations may require significant memory
4. **Compression**: Use compression for archiving inactive repos

## Security Considerations

1. **Path Validation**: Ensure repository paths are validated
2. **Access Control**: Implement proper authentication/authorization
3. **Data Validation**: Validate all input data
4. **Evidence Refs**: Ensure evidence references are properly secured

## Future Enhancements

1. **GraphQL Library Integration**: Replace simple query parser with proper GraphQL library (graphene, strawberry)
2. **Subscriptions**: Add real-time updates via WebSocket
3. **Caching Layer**: Implement Redis caching for performance
4. **Batch Operations**: Support batch import/export
5. **Advanced Queries**: Complex graph traversal queries
6. **Version Control**: Track schema versions and changes
7. **Conflict Resolution**: Handle merge conflicts in multi-repo scenarios

## Support

For issues or questions, refer to:
- Main documentation: `README.md`
- Technical architecture: `TECHNICAL_ARCHITECTURE.md`
- API documentation: `API_DOCUMENTATION.md`
