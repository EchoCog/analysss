"""
Relationship Inference Engine
=============================

Improvements implemented:
1. Dynamic relationship inference from entity interactions
2. Relationship type hierarchy and ontology
3. Confidence scoring for inferred relationships
4. Temporal relationship tracking
5. Relationship pattern detection
6. Relationship validation framework
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from pydantic import BaseModel, Field


class RelationshipType(str, Enum):
    """Hierarchical relationship types"""
    # Primary types
    COMMUNICATION = "communication"
    TRANSACTION = "transaction"
    COLLABORATION = "collaboration"
    CONFLICT = "conflict"
    HIERARCHY = "hierarchy"
    
    # Communication subtypes
    EMAIL = "email"
    PHONE = "phone"
    MEETING = "meeting"
    MESSAGE = "message"
    
    # Transaction subtypes
    FINANCIAL = "financial"
    RESOURCE = "resource"
    INFORMATION = "information"
    
    # Collaboration subtypes
    PARTNERSHIP = "partnership"
    EMPLOYMENT = "employment"
    MEMBERSHIP = "membership"
    
    # Conflict subtypes
    LEGAL = "legal"
    COMPETITIVE = "competitive"
    ADVERSARIAL = "adversarial"
    
    # Hierarchy subtypes
    OWNERSHIP = "ownership"
    MANAGEMENT = "management"
    SUPERVISION = "supervision"


class InferenceMethod(str, Enum):
    """Methods used for relationship inference"""
    DIRECT_EVIDENCE = "direct_evidence"
    CO_OCCURRENCE = "co_occurrence"
    TEMPORAL_PROXIMITY = "temporal_proximity"
    TRANSITIVE = "transitive"
    PATTERN_BASED = "pattern_based"
    ML_PREDICTION = "ml_prediction"


class RelationshipOntology:
    """Defines relationship type hierarchy and rules"""
    
    # Parent-child relationships in the ontology
    HIERARCHY = {
        RelationshipType.COMMUNICATION: [
            RelationshipType.EMAIL,
            RelationshipType.PHONE,
            RelationshipType.MEETING,
            RelationshipType.MESSAGE
        ],
        RelationshipType.TRANSACTION: [
            RelationshipType.FINANCIAL,
            RelationshipType.RESOURCE,
            RelationshipType.INFORMATION
        ],
        RelationshipType.COLLABORATION: [
            RelationshipType.PARTNERSHIP,
            RelationshipType.EMPLOYMENT,
            RelationshipType.MEMBERSHIP
        ],
        RelationshipType.CONFLICT: [
            RelationshipType.LEGAL,
            RelationshipType.COMPETITIVE,
            RelationshipType.ADVERSARIAL
        ],
        RelationshipType.HIERARCHY: [
            RelationshipType.OWNERSHIP,
            RelationshipType.MANAGEMENT,
            RelationshipType.SUPERVISION
        ]
    }
    
    # Mutually exclusive relationship types
    EXCLUSIVE_PAIRS = [
        (RelationshipType.COLLABORATION, RelationshipType.CONFLICT),
        (RelationshipType.PARTNERSHIP, RelationshipType.ADVERSARIAL)
    ]
    
    # Relationship type weights for inference
    TYPE_WEIGHTS = {
        RelationshipType.OWNERSHIP: 1.0,
        RelationshipType.EMPLOYMENT: 0.9,
        RelationshipType.FINANCIAL: 0.8,
        RelationshipType.LEGAL: 0.8,
        RelationshipType.MEETING: 0.6,
        RelationshipType.EMAIL: 0.5,
        RelationshipType.MESSAGE: 0.4
    }
    
    @classmethod
    def get_parent_type(cls, relationship_type: RelationshipType) -> Optional[RelationshipType]:
        """Get the parent type of a relationship"""
        for parent, children in cls.HIERARCHY.items():
            if relationship_type in children:
                return parent
        return None
    
    @classmethod
    def get_children_types(cls, relationship_type: RelationshipType) -> List[RelationshipType]:
        """Get child types of a relationship"""
        return cls.HIERARCHY.get(relationship_type, [])
    
    @classmethod
    def are_compatible(cls, type1: RelationshipType, type2: RelationshipType) -> bool:
        """Check if two relationship types are compatible"""
        for pair in cls.EXCLUSIVE_PAIRS:
            if (type1 in pair and type2 in pair):
                return False
        return True


class InferredRelationship(BaseModel):
    """Represents an inferred relationship with confidence scoring"""
    
    relationship_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: RelationshipType
    
    # Inference metadata
    inference_method: InferenceMethod
    confidence_score: float = Field(ge=0.0, le=1.0)
    supporting_evidence: List[str] = Field(default_factory=list)
    inference_timestamp: datetime = Field(default_factory=datetime.now)
    
    # Temporal tracking
    first_observed: Optional[datetime] = None
    last_observed: Optional[datetime] = None
    observation_count: int = 0
    
    # Validation
    validated: bool = False
    validation_timestamp: Optional[datetime] = None
    validation_notes: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RelationshipPattern(BaseModel):
    """Represents a detected relationship pattern"""
    
    pattern_id: str
    pattern_type: str
    entities_involved: List[str]
    relationships: List[str]
    pattern_strength: float = Field(ge=0.0, le=1.0)
    detected_at: datetime = Field(default_factory=datetime.now)
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RelationshipInferenceEngine:
    """Engine for inferring and managing relationships"""
    
    def __init__(self):
        self.inferred_relationships: Dict[str, InferredRelationship] = {}
        self.detected_patterns: Dict[str, RelationshipPattern] = {}
        self.ontology = RelationshipOntology()
        
        # Inference parameters
        self.co_occurrence_threshold = 3
        self.temporal_window_hours = 24
        self.min_confidence_threshold = 0.3
    
    def infer_from_co_occurrence(self, entity_id1: str, entity_id2: str, 
                                 events: List[Dict[str, Any]]) -> Optional[InferredRelationship]:
        """Infer relationship from entity co-occurrence in events"""
        
        # Count co-occurrences
        co_occurrences = 0
        event_ids = []
        
        for event in events:
            participants = event.get('participants', [])
            if entity_id1 in participants and entity_id2 in participants:
                co_occurrences += 1
                event_ids.append(event.get('event_id'))
        
        # Infer relationship if threshold met
        if co_occurrences >= self.co_occurrence_threshold:
            confidence = min(co_occurrences / 10.0, 1.0)  # Cap at 1.0
            
            relationship = InferredRelationship(
                relationship_id=f"inferred_{entity_id1}_{entity_id2}_{datetime.now().timestamp()}",
                source_entity_id=entity_id1,
                target_entity_id=entity_id2,
                relationship_type=RelationshipType.COLLABORATION,  # Default type
                inference_method=InferenceMethod.CO_OCCURRENCE,
                confidence_score=confidence,
                supporting_evidence=event_ids,
                observation_count=co_occurrences
            )
            
            self.inferred_relationships[relationship.relationship_id] = relationship
            return relationship
        
        return None
    
    def infer_from_temporal_proximity(self, entity_id1: str, entity_id2: str,
                                     events: List[Dict[str, Any]]) -> Optional[InferredRelationship]:
        """Infer relationship from temporal proximity of entity activities"""
        
        # Get events for each entity
        entity1_events = [e for e in events if entity_id1 in e.get('participants', [])]
        entity2_events = [e for e in events if entity_id2 in e.get('participants', [])]
        
        # Find temporally close events
        close_events = []
        for e1 in entity1_events:
            e1_time = datetime.fromisoformat(e1['timestamp']) if 'timestamp' in e1 else None
            if not e1_time:
                continue
                
            for e2 in entity2_events:
                e2_time = datetime.fromisoformat(e2['timestamp']) if 'timestamp' in e2 else None
                if not e2_time:
                    continue
                
                time_diff = abs((e1_time - e2_time).total_seconds() / 3600)  # hours
                if time_diff <= self.temporal_window_hours:
                    close_events.append((e1['event_id'], e2['event_id'], time_diff))
        
        # Infer relationship if significant temporal proximity
        if len(close_events) >= 2:
            avg_time_diff = sum(diff for _, _, diff in close_events) / len(close_events)
            confidence = max(0.3, 1.0 - (avg_time_diff / self.temporal_window_hours))
            
            relationship = InferredRelationship(
                relationship_id=f"inferred_{entity_id1}_{entity_id2}_{datetime.now().timestamp()}",
                source_entity_id=entity_id1,
                target_entity_id=entity_id2,
                relationship_type=RelationshipType.COMMUNICATION,
                inference_method=InferenceMethod.TEMPORAL_PROXIMITY,
                confidence_score=confidence,
                supporting_evidence=[f"{e1}_{e2}" for e1, e2, _ in close_events],
                observation_count=len(close_events)
            )
            
            self.inferred_relationships[relationship.relationship_id] = relationship
            return relationship
        
        return None
    
    def infer_transitive_relationships(self, relationships: List[Dict[str, Any]]) -> List[InferredRelationship]:
        """Infer transitive relationships (if A->B and B->C, then A->C)"""
        
        inferred = []
        
        # Build relationship graph
        graph = {}
        for rel in relationships:
            source = rel['source_entity_id']
            target = rel['target_entity_id']
            rel_type = rel['relationship_type']
            
            if source not in graph:
                graph[source] = []
            graph[source].append((target, rel_type))
        
        # Find transitive relationships
        for entity_a in graph:
            for entity_b, type_ab in graph.get(entity_a, []):
                for entity_c, type_bc in graph.get(entity_b, []):
                    if entity_a != entity_c:
                        # Infer A->C relationship
                        # Confidence decreases with transitivity
                        confidence = 0.5
                        
                        relationship = InferredRelationship(
                            relationship_id=f"transitive_{entity_a}_{entity_c}_{datetime.now().timestamp()}",
                            source_entity_id=entity_a,
                            target_entity_id=entity_c,
                            relationship_type=type_ab,  # Use first relationship type
                            inference_method=InferenceMethod.TRANSITIVE,
                            confidence_score=confidence,
                            supporting_evidence=[f"{entity_a}->{entity_b}->{entity_c}"]
                        )
                        
                        inferred.append(relationship)
                        self.inferred_relationships[relationship.relationship_id] = relationship
        
        return inferred
    
    def detect_relationship_patterns(self, relationships: List[Dict[str, Any]]) -> List[RelationshipPattern]:
        """Detect patterns in relationships"""
        
        patterns = []
        
        # Pattern 1: Triangular relationships (A-B, B-C, C-A)
        triangles = self._detect_triangles(relationships)
        for triangle in triangles:
            pattern = RelationshipPattern(
                pattern_id=f"triangle_{datetime.now().timestamp()}",
                pattern_type="triangle",
                entities_involved=triangle['entities'],
                relationships=triangle['relationships'],
                pattern_strength=triangle['strength'],
                description=f"Triangular relationship between {', '.join(triangle['entities'])}"
            )
            patterns.append(pattern)
            self.detected_patterns[pattern.pattern_id] = pattern
        
        # Pattern 2: Star patterns (one central entity connected to many)
        stars = self._detect_star_patterns(relationships)
        for star in stars:
            pattern = RelationshipPattern(
                pattern_id=f"star_{datetime.now().timestamp()}",
                pattern_type="star",
                entities_involved=star['entities'],
                relationships=star['relationships'],
                pattern_strength=star['strength'],
                description=f"Star pattern with {star['center']} at center"
            )
            patterns.append(pattern)
            self.detected_patterns[pattern.pattern_id] = pattern
        
        # Pattern 3: Chain patterns (A->B->C->D)
        chains = self._detect_chains(relationships)
        for chain in chains:
            pattern = RelationshipPattern(
                pattern_id=f"chain_{datetime.now().timestamp()}",
                pattern_type="chain",
                entities_involved=chain['entities'],
                relationships=chain['relationships'],
                pattern_strength=chain['strength'],
                description=f"Chain pattern: {' -> '.join(chain['entities'])}"
            )
            patterns.append(pattern)
            self.detected_patterns[pattern.pattern_id] = pattern
        
        return patterns
    
    def _detect_triangles(self, relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect triangular relationship patterns"""
        triangles = []
        
        # Build adjacency list
        graph = {}
        for rel in relationships:
            source = rel['source_entity_id']
            target = rel['target_entity_id']
            
            if source not in graph:
                graph[source] = set()
            graph[source].add(target)
        
        # Find triangles
        for a in graph:
            for b in graph.get(a, set()):
                for c in graph.get(b, set()):
                    if a in graph.get(c, set()):
                        triangles.append({
                            'entities': [a, b, c],
                            'relationships': [f"{a}->{b}", f"{b}->{c}", f"{c}->{a}"],
                            'strength': 0.8
                        })
        
        return triangles
    
    def _detect_star_patterns(self, relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect star relationship patterns"""
        stars = []
        
        # Count connections for each entity
        connections = {}
        for rel in relationships:
            source = rel['source_entity_id']
            target = rel['target_entity_id']
            
            connections[source] = connections.get(source, 0) + 1
            connections[target] = connections.get(target, 0) + 1
        
        # Find entities with many connections (hubs)
        for entity, count in connections.items():
            if count >= 5:  # Threshold for star pattern
                connected_entities = set()
                rel_ids = []
                
                for rel in relationships:
                    if rel['source_entity_id'] == entity:
                        connected_entities.add(rel['target_entity_id'])
                        rel_ids.append(rel.get('relationship_id', ''))
                    elif rel['target_entity_id'] == entity:
                        connected_entities.add(rel['source_entity_id'])
                        rel_ids.append(rel.get('relationship_id', ''))
                
                stars.append({
                    'center': entity,
                    'entities': [entity] + list(connected_entities),
                    'relationships': rel_ids,
                    'strength': min(count / 10.0, 1.0)
                })
        
        return stars
    
    def _detect_chains(self, relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect chain relationship patterns"""
        chains = []
        
        # Build directed graph
        graph = {}
        for rel in relationships:
            source = rel['source_entity_id']
            target = rel['target_entity_id']
            
            if source not in graph:
                graph[source] = []
            graph[source].append(target)
        
        # Find chains of length >= 3
        for start in graph:
            self._find_chains_from(start, graph, [], chains)
        
        return chains
    
    def _find_chains_from(self, current: str, graph: Dict, path: List[str], 
                         chains: List[Dict[str, Any]], max_depth: int = 5):
        """Recursively find chains from a starting node"""
        path = path + [current]
        
        if len(path) >= 3:
            chains.append({
                'entities': path.copy(),
                'relationships': [f"{path[i]}->{path[i+1]}" for i in range(len(path)-1)],
                'strength': 0.6
            })
        
        if len(path) < max_depth:
            for next_node in graph.get(current, []):
                if next_node not in path:  # Avoid cycles
                    self._find_chains_from(next_node, graph, path, chains, max_depth)
    
    def validate_relationship(self, relationship_id: str, validated: bool, 
                            notes: Optional[str] = None) -> bool:
        """Validate an inferred relationship"""
        relationship = self.inferred_relationships.get(relationship_id)
        if relationship:
            relationship.validated = validated
            relationship.validation_timestamp = datetime.now()
            relationship.validation_notes = notes
            return True
        return False
    
    def get_high_confidence_relationships(self, min_confidence: float = 0.7) -> List[InferredRelationship]:
        """Get relationships with confidence above threshold"""
        return [
            rel for rel in self.inferred_relationships.values()
            if rel.confidence_score >= min_confidence
        ]
    
    def export_relationships(self) -> List[Dict[str, Any]]:
        """Export all inferred relationships"""
        return [rel.dict() for rel in self.inferred_relationships.values()]

