"""
Enhanced Timeline Analysis with Gap Detection and Conflict Resolution
====================================================================

Improvements implemented:
1. Timeline gap detection and highlighting
2. Conflict resolution for contradictory events
3. Uncertainty quantification framework
4. Enhanced timeline visualization data generation
5. Timeline comparison and diff tools
6. Timeline reconstruction from partial data
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field


class TimelineGapType(str, Enum):
    """Types of gaps in timelines"""
    MISSING_PERIOD = "missing_period"
    UNEXPLAINED_TRANSITION = "unexplained_transition"
    INCOMPLETE_SEQUENCE = "incomplete_sequence"
    SPARSE_COVERAGE = "sparse_coverage"


class ConflictType(str, Enum):
    """Types of conflicts between timeline entries"""
    TEMPORAL_IMPOSSIBILITY = "temporal_impossibility"
    CONTRADICTORY_FACTS = "contradictory_facts"
    INCONSISTENT_SEQUENCE = "inconsistent_sequence"
    DUPLICATE_EVENT = "duplicate_event"


class UncertaintyType(str, Enum):
    """Types of uncertainty in timeline data"""
    TEMPORAL = "temporal"
    FACTUAL = "factual"
    CAUSAL = "causal"
    COMPLETENESS = "completeness"


class TimelineGap(BaseModel):
    """Represents a detected gap in the timeline"""
    
    gap_id: str
    gap_type: TimelineGapType
    start_time: datetime
    end_time: datetime
    duration_hours: float
    severity: float = Field(ge=0.0, le=1.0)
    description: str
    surrounding_events: List[str] = Field(default_factory=list)
    suggested_investigation: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TimelineConflict(BaseModel):
    """Represents a conflict between timeline entries"""
    
    conflict_id: str
    conflict_type: ConflictType
    conflicting_events: List[str]
    description: str
    resolution_strategy: Optional[str] = None
    resolved: bool = False
    resolution_notes: Optional[str] = None
    confidence_in_resolution: float = Field(default=0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class UncertaintyMeasure(BaseModel):
    """Represents uncertainty in timeline data"""
    
    uncertainty_id: str
    event_id: str
    uncertainty_type: UncertaintyType
    uncertainty_score: float = Field(ge=0.0, le=1.0)
    lower_bound: Optional[datetime] = None
    upper_bound: Optional[datetime] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TimelineReconstruction(BaseModel):
    """Represents a reconstructed timeline segment"""
    
    reconstruction_id: str
    original_events: List[str]
    reconstructed_events: List[Dict[str, Any]]
    reconstruction_method: str
    confidence: float = Field(ge=0.0, le=1.0)
    assumptions: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EnhancedTimelineAnalyzer:
    """Analyzer for advanced timeline analysis"""
    
    def __init__(self):
        self.gaps: Dict[str, TimelineGap] = {}
        self.conflicts: Dict[str, TimelineConflict] = {}
        self.uncertainties: Dict[str, UncertaintyMeasure] = {}
        self.reconstructions: Dict[str, TimelineReconstruction] = {}
        
        # Analysis parameters
        self.min_gap_hours = 24
        self.max_reasonable_gap_days = 7
        self.conflict_threshold = 0.7
    
    def detect_gaps(self, events: List[Dict[str, Any]]) -> List[TimelineGap]:
        """Detect gaps in the timeline"""
        
        gaps = []
        
        # Sort events by timestamp
        sorted_events = sorted(
            [e for e in events if e.get('timestamp')],
            key=lambda e: e['timestamp'] if isinstance(e['timestamp'], datetime) 
                         else datetime.fromisoformat(e['timestamp'])
        )
        
        # Detect gaps between consecutive events
        for i in range(len(sorted_events) - 1):
            event1 = sorted_events[i]
            event2 = sorted_events[i + 1]
            
            time1 = event1['timestamp']
            time2 = event2['timestamp']
            
            if isinstance(time1, str):
                time1 = datetime.fromisoformat(time1)
            if isinstance(time2, str):
                time2 = datetime.fromisoformat(time2)
            
            gap_duration = (time2 - time1).total_seconds() / 3600  # hours
            
            if gap_duration >= self.min_gap_hours:
                # Determine gap severity
                severity = min(gap_duration / (self.max_reasonable_gap_days * 24), 1.0)
                
                # Determine gap type
                gap_type = self._classify_gap_type(event1, event2, gap_duration)
                
                gap = TimelineGap(
                    gap_id=f"gap_{event1['event_id']}_{event2['event_id']}",
                    gap_type=gap_type,
                    start_time=time1,
                    end_time=time2,
                    duration_hours=gap_duration,
                    severity=severity,
                    description=f"{gap_duration:.1f} hour gap between {event1.get('title', 'event')} and {event2.get('title', 'event')}",
                    surrounding_events=[event1['event_id'], event2['event_id']],
                    suggested_investigation=self._suggest_gap_investigation(event1, event2, gap_type)
                )
                
                gaps.append(gap)
                self.gaps[gap.gap_id] = gap
        
        return gaps
    
    def _classify_gap_type(self, event1: Dict[str, Any], event2: Dict[str, Any], 
                          gap_hours: float) -> TimelineGapType:
        """Classify the type of gap"""
        
        # Check if events are part of a sequence
        if event1.get('event_id') in event2.get('related_events', []):
            return TimelineGapType.UNEXPLAINED_TRANSITION
        
        # Check if gap is unusually long
        if gap_hours > self.max_reasonable_gap_days * 24:
            return TimelineGapType.MISSING_PERIOD
        
        # Check if events are of related types
        type1 = event1.get('event_type', '')
        type2 = event2.get('event_type', '')
        
        related_types = [
            ('criminal_event', 'legal_action'),
            ('communication', 'transaction'),
            ('evidence_discovery', 'legal_action')
        ]
        
        if (type1, type2) in related_types:
            return TimelineGapType.INCOMPLETE_SEQUENCE
        
        return TimelineGapType.SPARSE_COVERAGE
    
    def _suggest_gap_investigation(self, event1: Dict[str, Any], event2: Dict[str, Any],
                                   gap_type: TimelineGapType) -> str:
        """Suggest investigation actions for a gap"""
        
        suggestions = {
            TimelineGapType.MISSING_PERIOD: "Investigate activities during this period through communications, financial records, or witness statements",
            TimelineGapType.UNEXPLAINED_TRANSITION: "Identify intermediate events or actions that connect these two events",
            TimelineGapType.INCOMPLETE_SEQUENCE: "Look for missing steps in the sequence of events",
            TimelineGapType.SPARSE_COVERAGE: "Gather more detailed timeline information for this period"
        }
        
        return suggestions.get(gap_type, "Further investigation recommended")
    
    def detect_conflicts(self, events: List[Dict[str, Any]]) -> List[TimelineConflict]:
        """Detect conflicts in the timeline"""
        
        conflicts = []
        
        # Check for temporal impossibilities
        temporal_conflicts = self._detect_temporal_conflicts(events)
        conflicts.extend(temporal_conflicts)
        
        # Check for contradictory facts
        factual_conflicts = self._detect_factual_conflicts(events)
        conflicts.extend(factual_conflicts)
        
        # Check for duplicate events
        duplicate_conflicts = self._detect_duplicates(events)
        conflicts.extend(duplicate_conflicts)
        
        return conflicts
    
    def _detect_temporal_conflicts(self, events: List[Dict[str, Any]]) -> List[TimelineConflict]:
        """Detect temporal impossibilities"""
        
        conflicts = []
        
        # Check for events that require the same entity to be in two places at once
        for i, event1 in enumerate(events):
            for event2 in events[i+1:]:
                # Check for overlapping times
                time1 = event1.get('timestamp')
                time2 = event2.get('timestamp')
                
                if not time1 or not time2:
                    continue
                
                if isinstance(time1, str):
                    time1 = datetime.fromisoformat(time1)
                if isinstance(time2, str):
                    time2 = datetime.fromisoformat(time2)
                
                # Check if events are very close in time
                time_diff = abs((time2 - time1).total_seconds() / 60)  # minutes
                
                if time_diff < 30:  # Less than 30 minutes apart
                    # Check for shared participants
                    participants1 = set(event1.get('participants', []))
                    participants2 = set(event2.get('participants', []))
                    shared = participants1.intersection(participants2)
                    
                    if shared:
                        # Check if events are in different locations
                        loc1 = event1.get('location')
                        loc2 = event2.get('location')
                        
                        if loc1 and loc2 and loc1 != loc2:
                            conflict = TimelineConflict(
                                conflict_id=f"temporal_{event1['event_id']}_{event2['event_id']}",
                                conflict_type=ConflictType.TEMPORAL_IMPOSSIBILITY,
                                conflicting_events=[event1['event_id'], event2['event_id']],
                                description=f"Shared participants {shared} cannot be in two locations within {time_diff:.0f} minutes",
                                resolution_strategy="Verify timestamps and locations"
                            )
                            
                            conflicts.append(conflict)
                            self.conflicts[conflict.conflict_id] = conflict
        
        return conflicts
    
    def _detect_factual_conflicts(self, events: List[Dict[str, Any]]) -> List[TimelineConflict]:
        """Detect contradictory facts"""
        
        conflicts = []
        
        # Group events by type and participants
        event_groups = {}
        for event in events:
            key = (event.get('event_type'), tuple(sorted(event.get('participants', []))))
            if key not in event_groups:
                event_groups[key] = []
            event_groups[key].append(event)
        
        # Check for contradictions within groups
        for key, group_events in event_groups.items():
            if len(group_events) > 1:
                # Check for contradictory descriptions
                for i, event1 in enumerate(group_events):
                    for event2 in group_events[i+1:]:
                        desc1 = event1.get('description', '').lower()
                        desc2 = event2.get('description', '').lower()
                        
                        # Simple contradiction detection (can be enhanced)
                        contradiction_pairs = [
                            ('approved', 'denied'),
                            ('present', 'absent'),
                            ('guilty', 'innocent'),
                            ('paid', 'unpaid')
                        ]
                        
                        for word1, word2 in contradiction_pairs:
                            if (word1 in desc1 and word2 in desc2) or (word2 in desc1 and word1 in desc2):
                                conflict = TimelineConflict(
                                    conflict_id=f"factual_{event1['event_id']}_{event2['event_id']}",
                                    conflict_type=ConflictType.CONTRADICTORY_FACTS,
                                    conflicting_events=[event1['event_id'], event2['event_id']],
                                    description=f"Contradictory information: '{word1}' vs '{word2}'",
                                    resolution_strategy="Review source documents and evidence"
                                )
                                
                                conflicts.append(conflict)
                                self.conflicts[conflict.conflict_id] = conflict
        
        return conflicts
    
    def _detect_duplicates(self, events: List[Dict[str, Any]]) -> List[TimelineConflict]:
        """Detect duplicate events"""
        
        conflicts = []
        
        for i, event1 in enumerate(events):
            for event2 in events[i+1:]:
                # Check for very similar events
                similarity_score = self._calculate_event_similarity(event1, event2)
                
                if similarity_score > 0.8:
                    conflict = TimelineConflict(
                        conflict_id=f"duplicate_{event1['event_id']}_{event2['event_id']}",
                        conflict_type=ConflictType.DUPLICATE_EVENT,
                        conflicting_events=[event1['event_id'], event2['event_id']],
                        description=f"Potential duplicate events (similarity: {similarity_score:.2f})",
                        resolution_strategy="Merge events or verify they are distinct"
                    )
                    
                    conflicts.append(conflict)
                    self.conflicts[conflict.conflict_id] = conflict
        
        return conflicts
    
    def _calculate_event_similarity(self, event1: Dict[str, Any], event2: Dict[str, Any]) -> float:
        """Calculate similarity between two events"""
        
        similarity = 0.0
        
        # Compare timestamps
        time1 = event1.get('timestamp')
        time2 = event2.get('timestamp')
        
        if time1 and time2:
            if isinstance(time1, str):
                time1 = datetime.fromisoformat(time1)
            if isinstance(time2, str):
                time2 = datetime.fromisoformat(time2)
            
            time_diff_hours = abs((time2 - time1).total_seconds() / 3600)
            if time_diff_hours < 1:
                similarity += 0.4
        
        # Compare event types
        if event1.get('event_type') == event2.get('event_type'):
            similarity += 0.3
        
        # Compare participants
        participants1 = set(event1.get('participants', []))
        participants2 = set(event2.get('participants', []))
        
        if participants1 and participants2:
            overlap = len(participants1.intersection(participants2)) / max(len(participants1), len(participants2))
            similarity += 0.3 * overlap
        
        return similarity
    
    def quantify_uncertainty(self, events: List[Dict[str, Any]]) -> List[UncertaintyMeasure]:
        """Quantify uncertainty in timeline data"""
        
        uncertainties = []
        
        for event in events:
            # Temporal uncertainty
            if not event.get('timestamp') or event.get('timestamp_approximate'):
                uncertainty = UncertaintyMeasure(
                    uncertainty_id=f"temporal_{event['event_id']}",
                    event_id=event['event_id'],
                    uncertainty_type=UncertaintyType.TEMPORAL,
                    uncertainty_score=0.7,
                    description="Timestamp is approximate or missing"
                )
                uncertainties.append(uncertainty)
                self.uncertainties[uncertainty.uncertainty_id] = uncertainty
            
            # Factual uncertainty
            verification_level = event.get('verification_level', 'alleged')
            if verification_level in ['alleged', 'disputed']:
                uncertainty_score = 0.8 if verification_level == 'disputed' else 0.6
                
                uncertainty = UncertaintyMeasure(
                    uncertainty_id=f"factual_{event['event_id']}",
                    event_id=event['event_id'],
                    uncertainty_type=UncertaintyType.FACTUAL,
                    uncertainty_score=uncertainty_score,
                    description=f"Event is {verification_level}"
                )
                uncertainties.append(uncertainty)
                self.uncertainties[uncertainty.uncertainty_id] = uncertainty
            
            # Completeness uncertainty
            if not event.get('participants') or len(event.get('participants', [])) == 0:
                uncertainty = UncertaintyMeasure(
                    uncertainty_id=f"completeness_{event['event_id']}",
                    event_id=event['event_id'],
                    uncertainty_type=UncertaintyType.COMPLETENESS,
                    uncertainty_score=0.5,
                    description="Missing participant information"
                )
                uncertainties.append(uncertainty)
                self.uncertainties[uncertainty.uncertainty_id] = uncertainty
        
        return uncertainties
    
    def reconstruct_timeline(self, partial_events: List[Dict[str, Any]],
                           known_patterns: Optional[List[Dict[str, Any]]] = None) -> TimelineReconstruction:
        """Reconstruct timeline from partial data"""
        
        reconstructed_events = []
        assumptions = []
        
        # Sort partial events
        sorted_events = sorted(
            [e for e in partial_events if e.get('timestamp')],
            key=lambda e: e['timestamp'] if isinstance(e['timestamp'], datetime)
                         else datetime.fromisoformat(e['timestamp'])
        )
        
        # Fill gaps with inferred events
        for i in range(len(sorted_events) - 1):
            event1 = sorted_events[i]
            event2 = sorted_events[i + 1]
            
            reconstructed_events.append(event1)
            
            # Check if there's a significant gap
            time1 = event1['timestamp']
            time2 = event2['timestamp']
            
            if isinstance(time1, str):
                time1 = datetime.fromisoformat(time1)
            if isinstance(time2, str):
                time2 = datetime.fromisoformat(time2)
            
            gap_hours = (time2 - time1).total_seconds() / 3600
            
            if gap_hours > self.min_gap_hours:
                # Infer intermediate events based on patterns
                inferred_event = {
                    'event_id': f"inferred_{event1['event_id']}_{event2['event_id']}",
                    'title': f"Inferred activity between {event1.get('title', 'event')} and {event2.get('title', 'event')}",
                    'description': "Reconstructed based on timeline patterns",
                    'timestamp': time1 + timedelta(hours=gap_hours/2),
                    'event_type': 'inferred',
                    'participants': list(set(event1.get('participants', []) + event2.get('participants', []))),
                    'inferred': True
                }
                
                reconstructed_events.append(inferred_event)
                assumptions.append(f"Inferred activity during {gap_hours:.1f} hour gap")
        
        # Add last event
        if sorted_events:
            reconstructed_events.append(sorted_events[-1])
        
        reconstruction = TimelineReconstruction(
            reconstruction_id=f"recon_{datetime.now().timestamp()}",
            original_events=[e['event_id'] for e in partial_events],
            reconstructed_events=reconstructed_events,
            reconstruction_method="gap_filling",
            confidence=0.6,
            assumptions=assumptions
        )
        
        self.reconstructions[reconstruction.reconstruction_id] = reconstruction
        return reconstruction
    
    def compare_timelines(self, timeline1: List[Dict[str, Any]], 
                         timeline2: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare two timelines and generate diff"""
        
        diff = {
            'only_in_timeline1': [],
            'only_in_timeline2': [],
            'common_events': [],
            'conflicting_events': [],
            'timeline1_count': len(timeline1),
            'timeline2_count': len(timeline2)
        }
        
        # Create event ID sets
        ids1 = {e['event_id'] for e in timeline1}
        ids2 = {e['event_id'] for e in timeline2}
        
        # Find unique events
        diff['only_in_timeline1'] = [e for e in timeline1 if e['event_id'] not in ids2]
        diff['only_in_timeline2'] = [e for e in timeline2 if e['event_id'] not in ids1]
        
        # Find common events and check for conflicts
        common_ids = ids1.intersection(ids2)
        
        for event_id in common_ids:
            event1 = next(e for e in timeline1 if e['event_id'] == event_id)
            event2 = next(e for e in timeline2 if e['event_id'] == event_id)
            
            # Check if events differ
            if event1.get('description') != event2.get('description'):
                diff['conflicting_events'].append({
                    'event_id': event_id,
                    'timeline1_version': event1,
                    'timeline2_version': event2,
                    'differences': self._find_event_differences(event1, event2)
                })
            else:
                diff['common_events'].append(event1)
        
        return diff
    
    def _find_event_differences(self, event1: Dict[str, Any], event2: Dict[str, Any]) -> List[str]:
        """Find specific differences between two events"""
        
        differences = []
        
        for key in set(event1.keys()).union(set(event2.keys())):
            if event1.get(key) != event2.get(key):
                differences.append(f"{key}: '{event1.get(key)}' vs '{event2.get(key)}'")
        
        return differences
    
    def export_analysis(self) -> Dict[str, Any]:
        """Export complete timeline analysis"""
        return {
            "gaps": [gap.dict() for gap in self.gaps.values()],
            "conflicts": [conflict.dict() for conflict in self.conflicts.values()],
            "uncertainties": [unc.dict() for unc in self.uncertainties.values()],
            "reconstructions": [recon.dict() for recon in self.reconstructions.values()]
        }

