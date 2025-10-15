# AD Hypergraph Repository Mapping Documentation

## Overview

The AD (Affidavit/Analysis Document) Hypergraph Repository Mapper enables comprehensive cross-repository analysis and evidence correlation across multiple GitHub repositories. This system maps entities, relations, and evidence across distributed repositories to create a unified hypergraph view for legal case analysis.

## Target Repositories

The system is configured to map the following repositories:

### Primary Evidence Source: `cogpy/ad-res-j7`
- **Evidence Level**: Primary
- **Organization**: cogpy
- **Key Evidence Folders**:
  - `evidence/bank_records`
  - `evidence/director_loan_accounts`
  - `evidence/correspondence`
  - `evidence/invoices`
  - `evidence/shopify_reports`
  - `jax-response`
  - `case_2025_137857`

### Comprehensive Analysis Hub: `EchoCog/analysss` 
- **Evidence Level**: Comprehensive
- **Organization**: EchoCog
- **Key Evidence Folders**:
  - `jax-response`
  - `murder-theft`
  - `case_2025_137857`
  - `evidence`

### Additional Repositories:
- **`rzonedevops/analysis`** - Limited evidence (workflows, analysis)
- **`rzonedevops/avtomaatoctory`** - No evidence (automation processes)
- **`rzonedevops/analyticase`** - Limited evidence (legal framework)

## Architecture

### Core Components

#### 1. ADHypergraphRepositoryMapper
Main orchestrator class that manages repository configurations, scanning, loading, and cross-repository linking.

```python
from src.api.ad_hypergraph_repository_mapper import ADHypergraphRepositoryMapper

mapper = ADHypergraphRepositoryMapper()
```

#### 2. RepositoryConfig
Configuration class for each target repository with metadata about evidence levels and folder structures.

#### 3. HyperGraphQL Integration
Extended the existing HyperGraphQL API with new resolvers for AD hypergraph operations:
- `resolve_ad_hypergraph_summary()`
- `resolve_ad_hypergraph_scan()`
- `resolve_ad_hypergraph_load()`
- `resolve_ad_hypergraph_generate_links()`
- `resolve_ad_hypergraph_export()`

## Command Line Interface

### Available Commands

```bash
# Get repository mapping summary
python src/main.py ad-hypergraph summary

# Scan repositories for entities, relations, and evidence
python src/main.py ad-hypergraph scan --repo analysss --output scan_results.json

# Load repositories into unified hypergraph schema
python src/main.py ad-hypergraph load --repo analysss

# Generate cross-repository entity links
python src/main.py ad-hypergraph link

# Export unified hypergraph
python src/main.py ad-hypergraph export --output unified_hypergraph.json
```

### Usage Examples

#### 1. Repository Summary
```bash
python src/main.py ad-hypergraph summary
```

Output includes:
- Total repositories configured
- Evidence level distribution
- Organization distribution  
- Entity and relation counts
- Local availability status

#### 2. Repository Scanning
```bash
# Scan specific repository
python src/main.py ad-hypergraph scan --repo analysss

# Scan all local repositories
python src/main.py ad-hypergraph scan
```

Scanning identifies:
- Entity files (JSON, Markdown)
- Relation files (JSON)
- Evidence files (PDF, DOC, images, etc.)
- File metadata and statistics

#### 3. Loading into Schema
```bash
# Load specific repository
python src/main.py ad-hypergraph load --repo analysss

# Load all available repositories
python src/main.py ad-hypergraph load
```

Loading process:
- Parses entity files into HyperGraphQLNode objects
- Parses relation files into HyperGraphQLEdge objects  
- Prefixes IDs with repository names for uniqueness
- Adds repository metadata to all objects

#### 4. Cross-Repository Linking
```bash
python src/main.py ad-hypergraph link
```

Linking algorithms:
- Name similarity matching
- Property intersection analysis
- Evidence correlation
- Strength-based relationship weighting

#### 5. Unified Export
```bash
python src/main.py ad-hypergraph export --output unified_ad_hypergraph.json
```

Export includes:
- All entities from all repositories
- All relations including cross-repository links
- Repository metadata
- Evidence correlation data
- Export timestamps and statistics

## GraphQL API Integration

### New Query Types

```graphql
type Query {
  # AD Hypergraph Repository Mapping Queries
  adHypergraphSummary: ADHypergraphSummary
  adHypergraphScan(repoName: String): JSON
  adHypergraphLoad(repoName: String): ADHypergraphLoadResult
  adHypergraphGenerateLinks: ADHypergraphLinkResult
  adHypergraphExport(outputPath: String!): ADHypergraphExportResult
}

type ADHypergraphSummary {
  totalRepositories: Int!
  repositories: JSON!
  evidenceDistribution: JSON!
  organizationDistribution: JSON!
  totalEntities: Int!
  totalRelations: Int!
  summaryTimestamp: DateTime!
}
```

### Query Examples

```graphql
# Get repository summary
query {
  adHypergraphSummary {
    totalRepositories
    evidenceDistribution
    organizationDistribution
    totalEntities
    totalRelations
  }
}

# Scan specific repository
query {
  adHypergraphScan(repoName: "analysss")
}

# Load repository data
query {
  adHypergraphLoad(repoName: "analysss") {
    totalLoaded
    schemaStats
  }
}
```

## Data Models

### Entity Structure
```json
{
  "id": "repo_name:entity_id",
  "node_type": "PERSON|ORGANIZATION|EVENT|EVIDENCE|DOCUMENT",
  "name": "Entity Name",
  "properties": {
    "custom_field": "value"
  },
  "org_level": "ORG",
  "repo_path": "/path/to/repo",
  "folder_path": "entities/type/file.json",
  "metadata": {
    "source_repo": "repo_name", 
    "source_org": "org_name",
    "evidence_level": "primary|comprehensive|limited|none",
    "ad_hypergraph_mapping": true
  }
}
```

### Relation Structure
```json
{
  "id": "repo_name:relation_id",
  "edge_type": "PARTICIPATES_IN|OWNS|CONTROLS|RELATED_TO",
  "source_id": "repo_name:source_entity_id",
  "target_ids": ["repo_name:target_entity_id"],
  "strength": 0.8,
  "properties": {
    "relationship_type": "specific_type"
  },
  "evidence_refs": ["evidence_file_1", "evidence_file_2"],
  "metadata": {
    "source_repo": "repo_name",
    "cross_repository": false
  }
}
```

### Cross-Repository Link
```json
{
  "id": "cross_link:repo1:entity1:repo2:entity2",
  "edge_type": "RELATED_TO",
  "source_id": "repo1:entity1",
  "target_ids": ["repo2:entity2"],
  "strength": 0.6,
  "properties": {
    "link_type": "cross_repository",
    "similarity_basis": "name_and_properties"
  },
  "org_level": "ENTERPRISE",
  "metadata": {
    "created_by": "ad_hypergraph_mapper",
    "source_repos": ["repo1", "repo2"]
  }
}
```

## File Organization

### Expected Repository Structure
```
repository/
├── entities/
│   ├── persons/
│   │   ├── person1.json
│   │   └── person2.md
│   ├── organizations/
│   │   └── org1.json
│   └── events/
│       └── event1.json
├── relations/
│   ├── ownership/
│   │   └── relation1.json
│   └── financial-flows/
│       └── flow1.json
├── evidence/
│   ├── bank_records/
│   │   ├── statement1.pdf
│   │   └── statement2.pdf
│   ├── documents/
│   │   └── contract1.doc
│   └── communications/
│       └── email1.eml
└── jax-response/
    ├── AD/
    ├── analysis-output/
    └── evidence-attachments/
```

## Evidence Correlation

### Evidence Types Supported
- **Documents**: PDF, DOC, DOCX, TXT, MD
- **Images**: JPG, JPEG, PNG
- **Data**: CSV, XLSX, JSON
- **Communications**: EML, MSG

### Evidence Indexing
Each evidence file is cataloged with:
- File path and name
- File type and size
- Modification timestamp
- Repository source
- Evidence level classification

## Cross-Repository Analysis

### Entity Resolution
- **Name Matching**: Exact and fuzzy name matching
- **Property Correlation**: Common property value matching  
- **Evidence Linking**: Shared evidence reference matching
- **Temporal Correlation**: Timeline-based relationship inference

### Link Strength Calculation
- **0.8-1.0**: Exact name match + property overlap
- **0.6-0.8**: Fuzzy name match + evidence correlation
- **0.3-0.6**: Property overlap + temporal proximity
- **0.1-0.3**: Weak similarity indicators

## Performance Optimization

### Repository Scanning
- Parallel file system traversal
- Lazy loading of file contents
- Incremental scanning for updates
- Caching of scan results

### Schema Loading
- Batch entity/relation loading
- Memory-efficient JSON parsing
- Progress reporting for large repositories
- Error handling and recovery

### Cross-Repository Linking
- Efficient similarity algorithms
- Configurable similarity thresholds
- Pruning of low-confidence links
- Link strength optimization

## Error Handling

### Common Error Scenarios
1. **Repository Not Found**: Invalid repository name or path
2. **File Parsing Errors**: Malformed JSON or unsupported formats
3. **Schema Conflicts**: Duplicate IDs or invalid entity types
4. **Memory Limits**: Large repository processing
5. **Permission Issues**: Inaccessible files or directories

### Error Recovery
- Graceful degradation for partial failures
- Detailed error logging and reporting
- Retry mechanisms for transient failures
- Fallback entity type assignment

## Integration Points

### Existing Framework Integration
- **HyperGraphQL**: Extended with AD hypergraph resolvers
- **Evidence Refinery**: Cross-repository evidence correlation
- **OpenCog**: AtomSpace integration for advanced reasoning
- **GGML**: Performance optimization for large datasets

### External System Integration
- **GitHub API**: Future integration for remote repository access
- **Database Sync**: Synchronization with Supabase and Neon
- **Export Formats**: JSON, GraphML, RDF support
- **Visualization**: Integration with hypergraph visualization tools

## Security Considerations

### Data Protection
- Repository access control validation
- Sensitive data filtering and masking
- Audit trail for cross-repository operations
- Compliance with legal evidence handling requirements

### Privacy Safeguards
- Anonymization of personal identifiers
- Configurable data retention policies
- Secure temporary file handling
- Encrypted data transmission for remote repositories

## Future Enhancements

### Planned Features
1. **GitHub API Integration**: Direct access to remote repositories
2. **Real-time Synchronization**: Live updates from repository changes
3. **Advanced Entity Resolution**: ML-powered entity matching
4. **Temporal Analysis**: Timeline-based cross-repository analysis
5. **Visualization Dashboard**: Interactive hypergraph exploration
6. **Automated Evidence Discovery**: AI-powered evidence identification

### Scalability Improvements
- **Distributed Processing**: Multi-node repository scanning
- **Incremental Updates**: Change-based synchronization
- **Compression Algorithms**: Efficient storage for large hypergraphs
- **Query Optimization**: Fast cross-repository queries

## Testing and Validation

### Test Coverage
- Unit tests for core components
- Integration tests for CLI commands
- End-to-end tests for complete workflows
- Performance benchmarks for large repositories

### Validation Procedures
- Repository configuration validation
- Entity/relation schema validation
- Cross-repository link quality assessment
- Export data integrity verification

## Monitoring and Metrics

### Key Performance Indicators
- Repository scanning time
- Entity/relation loading throughput
- Cross-repository link accuracy
- Memory usage and optimization
- Error rates and recovery times

### Logging and Debugging
- Structured logging with correlation IDs
- Performance profiling for bottlenecks
- Debug mode with verbose output
- Export operation audit trails

This documentation provides comprehensive coverage of the AD Hypergraph Repository Mapping system, enabling effective cross-repository analysis for legal case investigation and evidence correlation.