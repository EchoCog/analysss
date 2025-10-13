# Analysis Framework API Documentation

## Overview

The Analysis Framework provides a comprehensive REST API for managing criminal case analysis, evidence processing, and hypergraph-based relationship mapping.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

Currently, the API uses basic authentication. Include your credentials in the request headers:

```
Authorization: Bearer <your-api-key>
```

## Endpoints

### Cases

#### GET /cases
Retrieve all cases with optional filtering.

**Parameters:**
- `status` (optional): Filter by case status (active, completed, pending, archived)
- `priority` (optional): Filter by priority (low, medium, high, critical)
- `limit` (optional): Maximum number of results (default: 50)
- `offset` (optional): Number of results to skip (default: 0)

**Response:**
```json
{
  "cases": [
    {
      "id": "case_001",
      "title": "Investigation Alpha",
      "description": "Complex fraud investigation",
      "status": "active",
      "priority": "high",
      "created_at": "2025-01-01T00:00:00Z",
      "entity_count": 15,
      "evidence_count": 23,
      "event_count": 8
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

#### POST /cases
Create a new case.

**Request Body:**
```json
{
  "title": "New Investigation",
  "description": "Description of the case",
  "priority": "medium",
  "case_type": "criminal",
  "jurisdiction": "Federal",
  "assigned_investigator": "Agent Smith"
}
```

#### GET /cases/{case_id}
Retrieve a specific case by ID.

#### PUT /cases/{case_id}
Update an existing case.

#### DELETE /cases/{case_id}
Delete a case and all associated data.

### Entities

#### GET /cases/{case_id}/entities
Retrieve all entities for a specific case.

**Parameters:**
- `type` (optional): Filter by entity type (person, organization, location, event, evidence, document)
- `verification_status` (optional): Filter by verification status

#### POST /cases/{case_id}/entities
Create a new entity for a case.

**Request Body:**
```json
{
  "name": "John Doe",
  "type": "person",
  "properties": {
    "age": 35,
    "occupation": "Accountant",
    "address": "123 Main St"
  },
  "confidence_score": 0.95
}
```

#### GET /entities/{entity_id}
Retrieve a specific entity.

#### PUT /entities/{entity_id}
Update an entity.

#### DELETE /entities/{entity_id}
Delete an entity.

### Evidence

#### GET /cases/{case_id}/evidence
Retrieve all evidence for a case.

#### POST /cases/{case_id}/evidence
Upload new evidence.

**Request Body (multipart/form-data):**
- `file`: Evidence file
- `name`: Evidence name
- `type`: Evidence type
- `metadata`: JSON metadata

#### GET /evidence/{evidence_id}
Retrieve specific evidence.

#### GET /evidence/{evidence_id}/download
Download evidence file.

### Analysis

#### POST /cases/{case_id}/analyze
Start analysis for a case.

**Request Body:**
```json
{
  "analysis_type": "hypergraph_generation",
  "parameters": {
    "include_entities": true,
    "include_relationships": true,
    "confidence_threshold": 0.7
  }
}
```

#### GET /analysis/{analysis_id}
Get analysis status and results.

#### GET /cases/{case_id}/analysis
Get all analysis results for a case.

### Relationships

#### GET /cases/{case_id}/relationships
Retrieve entity relationships for a case.

#### POST /cases/{case_id}/relationships
Create a new relationship between entities.

**Request Body:**
```json
{
  "source_entity_id": "entity_001",
  "target_entity_id": "entity_002",
  "relationship_type": "knows",
  "strength": 0.8,
  "confidence": 0.9,
  "evidence_ids": ["evidence_001", "evidence_002"]
}
```

### Timeline

#### GET /cases/{case_id}/timeline
Retrieve timeline events for a case.

**Parameters:**
- `start_date` (optional): Filter events after this date
- `end_date` (optional): Filter events before this date
- `event_type` (optional): Filter by event type

#### POST /cases/{case_id}/timeline
Create a new timeline event.

**Request Body:**
```json
{
  "event_date": "2025-01-15T14:30:00Z",
  "event_type": "meeting",
  "description": "Suspect meeting with accomplice",
  "location": "Downtown Cafe",
  "participants": ["entity_001", "entity_002"],
  "evidence_ids": ["evidence_003"],
  "confidence": 0.85
}
```

### Communication Tracking

#### GET /cases/{case_id}/communications
Retrieve communication events for verification tracking.

#### POST /cases/{case_id}/communications
Record a new communication event.

**Request Body:**
```json
{
  "event_date": "2025-01-10T09:00:00Z",
  "sender": "John Doe",
  "intended_recipient": "Jane Smith",
  "actual_recipient": "Jane Smith",
  "channel": "john@example.com",
  "channel_type": "email",
  "content_summary": "Meeting arrangement",
  "verification_status": "confirmed"
}
```

### Hypergraph

#### GET /cases/{case_id}/hypergraph
Retrieve hypergraph data for a case.

**Response:**
```json
{
  "nodes": [
    {
      "id": "node_001",
      "type": "person",
      "data": {"name": "John Doe"},
      "weight": 1.0
    }
  ],
  "edges": [
    {
      "id": "edge_001",
      "type": "communication",
      "node_ids": ["node_001", "node_002"],
      "weight": 0.8
    }
  ]
}
```

#### POST /cases/{case_id}/hypergraph/generate
Generate hypergraph representation for a case.

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server error

Error responses include details:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid entity type",
    "details": {
      "field": "type",
      "allowed_values": ["person", "organization", "location"]
    }
  }
}
```

## Rate Limiting

API requests are limited to:
- 1000 requests per hour for authenticated users
- 100 requests per hour for unauthenticated users

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Request limit per hour
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Time when limit resets

## Webhooks

Configure webhooks to receive notifications for:
- Analysis completion
- Evidence processing completion
- Case status changes

**Webhook Payload Example:**
```json
{
  "event": "analysis.completed",
  "case_id": "case_001",
  "analysis_id": "analysis_001",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "status": "completed",
    "results_url": "/api/v1/analysis/analysis_001"
  }
}
```

## SDK and Libraries

Official SDKs are available for:
- Python: `pip install rzonedevops-analysis-sdk`
- JavaScript/Node.js: `npm install @rzonedevops/analysis-sdk`
- R: `install.packages("rzonedevops.analysis")`

## Examples

### Python SDK Example

```python
from rzonedevops_analysis import AnalysisClient

client = AnalysisClient(api_key="your-api-key")

# Create a new case
case = client.cases.create(
    title="Investigation Beta",
    description="Financial fraud case",
    priority="high"
)

# Add an entity
entity = client.entities.create(
    case_id=case.id,
    name="Suspect Alpha",
    type="person",
    properties={"age": 42, "occupation": "CFO"}
)

# Start analysis
analysis = client.analysis.start(
    case_id=case.id,
    analysis_type="hypergraph_generation"
)

# Wait for completion and get results
results = client.analysis.wait_for_completion(analysis.id)
print(f"Analysis completed: {results.status}")
```

### cURL Examples

```bash
# Create a case
curl -X POST http://localhost:5000/api/v1/cases \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Investigation Gamma",
    "description": "Cybercrime investigation",
    "priority": "critical"
  }'

# Upload evidence
curl -X POST http://localhost:5000/api/v1/cases/case_001/evidence \
  -H "Authorization: Bearer your-api-key" \
  -F "file=@evidence.pdf" \
  -F "name=Financial Records" \
  -F "type=document"

# Get hypergraph data
curl -X GET http://localhost:5000/api/v1/cases/case_001/hypergraph \
  -H "Authorization: Bearer your-api-key"
```

## Support

For API support and questions:
- Documentation: https://docs.rzonedevops.com/analysis
- Issues: https://github.com/rzonedevops/analysis/issues
- Email: api-support@rzonedevops.com
