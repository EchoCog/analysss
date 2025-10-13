"""
Enhanced System Dynamics with Agent-Based Modeling
=================================================

Improvements implemented:
1. Agent-based modeling framework for entities
2. Multi-agent simulation engine
3. Behavioral rule systems
4. Strategic goal modeling
5. Agent interaction protocols
6. Emergent behavior detection
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

import numpy as np
from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Types of agents in the system"""
    INDIVIDUAL = "individual"
    ORGANIZATION = "organization"
    INSTITUTION = "institution"
    SYSTEM = "system"


class BehaviorType(str, Enum):
    """Types of agent behaviors"""
    COOPERATIVE = "cooperative"
    COMPETITIVE = "competitive"
    DEFENSIVE = "defensive"
    AGGRESSIVE = "aggressive"
    NEUTRAL = "neutral"
    OPPORTUNISTIC = "opportunistic"


class InteractionType(str, Enum):
    """Types of agent interactions"""
    COMMUNICATION = "communication"
    TRANSACTION = "transaction"
    NEGOTIATION = "negotiation"
    CONFLICT = "conflict"
    COLLABORATION = "collaboration"
    INFLUENCE = "influence"


class AgentGoal(BaseModel):
    """Represents a strategic goal for an agent"""
    
    goal_id: str = Field(default_factory=lambda: str(uuid4()))
    description: str
    priority: float = Field(ge=0.0, le=1.0)
    target_state: Dict[str, Any] = Field(default_factory=dict)
    deadline: Optional[datetime] = None
    progress: float = Field(default=0.0, ge=0.0, le=1.0)
    achieved: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BehaviorRule(BaseModel):
    """Represents a behavioral rule for an agent"""
    
    rule_id: str = Field(default_factory=lambda: str(uuid4()))
    condition: str
    action: str
    priority: float = Field(ge=0.0, le=1.0)
    active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentState(BaseModel):
    """Represents the current state of an agent"""
    
    timestamp: datetime = Field(default_factory=datetime.now)
    resources: Dict[str, float] = Field(default_factory=dict)
    relationships: Dict[str, float] = Field(default_factory=dict)
    knowledge: Set[str] = Field(default_factory=set)
    beliefs: Dict[str, float] = Field(default_factory=dict)
    emotions: Dict[str, float] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            set: lambda v: list(v)
        }


class AgentInteraction(BaseModel):
    """Represents an interaction between agents"""
    
    interaction_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    source_agent_id: str
    target_agent_id: str
    interaction_type: InteractionType
    content: Dict[str, Any] = Field(default_factory=dict)
    outcome: Optional[str] = None
    impact_on_source: Dict[str, float] = Field(default_factory=dict)
    impact_on_target: Dict[str, float] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class EmergentPattern(BaseModel):
    """Represents an emergent pattern from agent interactions"""
    
    pattern_id: str = Field(default_factory=lambda: str(uuid4()))
    pattern_type: str
    agents_involved: List[str]
    description: str
    emergence_time: datetime = Field(default_factory=datetime.now)
    strength: float = Field(ge=0.0, le=1.0)
    stability: float = Field(ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Agent(BaseModel):
    """Represents an intelligent agent in the system"""
    
    agent_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    agent_type: AgentType
    behavior_type: BehaviorType = BehaviorType.NEUTRAL
    
    # Strategic components
    goals: List[AgentGoal] = Field(default_factory=list)
    behavior_rules: List[BehaviorRule] = Field(default_factory=list)
    
    # State
    current_state: AgentState = Field(default_factory=AgentState)
    state_history: List[AgentState] = Field(default_factory=list)
    
    # Capabilities
    capabilities: Set[str] = Field(default_factory=set)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    
    # Learning
    learning_rate: float = Field(default=0.1, ge=0.0, le=1.0)
    experience: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            set: lambda v: list(v)
        }
    
    def add_goal(self, description: str, priority: float, 
                target_state: Optional[Dict[str, Any]] = None) -> AgentGoal:
        """Add a strategic goal"""
        goal = AgentGoal(
            description=description,
            priority=priority,
            target_state=target_state or {}
        )
        self.goals.append(goal)
        return goal
    
    def add_behavior_rule(self, condition: str, action: str, priority: float = 0.5) -> BehaviorRule:
        """Add a behavioral rule"""
        rule = BehaviorRule(
            condition=condition,
            action=action,
            priority=priority
        )
        self.behavior_rules.append(rule)
        return rule
    
    def update_state(self, **kwargs):
        """Update agent state"""
        # Save current state to history
        self.state_history.append(self.current_state.copy())
        
        # Update state
        new_state = self.current_state.copy()
        for key, value in kwargs.items():
            if hasattr(new_state, key):
                setattr(new_state, key, value)
        
        new_state.timestamp = datetime.now()
        self.current_state = new_state
    
    def evaluate_goals(self) -> List[Tuple[AgentGoal, float]]:
        """Evaluate progress toward goals"""
        evaluations = []
        
        for goal in self.goals:
            if goal.achieved:
                evaluations.append((goal, 1.0))
                continue
            
            # Calculate progress based on current state vs target state
            progress = 0.0
            if goal.target_state:
                matches = 0
                total = len(goal.target_state)
                
                for key, target_value in goal.target_state.items():
                    current_value = self.current_state.resources.get(key, 0)
                    if isinstance(target_value, (int, float)):
                        if current_value >= target_value:
                            matches += 1
                
                progress = matches / total if total > 0 else 0.0
            
            goal.progress = progress
            if progress >= 1.0:
                goal.achieved = True
            
            evaluations.append((goal, progress))
        
        return evaluations
    
    def select_action(self, context: Dict[str, Any]) -> Optional[str]:
        """Select action based on behavior rules and goals"""
        
        # Evaluate active rules
        applicable_rules = []
        for rule in self.behavior_rules:
            if rule.active and self._evaluate_condition(rule.condition, context):
                applicable_rules.append(rule)
        
        # Select highest priority rule
        if applicable_rules:
            selected_rule = max(applicable_rules, key=lambda r: r.priority)
            return selected_rule.action
        
        return None
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate if a condition is met (simplified)"""
        # In practice, would use a proper rule engine
        # For now, simple keyword matching
        
        if "resource" in condition:
            return len(self.current_state.resources) > 0
        if "goal" in condition:
            return len(self.goals) > 0
        if "threat" in condition:
            return context.get('threat_level', 0) > 0.5
        
        return False
    
    def learn_from_experience(self, experience: Dict[str, Any]):
        """Learn from an experience"""
        self.experience.append(experience)
        
        # Simple learning: adjust behavior based on outcome
        outcome = experience.get('outcome', 'neutral')
        
        if outcome == 'positive':
            # Reinforce successful behaviors
            action = experience.get('action')
            for rule in self.behavior_rules:
                if rule.action == action:
                    rule.priority = min(1.0, rule.priority + self.learning_rate * 0.1)
        
        elif outcome == 'negative':
            # Reduce priority of unsuccessful behaviors
            action = experience.get('action')
            for rule in self.behavior_rules:
                if rule.action == action:
                    rule.priority = max(0.0, rule.priority - self.learning_rate * 0.1)


class MultiAgentSimulation:
    """Simulation engine for multi-agent systems"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.interactions: List[AgentInteraction] = []
        self.emergent_patterns: Dict[str, EmergentPattern] = {}
        self.simulation_time: datetime = datetime.now()
        self.time_step: timedelta = timedelta(hours=1)
    
    def add_agent(self, agent: Agent):
        """Add an agent to the simulation"""
        self.agents[agent.agent_id] = agent
    
    def create_agent(self, name: str, agent_type: AgentType, 
                    behavior_type: BehaviorType = BehaviorType.NEUTRAL) -> Agent:
        """Create and add a new agent"""
        agent = Agent(
            name=name,
            agent_type=agent_type,
            behavior_type=behavior_type
        )
        self.add_agent(agent)
        return agent
    
    def simulate_interaction(self, source_id: str, target_id: str,
                           interaction_type: InteractionType,
                           content: Optional[Dict[str, Any]] = None) -> AgentInteraction:
        """Simulate an interaction between two agents"""
        
        source_agent = self.agents.get(source_id)
        target_agent = self.agents.get(target_id)
        
        if not source_agent or not target_agent:
            raise ValueError("Invalid agent IDs")
        
        # Determine interaction outcome based on agent behaviors
        outcome = self._determine_interaction_outcome(
            source_agent, target_agent, interaction_type
        )
        
        # Calculate impacts
        impact_on_source, impact_on_target = self._calculate_interaction_impacts(
            source_agent, target_agent, interaction_type, outcome
        )
        
        interaction = AgentInteraction(
            timestamp=self.simulation_time,
            source_agent_id=source_id,
            target_agent_id=target_id,
            interaction_type=interaction_type,
            content=content or {},
            outcome=outcome,
            impact_on_source=impact_on_source,
            impact_on_target=impact_on_target
        )
        
        self.interactions.append(interaction)
        
        # Update agent states based on interaction
        self._apply_interaction_impacts(source_agent, target_agent, interaction)
        
        # Agents learn from interaction
        source_agent.learn_from_experience({
            'action': interaction_type.value,
            'outcome': 'positive' if impact_on_source.get('benefit', 0) > 0 else 'negative',
            'interaction_id': interaction.interaction_id
        })
        
        return interaction
    
    def _determine_interaction_outcome(self, source: Agent, target: Agent,
                                      interaction_type: InteractionType) -> str:
        """Determine the outcome of an interaction"""
        
        # Simplified outcome determination based on behavior types
        if interaction_type == InteractionType.COLLABORATION:
            if source.behavior_type == BehaviorType.COOPERATIVE and \
               target.behavior_type == BehaviorType.COOPERATIVE:
                return "mutual_success"
            else:
                return "partial_success"
        
        elif interaction_type == InteractionType.CONFLICT:
            if source.behavior_type == BehaviorType.AGGRESSIVE:
                return "source_dominant"
            elif target.behavior_type == BehaviorType.AGGRESSIVE:
                return "target_dominant"
            else:
                return "stalemate"
        
        elif interaction_type == InteractionType.NEGOTIATION:
            return "compromise"
        
        return "neutral"
    
    def _calculate_interaction_impacts(self, source: Agent, target: Agent,
                                      interaction_type: InteractionType,
                                      outcome: str) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Calculate impacts of interaction on both agents"""
        
        impact_on_source = {'benefit': 0.0, 'cost': 0.0}
        impact_on_target = {'benefit': 0.0, 'cost': 0.0}
        
        if outcome == "mutual_success":
            impact_on_source['benefit'] = 0.5
            impact_on_target['benefit'] = 0.5
        
        elif outcome == "source_dominant":
            impact_on_source['benefit'] = 0.7
            impact_on_target['cost'] = 0.7
        
        elif outcome == "target_dominant":
            impact_on_source['cost'] = 0.7
            impact_on_target['benefit'] = 0.7
        
        elif outcome == "compromise":
            impact_on_source['benefit'] = 0.3
            impact_on_target['benefit'] = 0.3
        
        return impact_on_source, impact_on_target
    
    def _apply_interaction_impacts(self, source: Agent, target: Agent,
                                  interaction: AgentInteraction):
        """Apply interaction impacts to agent states"""
        
        # Update source agent
        source_resources = source.current_state.resources.copy()
        source_resources['influence'] = source_resources.get('influence', 0) + \
                                       interaction.impact_on_source.get('benefit', 0) - \
                                       interaction.impact_on_source.get('cost', 0)
        source.update_state(resources=source_resources)
        
        # Update target agent
        target_resources = target.current_state.resources.copy()
        target_resources['influence'] = target_resources.get('influence', 0) + \
                                       interaction.impact_on_target.get('benefit', 0) - \
                                       interaction.impact_on_target.get('cost', 0)
        target.update_state(resources=target_resources)
        
        # Update relationships
        source_relationships = source.current_state.relationships.copy()
        target_relationships = target.current_state.relationships.copy()
        
        relationship_change = 0.1 if interaction.outcome in ['mutual_success', 'compromise'] else -0.1
        
        source_relationships[target.agent_id] = \
            source_relationships.get(target.agent_id, 0.5) + relationship_change
        target_relationships[source.agent_id] = \
            target_relationships.get(source.agent_id, 0.5) + relationship_change
        
        source.update_state(relationships=source_relationships)
        target.update_state(relationships=target_relationships)
    
    def step(self, num_steps: int = 1):
        """Advance simulation by specified number of time steps"""
        
        for _ in range(num_steps):
            # Each agent evaluates goals and selects actions
            for agent in self.agents.values():
                agent.evaluate_goals()
                
                # Simple action selection
                context = {
                    'simulation_time': self.simulation_time,
                    'other_agents': [a for a in self.agents.values() if a.agent_id != agent.agent_id]
                }
                
                action = agent.select_action(context)
                
                # Execute action if selected
                if action and 'interact' in action:
                    # Find a random target agent
                    other_agents = [a for a in self.agents.values() if a.agent_id != agent.agent_id]
                    if other_agents:
                        target = np.random.choice(other_agents)
                        self.simulate_interaction(
                            agent.agent_id,
                            target.agent_id,
                            InteractionType.COMMUNICATION
                        )
            
            # Detect emergent patterns
            self._detect_emergent_patterns()
            
            # Advance time
            self.simulation_time += self.time_step
    
    def _detect_emergent_patterns(self):
        """Detect emergent patterns from agent interactions"""
        
        # Pattern 1: Coalition formation
        coalitions = self._detect_coalitions()
        for coalition in coalitions:
            pattern = EmergentPattern(
                pattern_type="coalition",
                agents_involved=coalition,
                description=f"Coalition of {len(coalition)} agents",
                strength=0.7,
                stability=0.6
            )
            self.emergent_patterns[pattern.pattern_id] = pattern
        
        # Pattern 2: Hierarchies
        hierarchies = self._detect_hierarchies()
        for hierarchy in hierarchies:
            pattern = EmergentPattern(
                pattern_type="hierarchy",
                agents_involved=hierarchy['agents'],
                description=f"Hierarchical structure with {hierarchy['levels']} levels",
                strength=0.8,
                stability=0.7
            )
            self.emergent_patterns[pattern.pattern_id] = pattern
    
    def _detect_coalitions(self) -> List[List[str]]:
        """Detect coalition formations"""
        coalitions = []
        
        # Find groups of agents with strong mutual relationships
        visited = set()
        
        for agent_id, agent in self.agents.items():
            if agent_id in visited:
                continue
            
            coalition = [agent_id]
            visited.add(agent_id)
            
            # Find strongly connected agents
            for other_id, relationship_strength in agent.current_state.relationships.items():
                if relationship_strength > 0.7 and other_id not in visited:
                    coalition.append(other_id)
                    visited.add(other_id)
            
            if len(coalition) >= 3:
                coalitions.append(coalition)
        
        return coalitions
    
    def _detect_hierarchies(self) -> List[Dict[str, Any]]:
        """Detect hierarchical structures"""
        hierarchies = []
        
        # Calculate influence scores
        influence_scores = {}
        for agent_id, agent in self.agents.items():
            influence = agent.current_state.resources.get('influence', 0)
            influence_scores[agent_id] = influence
        
        # Group agents by influence levels
        sorted_agents = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)
        
        if len(sorted_agents) >= 3:
            # Simple 3-level hierarchy
            top_tier = [sorted_agents[0][0]]
            mid_tier = [a[0] for a in sorted_agents[1:3]]
            low_tier = [a[0] for a in sorted_agents[3:]]
            
            hierarchies.append({
                'agents': top_tier + mid_tier + low_tier,
                'levels': 3,
                'structure': {
                    'top': top_tier,
                    'middle': mid_tier,
                    'bottom': low_tier
                }
            })
        
        return hierarchies
    
    def export_simulation(self) -> Dict[str, Any]:
        """Export complete simulation state"""
        return {
            "agents": [agent.dict() for agent in self.agents.values()],
            "interactions": [interaction.dict() for interaction in self.interactions],
            "emergent_patterns": [pattern.dict() for pattern in self.emergent_patterns.values()],
            "simulation_time": self.simulation_time.isoformat(),
            "total_steps": len(self.interactions)
        }

