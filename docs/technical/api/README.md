# API Documentation

## Overview

This directory contains API documentation for REST and GraphQL interfaces,
including endpoint references, request/response schemas, and integration guides.

## API Types

### REST API
Standard RESTful API for CRUD operations and system interaction.

**Base URL:** `/api/v1/`

**Main Documentation:**
- [API_DOCUMENTATION.md](../../../API_DOCUMENTATION.md) - Complete REST API reference

### GraphQL API
HyperGraphQL API for complex queries and org-aware operations.

**Endpoint:** `/graphql`

**Main Documentation:**
- [HYPERGRAPHQL_API_DOCUMENTATION.md](../../../HYPERGRAPHQL_API_DOCUMENTATION.md) - GraphQL reference

## REST API Endpoints

### Cases Management
```
GET    /api/v1/cases              # List all cases
POST   /api/v1/cases              # Create new case
GET    /api/v1/cases/{id}         # Get case details
PUT    /api/v1/cases/{id}         # Update case
DELETE /api/v1/cases/{id}         # Delete case
```

### Evidence Management
```
GET    /api/v1/cases/{id}/evidence           # List evidence
POST   /api/v1/cases/{id}/evidence           # Upload evidence
GET    /api/v1/evidence/{id}                 # Get evidence
GET    /api/v1/evidence/{id}/download        # Download evidence
PUT    /api/v1/evidence/{id}                 # Update evidence
DELETE /api/v1/evidence/{id}                 # Delete evidence
```

### Timeline Management
```
GET    /api/v1/cases/{id}/timeline           # Get timeline
POST   /api/v1/cases/{id}/timeline/entries   # Add entry
PUT    /api/v1/timeline/entries/{id}         # Update entry
DELETE /api/v1/timeline/entries/{id}         # Delete entry
```

### Analysis Operations
```
POST   /api/v1/cases/{id}/analyze            # Start analysis
GET    /api/v1/analysis/{id}                 # Get analysis status
GET    /api/v1/cases/{id}/analysis           # List analyses
```

### Entity Management
```
GET    /api/v1/cases/{id}/entities           # List entities
POST   /api/v1/cases/{id}/entities           # Create entity
GET    /api/v1/entities/{id}                 # Get entity
PUT    /api/v1/entities/{id}                 # Update entity
DELETE /api/v1/entities/{id}                 # Delete entity
```

### Relationship Management
```
GET    /api/v1/cases/{id}/relationships      # List relationships
POST   /api/v1/cases/{id}/relationships      # Create relationship
GET    /api/v1/relationships/{id}            # Get relationship
PUT    /api/v1/relationships/{id}            # Update relationship
DELETE /api/v1/relationships/{id}            # Delete relationship
```

## GraphQL Schema

### Types
```graphql
type Case {
  id: ID!
  title: String!
  description: String
  status: CaseStatus!
  entities: [Entity!]!
  evidence: [Evidence!]!
  timeline: Timeline!
}

type Entity {
  id: ID!
  name: String!
  type: EntityType!
  attributes: JSON
  relationships: [Relationship!]!
}

type Evidence {
  id: ID!
  title: String!
  type: EvidenceType!
  classification: Classification!
  verificationStatus: VerificationStatus!
}

type Timeline {
  entries: [TimelineEntry!]!
  gaps: [TimelineGap!]!
}
```

### Queries
```graphql
query {
  case(id: "case_001") {
    title
    entities {
      name
      type
    }
    evidence {
      title
      verificationStatus
    }
  }
}

query {
  searchEntities(
    caseId: "case_001"
    query: "name:Smith"
  ) {
    name
    relationships {
      target {
        name
      }
      type
    }
  }
}
```

### Mutations
```graphql
mutation {
  createCase(input: {
    title: "New Investigation"
    description: "Case description"
    priority: HIGH
  }) {
    id
    title
  }
}

mutation {
  addEvidence(input: {
    caseId: "case_001"
    title: "Document A"
    type: DOCUMENT
    file: "file_upload"
  }) {
    id
    title
  }
}
```

## Authentication

### API Key Authentication
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.example.com/api/v1/cases
```

### JWT Token Authentication
```bash
# Get token
curl -X POST https://api.example.com/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"user","password":"pass"}'

# Use token
curl -H "Authorization: Bearer JWT_TOKEN" \
     https://api.example.com/api/v1/cases
```

## Request/Response Formats

### Standard Response Format
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2025-10-11T00:00:00Z"
}
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Case not found",
    "details": { ... }
  },
  "timestamp": "2025-10-11T00:00:00Z"
}
```

## Rate Limiting

- **Default**: 100 requests per minute
- **Authenticated**: 1000 requests per minute
- **Enterprise**: Custom limits

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1633046400
```

## Pagination

### Query Parameters
- `limit`: Results per page (default: 50, max: 100)
- `offset`: Number to skip (default: 0)
- `page`: Page number (alternative to offset)

### Response Format
```json
{
  "data": [ ... ],
  "pagination": {
    "total": 150,
    "limit": 50,
    "offset": 0,
    "hasNext": true,
    "hasPrevious": false
  }
}
```

## Filtering and Sorting

### Filtering
```
GET /api/v1/cases?status=active&priority=high
```

### Sorting
```
GET /api/v1/cases?sort=created_at&direction=desc
```

### Search
```
GET /api/v1/cases/search?q=keyword
```

## WebSocket API

### Connection
```javascript
const ws = new WebSocket('wss://api.example.com/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'case_updates',
    caseId: 'case_001'
  }));
};

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('Update:', update);
};
```

### Events
- `case_created`
- `case_updated`
- `evidence_added`
- `analysis_complete`
- `timeline_updated`

## Best Practices

### Request Best Practices
1. Use appropriate HTTP methods
2. Include proper headers
3. Validate input data
4. Handle errors gracefully
5. Implement retry logic

### Performance Best Practices
1. Use pagination for large datasets
2. Cache frequently accessed data
3. Batch related requests
4. Use appropriate filters
5. Monitor rate limits

### Security Best Practices
1. Always use HTTPS
2. Validate authentication tokens
3. Sanitize input data
4. Implement CSRF protection
5. Log security events

## Testing

### cURL Examples
See [API_DOCUMENTATION.md](../../../API_DOCUMENTATION.md) for complete examples.

### Postman Collection
Available at: `/docs/technical/api/postman_collection.json`

### API Testing Scripts
```bash
python tests/api/test_api_endpoints.py
```

## Integration Guides

1. **Getting Started**: Basic integration setup
2. **Authentication**: Setting up auth
3. **Common Workflows**: Typical use cases
4. **Error Handling**: Handling errors
5. **Advanced Features**: Complex queries

## Support

- **Documentation**: This directory
- **API Reference**: Main API docs
- **Examples**: Example code
- **Issues**: GitHub issues
- **Contact**: Support team

## Versioning

Current version: **v1**

- Breaking changes increment major version
- New features increment minor version
- Bug fixes increment patch version

## Changelog

See [CHANGELOG.md](../../../CHANGELOG.md) for API changes.
