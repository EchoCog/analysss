#!/usr/bin/env python3
"""
Refactored Case Data Loader for HyperGNN Framework
"""

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from dateutil.parser import parse as parse_date

# Import evidence management classes
try:
    from frameworks.evidence_management import (
        ClassificationLevel,
        EvidenceItem,
        EvidenceType,
        VerificationStatus,
    )
except ImportError:
    from src.api.evidence_management import (
        ClassificationLevel,
        EvidenceItem,
        EvidenceType,
        VerificationStatus,
    )


class InformationStatus(Enum):
    SAVED = "saved"
    VERIFIED = "verified"
    PARTIAL = "partial"
    CIRCUMSTANTIAL = "circumstantial"
    SPECULATIVE = "speculative"
    MISSING = "missing"


@dataclass
class CaseEntity:
    entity_id: str
    name: str
    entity_type: str
    roles: List[str]
    attributes: Dict[str, Any] = field(default_factory=dict)
    evidence_references: List[str] = field(default_factory=list)
    verification_status: InformationStatus = InformationStatus.PARTIAL
    
    # Agent-based modeling properties
    behavioral_properties: Dict[str, Any] = field(default_factory=dict)
    behavioral_rules: List[str] = field(default_factory=list)
    strategic_goals: List[str] = field(default_factory=list)
    current_state: Dict[str, Any] = field(default_factory=dict)
    state_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Enhanced properties for criminal and commercial legal analysis
    legal_role_indicators: Dict[str, float] = field(default_factory=dict)  # Criminal/commercial role strengths
    resource_flows: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)  # Financial/material flows
    timeline_significance: Dict[str, float] = field(default_factory=dict)  # Event significance scores
    
    def initialize_agent_model(self, 
                               legal_aggression: float = 0.5,
                               control_seeking: float = 0.5,
                               evidence_dismissal: float = 0.5,
                               vulnerability_to_pressure: float = 0.5,
                               ethical_compliance: float = 0.5) -> None:
        """
        Initialize agent-based modeling properties for this entity.
        
        Args:
            legal_aggression: Level of legal aggression (0.0 to 1.0)
            control_seeking: Level of control-seeking behavior (0.0 to 1.0)
            evidence_dismissal: Tendency to dismiss evidence (0.0 to 1.0)
            vulnerability_to_pressure: Vulnerability to legal pressure (0.0 to 1.0)
            ethical_compliance: Level of ethical compliance (0.0 to 1.0)
        """
        self.behavioral_properties = {
            'legal_aggression': legal_aggression,
            'control_seeking': control_seeking,
            'evidence_dismissal': evidence_dismissal,
            'vulnerability_to_pressure': vulnerability_to_pressure,
            'ethical_compliance': ethical_compliance,
        }
        
        self.current_state = {
            'active': True,
            'timestamp': datetime.now(),
            'events_participated': [],
            'decisions_made': [],
            'relationships': {},
        }
    
    def add_behavioral_rule(self, condition: str, action: str) -> None:
        """
        Add a behavioral rule for this agent.
        
        Args:
            condition: The condition that triggers the rule
            action: The action to take when the condition is met
        """
        rule = f"IF {condition} THEN {action}"
        if rule not in self.behavioral_rules:
            self.behavioral_rules.append(rule)
    
    def add_strategic_goal(self, goal: str) -> None:
        """
        Add a strategic goal for this agent.
        
        Args:
            goal: The strategic goal description
        """
        if goal not in self.strategic_goals:
            self.strategic_goals.append(goal)
    
    def update_state(self, event_id: str, changes: Dict[str, Any]) -> None:
        """
        Update the agent's state based on an event.
        
        Args:
            event_id: The ID of the event causing the state change
            changes: Dictionary of state changes to apply
        """
        # Save current state to history
        self.state_history.append({
            'timestamp': self.current_state.get('timestamp', datetime.now()),
            'state': self.current_state.copy(),
            'event_id': event_id,
        })
        
        # Update current state
        self.current_state.update(changes)
        self.current_state['timestamp'] = datetime.now()
        
        # Track event participation
        if 'events_participated' in self.current_state:
            if event_id not in self.current_state['events_participated']:
                self.current_state['events_participated'].append(event_id)
    
    def make_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a decision based on behavioral properties and current context.
        
        Args:
            context: Context information for decision making
            
        Returns:
            Dictionary containing the decision and reasoning
        """
        decision = {
            'timestamp': datetime.now(),
            'context': context,
            'decision': None,
            'reasoning': [],
        }
        
        # Apply behavioral rules
        for rule in self.behavioral_rules:
            # Simple rule matching (would be enhanced in production)
            if 'IF' in rule and 'THEN' in rule:
                parts = rule.split('THEN')
                condition = parts[0].replace('IF', '').strip()
                action = parts[1].strip()
                
                # Check if condition matches context
                if any(cond_key in str(context) for cond_key in condition.split()):
                    decision['reasoning'].append(f"Applied rule: {rule}")
                    decision['decision'] = action
                    break
        
        # Use behavioral properties if no rule matched
        if not decision['decision']:
            if self.behavioral_properties.get('legal_aggression', 0) > 0.7:
                decision['decision'] = 'escalate_legally'
                decision['reasoning'].append('High legal aggression level')
            elif self.behavioral_properties.get('control_seeking', 0) > 0.7:
                decision['decision'] = 'seek_control'
                decision['reasoning'].append('High control-seeking behavior')
            else:
                decision['decision'] = 'monitor'
                decision['reasoning'].append('No specific action triggered')
        
        # Track decision in current state
        if 'decisions_made' in self.current_state:
            self.current_state['decisions_made'].append(decision)
        
        return decision
    
    def get_relationship_strength(self, other_entity_id: str) -> float:
        """
        Get the relationship strength with another entity.
        
        Args:
            other_entity_id: The ID of the other entity
            
        Returns:
            Relationship strength (0.0 to 1.0)
        """
        relationships = self.current_state.get('relationships', {})
        return relationships.get(other_entity_id, 0.0)
    
    def update_relationship(self, other_entity_id: str, strength_delta: float) -> None:
        """
        Update relationship strength with another entity.
        
        Args:
            other_entity_id: The ID of the other entity
            strength_delta: Change in relationship strength (-1.0 to 1.0)
        """
        if 'relationships' not in self.current_state:
            self.current_state['relationships'] = {}
        
        current_strength = self.current_state['relationships'].get(other_entity_id, 0.5)
        new_strength = max(0.0, min(1.0, current_strength + strength_delta))
        self.current_state['relationships'][other_entity_id] = new_strength
    
    def identify_criminal_roles(self, events: List['CaseEvent']) -> Dict[str, float]:
        """
        Identify criminal law roles based on events and behavioral patterns.
        
        Args:
            events: List of case events involving this entity
            
        Returns:
            Dictionary mapping criminal roles to confidence scores (0.0-1.0)
        """
        criminal_roles = {
            'victim': 0.0,
            'perpetrator': 0.0,
            'witness': 0.0,
            'complainant': 0.0,
            'defendant': 0.0,
            'suspect': 0.0
        }
        
        # Analyze role indicators from events
        for event in events:
            if self.entity_id in event.participants or self.name.lower() in event.description.lower():
                description_lower = event.description.lower()
                
                # Victim indicators
                if any(term in description_lower for term in ['murdered', 'killed', 'victim', 'harmed', 'attacked']):
                    criminal_roles['victim'] += 0.3
                
                # Perpetrator indicators  
                if any(term in description_lower for term in ['perpetrator', 'committed', 'accused of', 'charged with']):
                    criminal_roles['perpetrator'] += 0.4
                    
                # Complainant indicators
                if any(term in description_lower for term in ['reported', 'complaint', 'filed report']):
                    criminal_roles['complainant'] += 0.3
                    
                # Witness indicators
                if any(term in description_lower for term in ['witnessed', 'saw', 'testimony', 'statement']):
                    criminal_roles['witness'] += 0.2
        
        # Factor in behavioral properties
        if self.behavioral_properties:
            aggression = self.behavioral_properties.get('legal_aggression', 0.5)
            ethical_compliance = self.behavioral_properties.get('ethical_compliance', 0.5)
            
            # High aggression + low ethics may indicate perpetrator tendencies
            if aggression > 0.7 and ethical_compliance < 0.4:
                criminal_roles['perpetrator'] += 0.2
                
            # High ethics may indicate victim/witness reliability
            if ethical_compliance > 0.7:
                criminal_roles['witness'] += 0.1
                criminal_roles['victim'] += 0.1
        
        # Normalize scores
        for role in criminal_roles:
            criminal_roles[role] = min(1.0, criminal_roles[role])
            
        self.legal_role_indicators.update({f"criminal_{k}": v for k, v in criminal_roles.items()})
        return criminal_roles
    
    def identify_commercial_roles(self, events: List['CaseEvent']) -> Dict[str, float]:
        """
        Identify commercial law roles based on events and patterns.
        
        Args:
            events: List of case events involving this entity
            
        Returns:
            Dictionary mapping commercial roles to confidence scores (0.0-1.0)
        """
        commercial_roles = {
            'debtor': 0.0,
            'creditor': 0.0,
            'contractual_party': 0.0,
            'fiduciary': 0.0,
            'fraudster': 0.0,
            'beneficiary': 0.0,
            'trustee': 0.0
        }
        
        # Analyze events for commercial indicators
        for event in events:
            if self.entity_id in event.participants or self.name.lower() in event.description.lower():
                description_lower = event.description.lower()
                
                # Debtor indicators
                if any(term in description_lower for term in ['owes', 'debt', 'payment due', 'defaulted']):
                    commercial_roles['debtor'] += 0.3
                    
                # Creditor indicators
                if any(term in description_lower for term in ['owed to', 'creditor', 'lender']):
                    commercial_roles['creditor'] += 0.3
                    
                # Fraud indicators
                if any(term in description_lower for term in ['fraud', 'misrepresentation', 'embezzlement']):
                    commercial_roles['fraudster'] += 0.4
                    
                # Fiduciary indicators
                if any(term in description_lower for term in ['trustee', 'fiduciary', 'agent', 'representative']):
                    commercial_roles['fiduciary'] += 0.3
        
        # Factor in behavioral properties for commercial analysis
        if self.behavioral_properties:
            control_seeking = self.behavioral_properties.get('control_seeking', 0.5)
            evidence_dismissal = self.behavioral_properties.get('evidence_dismissal', 0.5)
            
            # High control + evidence dismissal may indicate fraudulent behavior
            if control_seeking > 0.7 and evidence_dismissal > 0.6:
                commercial_roles['fraudster'] += 0.2
        
        # Normalize scores
        for role in commercial_roles:
            commercial_roles[role] = min(1.0, commercial_roles[role])
            
        self.legal_role_indicators.update({f"commercial_{k}": v for k, v in commercial_roles.items()})
        return commercial_roles
    
    def extract_legal_highlights(self, events: List['CaseEvent']) -> Dict[str, List[str]]:
        """
        Extract key legal highlights categorized by criminal and commercial law.
        
        Args:
            events: List of case events involving this entity
            
        Returns:
            Dictionary with 'criminal' and 'commercial' legal highlights
        """
        highlights = {
            'criminal': [],
            'commercial': []
        }
        
        criminal_indicators = [
            'murder', 'killed', 'murdered', 'violence', 'assault', 'criminal',
            'police', 'investigation', 'forensic', 'crime scene', 'evidence tampering'
        ]
        
        commercial_indicators = [
            'contract', 'agreement', 'payment', 'debt', 'fraud', 'financial',
            'misrepresentation', 'breach', 'damages', 'settlement', 'fiduciary'
        ]
        
        for event in events:
            if self.entity_id in event.participants or self.name.lower() in event.description.lower():
                description_lower = event.description.lower()
                
                # Check for criminal highlights
                for indicator in criminal_indicators:
                    if indicator in description_lower:
                        highlight = f"Criminal: {event.date.strftime('%Y-%m-%d')} - {event.description[:100]}..."
                        if highlight not in highlights['criminal']:
                            highlights['criminal'].append(highlight)
                        break
                
                # Check for commercial highlights  
                for indicator in commercial_indicators:
                    if indicator in description_lower:
                        highlight = f"Commercial: {event.date.strftime('%Y-%m-%d')} - {event.description[:100]}..."
                        if highlight not in highlights['commercial']:
                            highlights['commercial'].append(highlight)
                        break
        
        return highlights
    
    def track_resource_flow(self, flow_type: str, source: str, target: str, 
                           amount: float, timestamp: datetime, description: str) -> None:
        """
        Track resource flows (financial, material, information) for this entity.
        
        Args:
            flow_type: Type of resource flow ('financial', 'material', 'information')
            source: Source entity ID
            target: Target entity ID  
            amount: Flow magnitude
            timestamp: When the flow occurred
            description: Description of the flow
        """
        if flow_type not in self.resource_flows:
            self.resource_flows[flow_type] = []
        
        flow_record = {
            'source': source,
            'target': target,
            'amount': amount,
            'timestamp': timestamp.isoformat(),
            'description': description,
            'involves_entity': (source == self.entity_id or target == self.entity_id)
        }
        
        self.resource_flows[flow_type].append(flow_record)
    
    def calculate_timeline_significance(self, events: List['CaseEvent']) -> Dict[str, float]:
        """
        Calculate the timeline significance of events for this entity.
        
        Args:
            events: List of case events
            
        Returns:
            Dictionary mapping event IDs to significance scores (0.0-1.0)
        """
        significance_scores = {}
        
        for event in events:
            score = 0.0
            
            # Direct participation increases significance
            if self.entity_id in event.participants:
                score += 0.4
            
            # Entity mentioned in description
            if self.name.lower() in event.description.lower():
                score += 0.2
            
            # High-impact event types
            description_lower = event.description.lower()
            if any(term in description_lower for term in ['murder', 'killed', 'fraud', 'court']):
                score += 0.3
            
            # Legal action events
            if any(term in description_lower for term in ['filed', 'lawsuit', 'legal action', 'court order']):
                score += 0.2
            
            # Evidence-related events
            if any(term in description_lower for term in ['evidence', 'document', 'investigation']):
                score += 0.1
            
            significance_scores[event.event_id] = min(1.0, score)
        
        self.timeline_significance = significance_scores
        return significance_scores
    
    def to_agent(self) -> 'Agent':
        """
        Convert this CaseEntity to an Agent object for HyperGNN framework.
        
        Returns:
            An Agent object representing this entity
            
        Note:
            Requires the frameworks.hypergnn_core_enhanced module to be imported
        """
        try:
            from frameworks.hypergnn_core_enhanced import Agent, AgentType
        except ImportError:
            from src.api.hypergnn_core import Agent, AgentType
        
        # Map entity_type to AgentType
        agent_type_mapping = {
            'person': AgentType.INDIVIDUAL,
            'organization': AgentType.ORGANIZATION,
            'group': AgentType.GROUP,
            'system': AgentType.SYSTEM,
        }
        
        agent_type = agent_type_mapping.get(self.entity_type.lower(), AgentType.INDIVIDUAL)
        
        # Create Agent instance
        agent = Agent(
            agent_id=self.entity_id,
            agent_type=agent_type,
            name=self.name,
            attributes={
                **self.attributes,
                'behavioral_properties': self.behavioral_properties,
                'behavioral_rules': self.behavioral_rules,
                'strategic_goals': self.strategic_goals,
                'roles': self.roles,
                'verification_status': self.verification_status.value,
                'legal_role_indicators': self.legal_role_indicators,
                'resource_flows': self.resource_flows,
                'timeline_significance': self.timeline_significance,
            }
        )
        
        return agent


@dataclass
class CaseEvent:
    event_id: str
    date: datetime
    description: str
    participants: List[str]
    evidence_references: List[str] = field(default_factory=list)
    verification_status: InformationStatus = InformationStatus.PARTIAL
    event_type: str = "general"
    
    # Enhanced properties for legal analysis
    criminal_significance: float = 0.0  # 0.0-1.0 significance for criminal law
    commercial_significance: float = 0.0  # 0.0-1.0 significance for commercial law  
    causal_relations: List[str] = field(default_factory=list)  # IDs of events this causes/enables
    temporal_dependencies: List[str] = field(default_factory=list)  # Events this depends on temporally
    legal_categories: List[str] = field(default_factory=list)  # Criminal/commercial legal categories
    
    def categorize_legal_significance(self) -> Dict[str, float]:
        """
        Categorize and score the legal significance of this event.
        
        Returns:
            Dictionary with criminal and commercial significance scores
        """
        criminal_keywords = [
            'murder', 'killed', 'murdered', 'violence', 'assault', 'criminal',
            'police', 'investigation', 'forensic', 'crime scene', 'evidence tampering',
            'victim', 'perpetrator', 'witness', 'testimony', 'criminal charge'
        ]
        
        commercial_keywords = [
            'contract', 'agreement', 'payment', 'debt', 'fraud', 'financial',
            'misrepresentation', 'breach', 'damages', 'settlement', 'fiduciary',
            'business', 'transaction', 'invoice', 'account', 'monetary', 'creditor'
        ]
        
        description_lower = self.description.lower()
        
        # Calculate criminal significance
        criminal_matches = sum(1 for keyword in criminal_keywords if keyword in description_lower)
        self.criminal_significance = min(1.0, criminal_matches * 0.2)
        
        # Calculate commercial significance  
        commercial_matches = sum(1 for keyword in commercial_keywords if keyword in description_lower)
        self.commercial_significance = min(1.0, commercial_matches * 0.2)
        
        # Determine legal categories
        self.legal_categories = []
        if self.criminal_significance > 0.3:
            self.legal_categories.append('criminal')
        if self.commercial_significance > 0.3:
            self.legal_categories.append('commercial')
        if not self.legal_categories:
            self.legal_categories.append('general')
        
        return {
            'criminal': self.criminal_significance,
            'commercial': self.commercial_significance
        }
    
    def identify_causal_relationships(self, other_events: List['CaseEvent']) -> List[str]:
        """
        Identify causal relationships with other events based on temporal and content analysis.
        
        Args:
            other_events: List of other events to analyze relationships with
            
        Returns:
            List of event IDs that this event may causally influence
        """
        causal_indicators = [
            'as a result', 'therefore', 'consequently', 'due to', 'because of',
            'led to', 'caused', 'resulting in', 'prompted', 'triggered'
        ]
        
        temporal_causal_patterns = [
            ('filed', ['court order', 'legal action', 'hearing']),
            ('reported', ['investigation', 'police', 'forensic']),
            ('evidence', ['charge', 'arrest', 'court']),
            ('murder', ['investigation', 'forensic', 'witness'])
        ]
        
        caused_events = []
        description_lower = self.description.lower()
        
        # Check events that occur after this one
        for other_event in other_events:
            if other_event.date > self.date and other_event.event_id != self.event_id:
                other_desc_lower = other_event.description.lower()
                
                # Direct causal language
                if any(indicator in other_desc_lower for indicator in causal_indicators):
                    # Check if this event is referenced in the other event
                    if any(word in other_desc_lower for word in description_lower.split()[:5]):
                        caused_events.append(other_event.event_id)
                
                # Pattern-based causal analysis
                for trigger, consequences in temporal_causal_patterns:
                    if trigger in description_lower:
                        if any(consequence in other_desc_lower for consequence in consequences):
                            caused_events.append(other_event.event_id)
        
        self.causal_relations = caused_events
        return caused_events
    
    def calculate_temporal_dependencies(self, other_events: List['CaseEvent']) -> List[str]:
        """
        Calculate temporal dependencies - events that must happen before this one.
        
        Args:
            other_events: List of other events to analyze dependencies with
            
        Returns:
            List of event IDs this event depends on temporally
        """
        dependencies = []
        
        dependency_patterns = [
            ('court order', ['filed', 'application', 'legal action']),
            ('investigation', ['reported', 'complaint', 'murder']),
            ('arrest', ['investigation', 'evidence', 'warrant']),
            ('hearing', ['filed', 'court order', 'legal action'])
        ]
        
        description_lower = self.description.lower()
        
        # Find events that occur before this one
        for other_event in other_events:
            if other_event.date < self.date and other_event.event_id != self.event_id:
                other_desc_lower = other_event.description.lower()
                
                # Pattern-based dependency analysis
                for event_type, prerequisites in dependency_patterns:
                    if event_type in description_lower:
                        if any(prereq in other_desc_lower for prereq in prerequisites):
                            dependencies.append(other_event.event_id)
        
        self.temporal_dependencies = dependencies
        return dependencies


@dataclass
class CaseRelationship:
    relationship_id: str
    source_entity: str
    target_entity: str
    relationship_type: str
    strength: float = 1.0
    evidence_references: List[str] = field(default_factory=list)
    verification_status: InformationStatus = InformationStatus.PARTIAL


class DocumentLoader:
    def __init__(self, base_directory: str):
        self.base_directory = Path(base_directory)

    def load_documents(self, document_paths: List[str]) -> Dict[str, str]:
        loaded_docs = {}
        for doc_path in document_paths:
            full_path = self.base_directory / doc_path
            if full_path.exists():
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        loaded_docs[str(full_path)] = f.read()
                except Exception as e:
                    print(f"Error loading {full_path}: {e}")
        return loaded_docs


class EntityExtractor:
    def __init__(self):
        self.entity_patterns = {
            "person": [
                r"([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+)",
                r"([A-Z][a-z]+ [A-Z][a-z]+)",
            ],
            "email": [r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"],
            "organization": [r"(RegimA Group|RegimA Worldwide|Sage Account)"],
        }

    def extract_entities(self, content: str, source_file: str) -> Dict[str, CaseEntity]:
        entities = {}
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    entity_id = match.group(1).lower().replace(" ", "_")
                    if entity_id not in entities:
                        entities[entity_id] = CaseEntity(
                            entity_id=entity_id,
                            name=match.group(1),
                            entity_type=entity_type,
                            roles=[],  # Role extraction would be a separate, more complex process
                            evidence_references=[source_file],
                            verification_status=InformationStatus.PARTIAL,  # Simplified for this refactoring
                        )
        return entities


class EventExtractor:
    def __init__(self):
        self.date_patterns = [
            r"(\d{4}-\d{2}-\d{2})",
            r"(\d{1,2}/\d{1,2}/\d{4})",
            r"([A-Z][a-z]+ \d{1,2}, \d{4})",
            r"(\d{1,2} [A-Z][a-z]+ \d{4})",
        ]

    def extract_events(self, content: str, source_file: str) -> List[CaseEvent]:
        events = []
        for line in content.split("\n"):
            for pattern in self.date_patterns:
                for match in re.finditer(pattern, line):
                    try:
                        event_date = parse_date(match.group(1))
                        events.append(
                            CaseEvent(
                                event_id=f"event_{len(events)}_{event_date.strftime('%Y%m%d')}",
                                date=event_date,
                                description=line.strip(),
                                participants=[],  # Participant extraction is complex
                                evidence_references=[source_file],
                                verification_status=InformationStatus.PARTIAL,
                            )
                        )
                    except ValueError:
                        continue
        return events


class AgentModelFactory:
    """Factory for creating agent models with predefined behavioral patterns"""
    
    @staticmethod
    def create_primary_agent(entity: CaseEntity, agent_profile: str) -> CaseEntity:
        """
        Create a primary agent with behavioral patterns from agent_based_model_updated.md.
        
        Args:
            entity: The CaseEntity to enhance with agent model
            agent_profile: Profile type ('peter_faucitt', 'jacqueline_faucitt', 'daniel_faucitt')
            
        Returns:
            The enhanced CaseEntity with agent model properties
        """
        if agent_profile == 'peter_faucitt':
            entity.initialize_agent_model(
                legal_aggression=0.9,
                control_seeking=0.95,
                evidence_dismissal=0.85,
                vulnerability_to_pressure=0.2,
                ethical_compliance=0.3
            )
            entity.add_behavioral_rule(
                "challenged",
                "escalate through legal mechanisms"
            )
            entity.add_behavioral_rule(
                "evidence contradicts claims",
                "ignore and escalate"
            )
            entity.add_behavioral_rule(
                "opposition presents evidence",
                "use legal system as weapon"
            )
            entity.add_strategic_goal("Maintain control over financial resources")
            entity.add_strategic_goal("Neutralize witnesses to serious crimes")
            entity.add_strategic_goal("Establish dominance through legal mechanisms")
            entity.add_strategic_goal("Create public record discrediting opponents")
            
        elif agent_profile == 'jacqueline_faucitt':
            entity.initialize_agent_model(
                legal_aggression=0.3,
                control_seeking=0.2,
                evidence_dismissal=0.2,
                vulnerability_to_pressure=0.8,
                ethical_compliance=0.7
            )
            entity.add_behavioral_rule(
                "attacked",
                "provide evidence"
            )
            entity.add_behavioral_rule(
                "coerced",
                "partial compliance with resistance"
            )
            entity.add_behavioral_rule(
                "threatened",
                "seek legal protection"
            )
            entity.add_strategic_goal("Protect personal interests")
            entity.add_strategic_goal("Expose financial misconduct")
            entity.add_strategic_goal("Resist coercive control")
            entity.add_strategic_goal("Maintain credibility as witness")
            
        elif agent_profile == 'daniel_faucitt':
            entity.initialize_agent_model(
                legal_aggression=0.4,
                control_seeking=0.2,
                evidence_dismissal=0.1,
                vulnerability_to_pressure=0.8,
                ethical_compliance=0.9
            )
            entity.add_behavioral_rule(
                "attacked",
                "provide comprehensive evidence"
            )
            entity.add_behavioral_rule(
                "coerced",
                "strategic compliance with documentation"
            )
            entity.add_behavioral_rule(
                "threatened",
                "seek legal protection and expose false narratives"
            )
            entity.add_strategic_goal("Protect personal interests")
            entity.add_strategic_goal("Expose financial misconduct and serious crimes")
            entity.add_strategic_goal("Resist coercive control")
            entity.add_strategic_goal("Maintain credibility as witness")
        
        return entity
    
    @staticmethod
    def create_secondary_agent(entity: CaseEntity, agent_profile: str) -> CaseEntity:
        """
        Create a secondary agent with behavioral patterns.
        
        Args:
            entity: The CaseEntity to enhance with agent model
            agent_profile: Profile type ('elliott_attorneys', 'ens_africa', 'medical_professionals')
            
        Returns:
            The enhanced CaseEntity with agent model properties
        """
        if agent_profile == 'elliott_attorneys':
            entity.initialize_agent_model(
                legal_aggression=0.8,
                control_seeking=0.7,
                evidence_dismissal=0.8,
                vulnerability_to_pressure=0.3,
                ethical_compliance=0.3
            )
            entity.add_behavioral_rule(
                "client requests",
                "draft agreements with hidden coercive mechanisms"
            )
            entity.add_behavioral_rule(
                "evidence contradicts client",
                "ignore contradictory evidence"
            )
            entity.add_strategic_goal("Serve client interests regardless of ethics")
            entity.add_strategic_goal("Create legal frameworks for client control")
            entity.add_strategic_goal("Maintain appearance of professional conduct")
            entity.add_strategic_goal("Generate ongoing legal fees")
            
        elif agent_profile == 'ens_africa':
            entity.initialize_agent_model(
                legal_aggression=0.5,
                control_seeking=0.4,
                evidence_dismissal=0.5,
                vulnerability_to_pressure=0.5,
                ethical_compliance=0.6
            )
            entity.add_behavioral_rule(
                "evidence received",
                "process evidence but with limited action"
            )
            entity.add_behavioral_rule(
                "client directs",
                "limited challenge to client directives"
            )
            entity.add_strategic_goal("Maintain client relationship")
            entity.add_strategic_goal("Limit professional liability")
            entity.add_strategic_goal("Follow formal procedures")
            entity.add_strategic_goal("Avoid direct involvement in ethical conflicts")
            
        elif agent_profile == 'medical_professionals':
            entity.initialize_agent_model(
                legal_aggression=0.2,
                control_seeking=0.6,
                evidence_dismissal=0.4,
                vulnerability_to_pressure=0.7,
                ethical_compliance=0.4
            )
            entity.add_behavioral_rule(
                "evaluation requested",
                "conduct evaluations with predetermined focus"
            )
            entity.add_behavioral_rule(
                "tests possible",
                "order additional tests when possible"
            )
            entity.add_strategic_goal("Generate professional fees")
            entity.add_strategic_goal("Maintain referral relationships")
            entity.add_strategic_goal("Avoid professional liability")
            entity.add_strategic_goal("Expand scope of professional services")
        
        return entity
    
    @staticmethod
    def create_institutional_agent(entity: CaseEntity, agent_profile: str) -> CaseEntity:
        """
        Create an institutional agent with behavioral patterns.
        
        Args:
            entity: The CaseEntity to enhance with agent model
            agent_profile: Profile type ('court_system', 'forensic_investigators')
            
        Returns:
            The enhanced CaseEntity with agent model properties
        """
        if agent_profile == 'court_system':
            entity.initialize_agent_model(
                legal_aggression=0.3,
                control_seeking=0.5,
                evidence_dismissal=0.3,
                vulnerability_to_pressure=0.5,
                ethical_compliance=0.8
            )
            entity.add_behavioral_rule(
                "application filed",
                "process applications according to procedure"
            )
            entity.add_behavioral_rule(
                "evidence presented",
                "evaluate evidence within procedural constraints"
            )
            entity.add_strategic_goal("Uphold legal procedures")
            entity.add_strategic_goal("Process cases efficiently")
            entity.add_strategic_goal("Maintain institutional authority")
            entity.add_strategic_goal("Avoid procedural errors")
            
        elif agent_profile == 'forensic_investigators':
            entity.initialize_agent_model(
                legal_aggression=0.2,
                control_seeking=0.3,
                evidence_dismissal=0.3,
                vulnerability_to_pressure=0.7,
                ethical_compliance=0.7
            )
            entity.add_behavioral_rule(
                "investigation assigned",
                "investigate within defined terms of reference"
            )
            entity.add_behavioral_rule(
                "findings documented",
                "document findings according to professional standards"
            )
            entity.add_strategic_goal("Complete investigation within parameters")
            entity.add_strategic_goal("Maintain professional reputation")
            entity.add_strategic_goal("Generate professional fees")
            entity.add_strategic_goal("Avoid professional liability")
        
        return entity


class CaseDataLoader:
    def __init__(self, case_id: str, base_directory: str):
        self.case_id = case_id
        self.doc_loader = DocumentLoader(base_directory)
        self.entity_extractor = EntityExtractor()
        self.event_extractor = EventExtractor()
        self.entities: Dict[str, CaseEntity] = {}
        self.events: List[CaseEvent] = []

    def load_and_process_case(self, priority_docs: List[str]):
        documents = self.doc_loader.load_documents(priority_docs)
        for doc_path, content in documents.items():
            self.entities.update(
                self.entity_extractor.extract_entities(content, doc_path)
            )
            self.events.extend(self.event_extractor.extract_events(content, doc_path))

        return {
            "total_documents_processed": len(documents),
            "entities_found": len(self.entities),
            "events_found": len(self.events),
        }

    def integrate_ocr_revelations(self):
        """Integrate OCR revelations into case data
        
        Updates entities and events based on OCR findings about 
        Pete@regima.com control by Rynette Farrar
        """
        # Update Peter Faucitt entity with OCR revelation impact
        peter_id = "peter_faucitt"
        if peter_id in self.entities:
            self.entities[peter_id].attributes.update({
                "email_access_status": "NO_DIRECT_ACCESS",
                "pete_regima_com_controller": "Rynette Farrar",
                "information_dependency": "Complete - all email filtered through Rynette",
                "ocr_verified_status": "victim_of_email_hijacking"
            })
            self.entities[peter_id].verification_status = InformationStatus.VERIFIED
        else:
            # Create Peter entity with OCR context
            self.entities[peter_id] = CaseEntity(
                entity_id=peter_id,
                name="Peter Faucitt",
                entity_type="person",
                roles=["nominal_email_owner", "information_dependent"],
                attributes={
                    "email_access_status": "NO_DIRECT_ACCESS", 
                    "pete_regima_com_controller": "Rynette Farrar",
                    "information_dependency": "Complete - all email filtered through Rynette",
                    "ocr_verified_status": "victim_of_email_hijacking"
                },
                evidence_references=["OCR Screenshot 2025-06-20 Sage Account system"],
                verification_status=InformationStatus.VERIFIED
            )

        # Update/Create Rynette Farrar entity with controller role
        rynette_id = "rynette_farrar"
        if rynette_id in self.entities:
            self.entities[rynette_id].attributes.update({
                "email_control_status": "UNAUTHORIZED_CONTROLLER",
                "controlled_addresses": ["Pete@regima.com"],
                "information_warfare_capability": True,
                "ocr_verified_role": "information_interceptor"
            })
            self.entities[rynette_id].roles.extend([
                "unauthorized_email_controller", 
                "information_interceptor"
            ])
        else:
            # Create Rynette entity with OCR revelations
            self.entities[rynette_id] = CaseEntity(
                entity_id=rynette_id,
                name="Rynette Farrar", 
                entity_type="person",
                roles=["unauthorized_email_controller", "information_interceptor"],
                attributes={
                    "email_control_status": "UNAUTHORIZED_CONTROLLER",
                    "controlled_addresses": ["Pete@regima.com"],
                    "information_warfare_capability": True,
                    "ocr_verified_role": "information_interceptor"
                },
                evidence_references=["OCR Screenshot 2025-06-20 Sage Account system"],
                verification_status=InformationStatus.VERIFIED
            )

        # Add Pete@regima.com as communication channel entity  
        channel_id = "pete_regima_com_channel"
        self.entities[channel_id] = CaseEntity(
            entity_id=channel_id,
            name="Pete@regima.com",
            entity_type="communication_channel",
            roles=["hijacked_email_address"],
            attributes={
                "nominal_owner": "Peter Faucitt",
                "actual_controller": "Rynette Farrar", 
                "channel_type": "email",
                "hijack_verified": True,
                "legal_status": "identity_theft_evidence"
            },
            evidence_references=["OCR Screenshot 2025-06-20 Sage Account system"],
            verification_status=InformationStatus.VERIFIED
        )

        # Add OCR revelation event
        ocr_event = CaseEvent(
            event_id="ocr_revelation_2025_06_20",
            date=datetime(2025, 6, 20),
            description="OCR Screenshot reveals Rynette Farrar controls Pete@regima.com, not Peter Faucitt",
            event_type="evidence_discovery",
            participants=["peter_faucitt", "rynette_farrar"],
            evidence_references=["OCR Screenshot 2025-06-20 Sage Account system"],
            verification_status=InformationStatus.VERIFIED,
            attributes={
                "revelation_type": "email_hijacking_evidence",
                "legal_implications": ["identity_theft", "perjury_evidence", "information_warfare"],
                "impact_scope": "all_email_based_evidence_invalid"
            }
        )
        self.events.append(ocr_event)

    def export_ocr_summary(self) -> Dict[str, Any]:
        """Export summary of OCR revelations and their impact
        
        Returns:
            Dictionary containing OCR impact summary
        """
        return {
            "critical_revelation": {
                "finding": "Pete@regima.com controlled by Rynette Farrar, not Peter Faucitt",
                "evidence": "OCR Screenshot 2025-06-20 Sage Account system",
                "legal_status": "verified_identity_theft"
            },
            "affected_entities": {
                "peter_faucitt": {
                    "status": "victim_of_email_hijacking",
                    "access_level": "NO_DIRECT_ACCESS", 
                    "information_dependency": "Complete dependency on Rynette Farrar"
                },
                "rynette_farrar": {
                    "status": "unauthorized_controller",
                    "capabilities": ["email_interception", "information_warfare"],
                    "controlled_channels": ["Pete@regima.com"]
                }
            },
            "legal_implications": [
                "All Peter's claims of direct email receipt are impossible (perjury evidence)",
                "Identity theft charges applicable for Pete@regima.com usage",
                "Information warfare through systematic email interception",
                "All email-based timeline events require re-verification"
            ],
            "verification_requirements": [
                "Review all timeline entries showing Peter receiving emails",
                "Verify what Peter actually knew vs email content", 
                "Flag all court affidavits claiming direct email receipt as impossible",
                "Investigate how Pete@regima.com was created and by whom"
            ]
        }


if __name__ == "__main__":
    # Example usage:
    case_id = "rzonedevops_analysis"
    # It's better to pass the base directory as an argument or from a config file
    base_directory = "."
    data_loader = CaseDataLoader(case_id, base_directory)

    priority_documents = [
        "docs/current-state-summary-2025.md",
        "docs/ocr-assumptions-update-report.md",
        "docs/party-knowledge-matrix-analysis.md",
        "docs/court-order-timeline-cross-reference-analysis.md",
        "criminal-case-timeline-outline-sa.md",
    ]

    results = data_loader.load_and_process_case(priority_documents)
    print(json.dumps(results, indent=4))
