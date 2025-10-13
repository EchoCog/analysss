"""
Enhanced Entity Model with Validation and Lifecycle Management
===============================================================

Improvements implemented:
1. Pydantic validation for entity properties
2. Entity lifecycle management (create, update, delete, archive)
3. Temporal versioning for entity state changes
4. Entity relationship graph builder
5. Entity similarity metrics
6. Entity serialization/deserialization
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

import numpy as np
from pydantic import BaseModel, Field, validator


class EntityType(str, Enum):
    """Types of entities in the system"""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    EVENT = "event"
    DOCUMENT = "document"
    RESOURCE = "resource"
    AGENT = "agent"


class EntityStatus(str, Enum):
    """Lifecycle status of entities"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DELETED = "deleted"
    PENDING = "pending"


class EntityVersion(BaseModel):
    """Represents a version of an entity at a specific point in time"""
    version_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    properties: Dict[str, Any] = Field(default_factory=dict)
    changed_by: Optional[str] = None
    change_reason: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class EntityRelationship(BaseModel):
    """Represents a relationship between two entities"""
    relationship_id: str = Field(default_factory=lambda: str(uuid4()))
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    strength: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence_refs: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @validator('strength', 'confidence')
    def validate_score(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Score must be between 0.0 and 1.0')
        return v


class EnhancedEntity(BaseModel):
    """Enhanced entity model with validation and lifecycle management"""
    
    # Core properties
    entity_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., min_length=1, max_length=500)
    entity_type: EntityType
    status: EntityStatus = Field(default=EntityStatus.ACTIVE)
    
    # Descriptive properties
    description: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    tags: Set[str] = Field(default_factory=set)
    
    # Behavioral properties (for agent-based modeling)
    behavioral_properties: Dict[str, float] = Field(default_factory=dict)
    strategic_goals: List[str] = Field(default_factory=list)
    behavioral_rules: List[str] = Field(default_factory=list)
    
    # State management
    current_state: Dict[str, Any] = Field(default_factory=dict)
    
    # Temporal tracking
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    archived_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    # Versioning
    version_history: List[EntityVersion] = Field(default_factory=list)
    current_version: int = Field(default=1)
    
    # Relationships
    relationships: List[EntityRelationship] = Field(default_factory=list)
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            set: lambda v: list(v)
        }
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Entity name cannot be empty')
        return v.strip()
    
    @validator('behavioral_properties')
    def validate_behavioral_properties(cls, v):
        for key, value in v.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f'Behavioral property {key} must be numeric')
            if not 0.0 <= value <= 1.0:
                raise ValueError(f'Behavioral property {key} must be between 0.0 and 1.0')
        return v
    
    def create_version(self, changed_by: Optional[str] = None, change_reason: Optional[str] = None):
        """Create a new version of the entity"""
        version = EntityVersion(
            timestamp=datetime.now(),
            properties={
                "name": self.name,
                "entity_type": self.entity_type.value,
                "status": self.status.value,
                "description": self.description,
                "behavioral_properties": self.behavioral_properties.copy(),
                "current_state": self.current_state.copy(),
            },
            changed_by=changed_by,
            change_reason=change_reason
        )
        self.version_history.append(version)
        self.current_version += 1
        self.updated_at = datetime.now()
    
    def update_property(self, property_name: str, value: Any, changed_by: Optional[str] = None):
        """Update a property and create a version"""
        if hasattr(self, property_name):
            setattr(self, property_name, value)
            self.create_version(changed_by=changed_by, change_reason=f"Updated {property_name}")
        else:
            raise ValueError(f"Property {property_name} does not exist")
    
    def archive(self, reason: Optional[str] = None):
        """Archive the entity"""
        self.status = EntityStatus.ARCHIVED
        self.archived_at = datetime.now()
        self.create_version(change_reason=reason or "Entity archived")
    
    def delete(self, reason: Optional[str] = None):
        """Soft delete the entity"""
        self.status = EntityStatus.DELETED
        self.deleted_at = datetime.now()
        self.create_version(change_reason=reason or "Entity deleted")
    
    def restore(self):
        """Restore an archived or deleted entity"""
        self.status = EntityStatus.ACTIVE
        self.archived_at = None
        self.deleted_at = None
        self.create_version(change_reason="Entity restored")
    
    def add_relationship(self, target_entity_id: str, relationship_type: str, 
                        strength: float = 0.5, confidence: float = 0.5,
                        evidence_refs: Optional[List[str]] = None) -> EntityRelationship:
        """Add a relationship to another entity"""
        relationship = EntityRelationship(
            source_entity_id=self.entity_id,
            target_entity_id=target_entity_id,
            relationship_type=relationship_type,
            strength=strength,
            confidence=confidence,
            evidence_refs=evidence_refs or []
        )
        self.relationships.append(relationship)
        self.updated_at = datetime.now()
        return relationship
    
    def get_relationships_by_type(self, relationship_type: str) -> List[EntityRelationship]:
        """Get all relationships of a specific type"""
        return [r for r in self.relationships if r.relationship_type == relationship_type]
    
    def calculate_similarity(self, other: 'EnhancedEntity') -> float:
        """Calculate similarity score with another entity"""
        similarity_score = 0.0
        weight_sum = 0.0
        
        # Type similarity (weight: 0.3)
        if self.entity_type == other.entity_type:
            similarity_score += 0.3
        weight_sum += 0.3
        
        # Tag overlap (weight: 0.2)
        if self.tags and other.tags:
            tag_overlap = len(self.tags.intersection(other.tags)) / max(len(self.tags), len(other.tags))
            similarity_score += 0.2 * tag_overlap
        weight_sum += 0.2
        
        # Behavioral property similarity (weight: 0.3)
        if self.behavioral_properties and other.behavioral_properties:
            common_props = set(self.behavioral_properties.keys()).intersection(
                set(other.behavioral_properties.keys())
            )
            if common_props:
                prop_diff = sum(
                    abs(self.behavioral_properties[k] - other.behavioral_properties[k])
                    for k in common_props
                ) / len(common_props)
                similarity_score += 0.3 * (1 - prop_diff)
        weight_sum += 0.3
        
        # Relationship overlap (weight: 0.2)
        if self.relationships and other.relationships:
            self_targets = {r.target_entity_id for r in self.relationships}
            other_targets = {r.target_entity_id for r in other.relationships}
            if self_targets or other_targets:
                overlap = len(self_targets.intersection(other_targets)) / max(
                    len(self_targets), len(other_targets)
                )
                similarity_score += 0.2 * overlap
        weight_sum += 0.2
        
        return similarity_score / weight_sum if weight_sum > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary"""
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedEntity':
        """Create entity from dictionary"""
        return cls(**data)
    
    def export_to_json(self) -> str:
        """Export entity to JSON string"""
        return self.json(indent=2)
    
    @classmethod
    def import_from_json(cls, json_str: str) -> 'EnhancedEntity':
        """Import entity from JSON string"""
        return cls.parse_raw(json_str)


class EntityManager:
    """Manager for entity lifecycle and operations"""
    
    def __init__(self):
        self.entities: Dict[str, EnhancedEntity] = {}
        self.entity_index: Dict[str, Set[str]] = {
            "by_type": {},
            "by_status": {},
            "by_tag": {}
        }
    
    def create_entity(self, **kwargs) -> EnhancedEntity:
        """Create a new entity"""
        entity = EnhancedEntity(**kwargs)
        self.entities[entity.entity_id] = entity
        self._update_index(entity)
        return entity
    
    def get_entity(self, entity_id: str) -> Optional[EnhancedEntity]:
        """Get an entity by ID"""
        return self.entities.get(entity_id)
    
    def update_entity(self, entity_id: str, **kwargs) -> Optional[EnhancedEntity]:
        """Update an entity"""
        entity = self.get_entity(entity_id)
        if entity:
            for key, value in kwargs.items():
                entity.update_property(key, value)
            self._update_index(entity)
        return entity
    
    def delete_entity(self, entity_id: str, reason: Optional[str] = None) -> bool:
        """Delete an entity"""
        entity = self.get_entity(entity_id)
        if entity:
            entity.delete(reason)
            self._update_index(entity)
            return True
        return False
    
    def find_entities_by_type(self, entity_type: EntityType) -> List[EnhancedEntity]:
        """Find all entities of a specific type"""
        return [
            self.entities[eid] 
            for eid in self.entity_index["by_type"].get(entity_type.value, set())
        ]
    
    def find_entities_by_tag(self, tag: str) -> List[EnhancedEntity]:
        """Find all entities with a specific tag"""
        return [
            self.entities[eid] 
            for eid in self.entity_index["by_tag"].get(tag, set())
        ]
    
    def find_similar_entities(self, entity_id: str, threshold: float = 0.5) -> List[Tuple[EnhancedEntity, float]]:
        """Find entities similar to the given entity"""
        entity = self.get_entity(entity_id)
        if not entity:
            return []
        
        similar = []
        for other_id, other_entity in self.entities.items():
            if other_id != entity_id and other_entity.status == EntityStatus.ACTIVE:
                similarity = entity.calculate_similarity(other_entity)
                if similarity >= threshold:
                    similar.append((other_entity, similarity))
        
        return sorted(similar, key=lambda x: x[1], reverse=True)
    
    def build_relationship_graph(self) -> Dict[str, List[str]]:
        """Build a graph of entity relationships"""
        graph = {}
        for entity in self.entities.values():
            if entity.status == EntityStatus.ACTIVE:
                graph[entity.entity_id] = [
                    r.target_entity_id for r in entity.relationships
                ]
        return graph
    
    def _update_index(self, entity: EnhancedEntity):
        """Update entity indices"""
        # Index by type
        if entity.entity_type.value not in self.entity_index["by_type"]:
            self.entity_index["by_type"][entity.entity_type.value] = set()
        self.entity_index["by_type"][entity.entity_type.value].add(entity.entity_id)
        
        # Index by status
        if entity.status.value not in self.entity_index["by_status"]:
            self.entity_index["by_status"][entity.status.value] = set()
        self.entity_index["by_status"][entity.status.value].add(entity.entity_id)
        
        # Index by tags
        for tag in entity.tags:
            if tag not in self.entity_index["by_tag"]:
                self.entity_index["by_tag"][tag] = set()
            self.entity_index["by_tag"][tag].add(entity.entity_id)
    
    def export_all(self) -> List[Dict[str, Any]]:
        """Export all entities"""
        return [entity.to_dict() for entity in self.entities.values()]
    
    def import_all(self, entities_data: List[Dict[str, Any]]):
        """Import multiple entities"""
        for data in entities_data:
            entity = EnhancedEntity.from_dict(data)
            self.entities[entity.entity_id] = entity
            self._update_index(entity)

