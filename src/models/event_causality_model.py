"""
Event Causality and Sequence Analysis Model
==========================================

Improvements implemented:
1. Event causality modeling and inference
2. Event sequence pattern analysis
3. Impact propagation simulation
4. Event correlation detection
5. Anomaly detection for unusual events
6. Event prediction capabilities
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from pydantic import BaseModel, Field


class CausalityType(str, Enum):
    """Types of causal relationships between events"""
    DIRECT_CAUSE = "direct_cause"
    CONTRIBUTING_FACTOR = "contributing_factor"
    ENABLING_CONDITION = "enabling_condition"
    TRIGGER = "trigger"
    CONSEQUENCE = "consequence"
    CORRELATION = "correlation"


class ImpactLevel(str, Enum):
    """Impact levels for event propagation"""
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class EventSequenceType(str, Enum):
    """Types of event sequences"""
    LINEAR = "linear"
    BRANCHING = "branching"
    CYCLICAL = "cyclical"
    PARALLEL = "parallel"
    CONVERGENT = "convergent"


class CausalRelationship(BaseModel):
    """Represents a causal relationship between two events"""
    
    relationship_id: str
    cause_event_id: str
    effect_event_id: str
    causality_type: CausalityType
    confidence: float = Field(ge=0.0, le=1.0)
    time_lag: Optional[timedelta] = None
    evidence: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            timedelta: lambda v: v.total_seconds()
        }


class EventImpact(BaseModel):
    """Represents the impact of an event"""
    
    event_id: str
    impact_level: ImpactLevel
    affected_entities: List[str] = Field(default_factory=list)
    affected_events: List[str] = Field(default_factory=list)
    impact_description: str
    propagation_path: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EventSequence(BaseModel):
    """Represents a sequence of related events"""
    
    sequence_id: str
    sequence_type: EventSequenceType
    events: List[str] = Field(default_factory=list)
    start_time: datetime
    end_time: datetime
    pattern_strength: float = Field(ge=0.0, le=1.0)
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class EventAnomaly(BaseModel):
    """Represents a detected event anomaly"""
    
    anomaly_id: str
    event_id: str
    anomaly_type: str
    anomaly_score: float = Field(ge=0.0, le=1.0)
    expected_pattern: str
    actual_pattern: str
    detection_method: str
    detected_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EventPrediction(BaseModel):
    """Represents a predicted future event"""
    
    prediction_id: str
    predicted_event_type: str
    predicted_time: datetime
    confidence: float = Field(ge=0.0, le=1.0)
    based_on_events: List[str] = Field(default_factory=list)
    prediction_method: str
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class EventCausalityEngine:
    """Engine for analyzing event causality and sequences"""
    
    def __init__(self):
        self.causal_relationships: Dict[str, CausalRelationship] = {}
        self.event_impacts: Dict[str, EventImpact] = {}
        self.event_sequences: Dict[str, EventSequence] = {}
        self.anomalies: Dict[str, EventAnomaly] = {}
        self.predictions: Dict[str, EventPrediction] = {}
        
        # Analysis parameters
        self.max_time_lag_hours = 168  # 1 week
        self.min_correlation_threshold = 0.5
        self.anomaly_threshold = 0.7
    
    def infer_causality(self, events: List[Dict[str, Any]]) -> List[CausalRelationship]:
        """Infer causal relationships between events"""
        
        causal_rels = []
        
        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.get('timestamp', datetime.min))
        
        # Analyze pairs of events for causality
        for i, event1 in enumerate(sorted_events):
            for event2 in sorted_events[i+1:]:
                causality = self._analyze_causality_pair(event1, event2)
                if causality:
                    causal_rels.append(causality)
                    self.causal_relationships[causality.relationship_id] = causality
        
        return causal_rels
    
    def _analyze_causality_pair(self, event1: Dict[str, Any], 
                               event2: Dict[str, Any]) -> Optional[CausalRelationship]:
        """Analyze potential causality between two events"""
        
        # Extract timestamps
        time1 = event1.get('timestamp')
        time2 = event2.get('timestamp')
        
        if not time1 or not time2:
            return None
        
        # Convert to datetime if needed
        if isinstance(time1, str):
            time1 = datetime.fromisoformat(time1)
        if isinstance(time2, str):
            time2 = datetime.fromisoformat(time2)
        
        # Calculate time lag
        time_lag = time2 - time1
        
        # Check if within reasonable time window
        if time_lag.total_seconds() < 0 or time_lag.total_seconds() > self.max_time_lag_hours * 3600:
            return None
        
        # Analyze for causality indicators
        confidence = 0.0
        causality_type = CausalityType.CORRELATION
        evidence = []
        
        # Check for participant overlap
        participants1 = set(event1.get('participants', []))
        participants2 = set(event2.get('participants', []))
        overlap = participants1.intersection(participants2)
        
        if overlap:
            confidence += 0.3
            evidence.append(f"Shared participants: {', '.join(overlap)}")
        
        # Check for explicit references
        if event1.get('event_id') in event2.get('related_events', []):
            confidence += 0.4
            causality_type = CausalityType.DIRECT_CAUSE
            evidence.append("Explicit reference in event2")
        
        # Check for type-based causality patterns
        type1 = event1.get('event_type', '')
        type2 = event2.get('event_type', '')
        
        causal_patterns = {
            ('criminal_event', 'legal_action'): (CausalityType.TRIGGER, 0.3),
            ('communication', 'transaction'): (CausalityType.ENABLING_CONDITION, 0.2),
            ('evidence_discovery', 'legal_action'): (CausalityType.CONTRIBUTING_FACTOR, 0.3)
        }
        
        if (type1, type2) in causal_patterns:
            pattern_type, pattern_conf = causal_patterns[(type1, type2)]
            causality_type = pattern_type
            confidence += pattern_conf
            evidence.append(f"Pattern: {type1} -> {type2}")
        
        # Only create relationship if confidence is sufficient
        if confidence >= self.min_correlation_threshold:
            return CausalRelationship(
                relationship_id=f"causal_{event1['event_id']}_{event2['event_id']}",
                cause_event_id=event1['event_id'],
                effect_event_id=event2['event_id'],
                causality_type=causality_type,
                confidence=min(confidence, 1.0),
                time_lag=time_lag,
                evidence=evidence
            )
        
        return None
    
    def simulate_impact_propagation(self, source_event_id: str, 
                                   events: List[Dict[str, Any]],
                                   max_depth: int = 5) -> EventImpact:
        """Simulate how an event's impact propagates through the system"""
        
        affected_events = set()
        affected_entities = set()
        propagation_path = [source_event_id]
        
        # Find source event
        source_event = next((e for e in events if e['event_id'] == source_event_id), None)
        if not source_event:
            return None
        
        # Initial affected entities
        affected_entities.update(source_event.get('participants', []))
        
        # Propagate through causal relationships
        current_level = {source_event_id}
        for depth in range(max_depth):
            next_level = set()
            
            for event_id in current_level:
                # Find events caused by this event
                for rel in self.causal_relationships.values():
                    if rel.cause_event_id == event_id:
                        next_level.add(rel.effect_event_id)
                        affected_events.add(rel.effect_event_id)
                        propagation_path.append(rel.effect_event_id)
                        
                        # Add affected entities from this event
                        effect_event = next((e for e in events if e['event_id'] == rel.effect_event_id), None)
                        if effect_event:
                            affected_entities.update(effect_event.get('participants', []))
            
            if not next_level:
                break
            
            current_level = next_level
        
        # Determine impact level
        impact_level = self._calculate_impact_level(len(affected_events), len(affected_entities))
        
        impact = EventImpact(
            event_id=source_event_id,
            impact_level=impact_level,
            affected_entities=list(affected_entities),
            affected_events=list(affected_events),
            impact_description=f"Impact propagated to {len(affected_events)} events and {len(affected_entities)} entities",
            propagation_path=propagation_path
        )
        
        self.event_impacts[source_event_id] = impact
        return impact
    
    def _calculate_impact_level(self, num_events: int, num_entities: int) -> ImpactLevel:
        """Calculate impact level based on propagation"""
        total_impact = num_events + num_entities
        
        if total_impact >= 20:
            return ImpactLevel.CRITICAL
        elif total_impact >= 10:
            return ImpactLevel.HIGH
        elif total_impact >= 5:
            return ImpactLevel.MODERATE
        elif total_impact >= 2:
            return ImpactLevel.LOW
        else:
            return ImpactLevel.NEGLIGIBLE
    
    def detect_event_sequences(self, events: List[Dict[str, Any]]) -> List[EventSequence]:
        """Detect patterns in event sequences"""
        
        sequences = []
        
        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.get('timestamp', datetime.min))
        
        # Detect linear sequences
        linear_seqs = self._detect_linear_sequences(sorted_events)
        sequences.extend(linear_seqs)
        
        # Detect branching sequences
        branching_seqs = self._detect_branching_sequences(sorted_events)
        sequences.extend(branching_seqs)
        
        # Detect cyclical patterns
        cyclical_seqs = self._detect_cyclical_sequences(sorted_events)
        sequences.extend(cyclical_seqs)
        
        return sequences
    
    def _detect_linear_sequences(self, events: List[Dict[str, Any]]) -> List[EventSequence]:
        """Detect linear event sequences"""
        sequences = []
        
        # Group events by participants
        participant_events = {}
        for event in events:
            for participant in event.get('participants', []):
                if participant not in participant_events:
                    participant_events[participant] = []
                participant_events[participant].append(event)
        
        # Find linear sequences for each participant
        for participant, participant_evts in participant_events.items():
            if len(participant_evts) >= 3:
                sorted_evts = sorted(participant_evts, key=lambda e: e.get('timestamp', datetime.min))
                
                sequence = EventSequence(
                    sequence_id=f"linear_{participant}_{datetime.now().timestamp()}",
                    sequence_type=EventSequenceType.LINEAR,
                    events=[e['event_id'] for e in sorted_evts],
                    start_time=sorted_evts[0].get('timestamp', datetime.now()),
                    end_time=sorted_evts[-1].get('timestamp', datetime.now()),
                    pattern_strength=0.7,
                    description=f"Linear sequence of {len(sorted_evts)} events involving {participant}"
                )
                
                sequences.append(sequence)
                self.event_sequences[sequence.sequence_id] = sequence
        
        return sequences
    
    def _detect_branching_sequences(self, events: List[Dict[str, Any]]) -> List[EventSequence]:
        """Detect branching event sequences"""
        sequences = []
        
        # Find events that lead to multiple subsequent events
        for event in events:
            subsequent = []
            event_time = event.get('timestamp')
            
            for other_event in events:
                if other_event['event_id'] == event['event_id']:
                    continue
                
                other_time = other_event.get('timestamp')
                if other_time and event_time and other_time > event_time:
                    # Check if there's a causal relationship
                    for rel in self.causal_relationships.values():
                        if rel.cause_event_id == event['event_id'] and rel.effect_event_id == other_event['event_id']:
                            subsequent.append(other_event['event_id'])
            
            if len(subsequent) >= 2:
                sequence = EventSequence(
                    sequence_id=f"branch_{event['event_id']}_{datetime.now().timestamp()}",
                    sequence_type=EventSequenceType.BRANCHING,
                    events=[event['event_id']] + subsequent,
                    start_time=event.get('timestamp', datetime.now()),
                    end_time=datetime.now(),
                    pattern_strength=0.6,
                    description=f"Branching sequence with {len(subsequent)} branches from {event['event_id']}"
                )
                
                sequences.append(sequence)
                self.event_sequences[sequence.sequence_id] = sequence
        
        return sequences
    
    def _detect_cyclical_sequences(self, events: List[Dict[str, Any]]) -> List[EventSequence]:
        """Detect cyclical event patterns"""
        sequences = []
        
        # Look for repeating event types with similar participants
        event_patterns = {}
        
        for event in events:
            pattern_key = (event.get('event_type'), tuple(sorted(event.get('participants', []))))
            if pattern_key not in event_patterns:
                event_patterns[pattern_key] = []
            event_patterns[pattern_key].append(event)
        
        # Find patterns that repeat
        for pattern_key, pattern_events in event_patterns.items():
            if len(pattern_events) >= 3:
                sequence = EventSequence(
                    sequence_id=f"cycle_{pattern_key[0]}_{datetime.now().timestamp()}",
                    sequence_type=EventSequenceType.CYCLICAL,
                    events=[e['event_id'] for e in pattern_events],
                    start_time=pattern_events[0].get('timestamp', datetime.now()),
                    end_time=pattern_events[-1].get('timestamp', datetime.now()),
                    pattern_strength=0.8,
                    description=f"Cyclical pattern of {pattern_key[0]} events"
                )
                
                sequences.append(sequence)
                self.event_sequences[sequence.sequence_id] = sequence
        
        return sequences
    
    def detect_anomalies(self, events: List[Dict[str, Any]]) -> List[EventAnomaly]:
        """Detect anomalous events"""
        anomalies = []
        
        # Calculate event statistics
        event_type_counts = {}
        participant_counts = {}
        
        for event in events:
            event_type = event.get('event_type', 'unknown')
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
            
            for participant in event.get('participants', []):
                participant_counts[participant] = participant_counts.get(participant, 0) + 1
        
        # Detect anomalies
        for event in events:
            anomaly_score = 0.0
            anomaly_reasons = []
            
            # Check for rare event types
            event_type = event.get('event_type', 'unknown')
            if event_type_counts.get(event_type, 0) == 1:
                anomaly_score += 0.3
                anomaly_reasons.append("Unique event type")
            
            # Check for unusual participant combinations
            participants = event.get('participants', [])
            if len(participants) > 5:
                anomaly_score += 0.2
                anomaly_reasons.append("Unusually high number of participants")
            
            # Check for temporal anomalies
            event_time = event.get('timestamp')
            if event_time:
                # Check if event occurs at unusual time (e.g., late night)
                if isinstance(event_time, str):
                    event_time = datetime.fromisoformat(event_time)
                
                if event_time.hour < 6 or event_time.hour > 22:
                    anomaly_score += 0.2
                    anomaly_reasons.append("Unusual time of day")
            
            # Check for missing expected relationships
            has_causal_rel = any(
                rel.cause_event_id == event['event_id'] or rel.effect_event_id == event['event_id']
                for rel in self.causal_relationships.values()
            )
            
            if not has_causal_rel and len(events) > 5:
                anomaly_score += 0.3
                anomaly_reasons.append("No causal relationships")
            
            # Create anomaly if score exceeds threshold
            if anomaly_score >= self.anomaly_threshold:
                anomaly = EventAnomaly(
                    anomaly_id=f"anomaly_{event['event_id']}",
                    event_id=event['event_id'],
                    anomaly_type="composite",
                    anomaly_score=min(anomaly_score, 1.0),
                    expected_pattern="Standard event pattern",
                    actual_pattern="; ".join(anomaly_reasons),
                    detection_method="statistical_analysis"
                )
                
                anomalies.append(anomaly)
                self.anomalies[anomaly.anomaly_id] = anomaly
        
        return anomalies
    
    def predict_future_events(self, events: List[Dict[str, Any]], 
                             prediction_window_days: int = 30) -> List[EventPrediction]:
        """Predict future events based on patterns"""
        predictions = []
        
        # Analyze event sequences to predict next events
        for sequence in self.event_sequences.values():
            if sequence.sequence_type == EventSequenceType.CYCLICAL:
                # Predict continuation of cycle
                last_event = next((e for e in events if e['event_id'] == sequence.events[-1]), None)
                if last_event:
                    last_time = last_event.get('timestamp')
                    if last_time:
                        if isinstance(last_time, str):
                            last_time = datetime.fromisoformat(last_time)
                        
                        # Calculate average time between events in cycle
                        time_diffs = []
                        for i in range(len(sequence.events) - 1):
                            e1 = next((e for e in events if e['event_id'] == sequence.events[i]), None)
                            e2 = next((e for e in events if e['event_id'] == sequence.events[i+1]), None)
                            if e1 and e2:
                                t1 = e1.get('timestamp')
                                t2 = e2.get('timestamp')
                                if t1 and t2:
                                    if isinstance(t1, str):
                                        t1 = datetime.fromisoformat(t1)
                                    if isinstance(t2, str):
                                        t2 = datetime.fromisoformat(t2)
                                    time_diffs.append((t2 - t1).total_seconds())
                        
                        if time_diffs:
                            avg_diff = sum(time_diffs) / len(time_diffs)
                            predicted_time = last_time + timedelta(seconds=avg_diff)
                            
                            if predicted_time <= datetime.now() + timedelta(days=prediction_window_days):
                                prediction = EventPrediction(
                                    prediction_id=f"pred_{sequence.sequence_id}",
                                    predicted_event_type=last_event.get('event_type', 'unknown'),
                                    predicted_time=predicted_time,
                                    confidence=sequence.pattern_strength,
                                    based_on_events=sequence.events,
                                    prediction_method="cyclical_pattern"
                                )
                                
                                predictions.append(prediction)
                                self.predictions[prediction.prediction_id] = prediction
        
        return predictions
    
    def export_analysis(self) -> Dict[str, Any]:
        """Export complete causality analysis"""
        return {
            "causal_relationships": [rel.dict() for rel in self.causal_relationships.values()],
            "event_impacts": [impact.dict() for impact in self.event_impacts.values()],
            "event_sequences": [seq.dict() for seq in self.event_sequences.values()],
            "anomalies": [anomaly.dict() for anomaly in self.anomalies.values()],
            "predictions": [pred.dict() for pred in self.predictions.values()]
        }

