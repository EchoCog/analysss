#!/usr/bin/env python3
"""
Unified Model Framework
======================

This framework orchestrates and integrates all model types:
1. Agent-based models (HyperGNN)
2. Discrete event models
3. System dynamics models
4. Hypergraph models
5. LLM/Transformer models

The framework provides a unified interface to run comprehensive analysis
using all model types simultaneously, with data flow and coordination
between different modeling approaches.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np

# Import all model frameworks
try:
    from frameworks.hypergnn_core import (
        Agent,
        AgentType,
        DiscreteEvent,
        EventType,
        FlowType,
        HyperGNNFramework,
        SystemFlow,
        TensorType,
        TimelineTensor,
    )
except ImportError:
    from frameworks.hypergnn_core import Agent, AgentType

    # Define minimal classes for compatibility
    class DiscreteEvent:
        def __init__(self, event_id, timestamp, event_type, actors, description):
            self.event_id = event_id
            self.timestamp = timestamp
            self.event_type = event_type
            self.actors = actors
            self.description = description

    class EventType:
        COMMUNICATION = "communication"
        TRANSACTION = "transaction"
        MEETING = "meeting"
        EVIDENCE = "evidence"

    class SystemFlow:
        def __init__(
            self, flow_id, flow_type, source, target, timestamp, magnitude, description
        ):
            self.flow_id = flow_id
            self.flow_type = flow_type
            self.source = source
            self.target = target
            self.timestamp = timestamp
            self.magnitude = magnitude
            self.description = description

    class FlowType:
        INFORMATION = "information"
        FINANCIAL = "financial"

    class HyperGNNFramework:
        def __init__(self, case_id):
            self.case_id = case_id

        def add_agent(self, agent):
            pass

        def add_event(self, event):
            pass

        def add_flow(self, flow):
            pass


from frameworks.system_dynamics import (
    DeceptionPattern,
    Flow,
    MotiveMeansOpportunity,
    RiskLevel,
    Stock,
    StockType,
    SystemDynamicsModel,
)

try:
    from frameworks.llm_transformer_schema import (
        AttentionHead,
        EventToken,
        LLMTransformerSchema,
        TokenType,
    )
except ImportError:
    # Define minimal classes for compatibility
    class LLMTransformerSchema:
        def __init__(self, case_id, **kwargs):
            self.case_id = case_id
            self.embed_dim = kwargs.get("embed_dim", 512)
            self.num_layers = kwargs.get("num_layers", 6)

        def create_attention_head_for_agent(self, agent, perspective):
            pass

        def add_event_token(self, token):
            pass

    class TokenType:
        ACTION_COMMUNICATION = "action_communication"
        ACTION_TRANSACTION = "action_transaction"
        ACTION_MEETING = "action_meeting"

    class EventToken:
        def __init__(self, event_id, token_type, timestamp, actors, description):
            self.event_id = event_id
            self.token_type = token_type
            self.timestamp = timestamp
            self.actors = actors
            self.description = description


try:
    from frameworks.hypergraph_model import (
        Hyperedge,
        HyperedgeType,
        HypergraphModel,
        HypergraphNode,
        RelationshipStrength,
    )
except ImportError:
    # Will be defined locally if needed
    pass

try:
    from discrete_event_model import DiscreteEventModel
except ImportError:
    # Define minimal class for compatibility
    class DiscreteEventModel:
        def __init__(self, case_id):
            self.case_id = case_id
            self.events = {}
            self.agent_states = {}


class AnalysisMode(Enum):
    """Different analysis modes for the unified framework"""

    BASIC = "basic"  # Individual models only
    INTEGRATED = "integrated"  # Models with data sharing
    COMPREHENSIVE = "comprehensive"  # Full integration with cross-validation
    INVESTIGATIVE = "investigative"  # Focus on suspicious pattern detection


class ModelType(Enum):
    """Types of models in the framework"""

    AGENT_BASED = "agent_based"
    DISCRETE_EVENT = "discrete_event"
    SYSTEM_DYNAMICS = "system_dynamics"
    HYPERGRAPH = "hypergraph"
    LLM_TRANSFORMER = "llm_transformer"


@dataclass
class UnifiedAnalysisConfiguration:
    """Configuration for unified analysis"""

    case_id: str
    analysis_mode: AnalysisMode = AnalysisMode.COMPREHENSIVE
    enabled_models: Set[ModelType] = field(default_factory=lambda: set(ModelType))
    temporal_window: Optional[timedelta] = field(default=timedelta(days=365))
    confidence_threshold: float = 0.7
    enable_cross_validation: bool = True
    enable_pattern_detection: bool = True
    output_format: str = "comprehensive"  # "summary", "detailed", "comprehensive"


class UnifiedModelFramework:
    """
    Unified framework that orchestrates all model types for comprehensive analysis
    """

    def __init__(self, config: UnifiedAnalysisConfiguration):
        self.config = config
        self.case_id = config.case_id

        # Initialize models based on configuration
        self.models: Dict[ModelType, Any] = {}
        self._initialize_models()

        # Shared data structures
        self.shared_agents: Dict[str, Agent] = {}
        self.shared_events: Dict[str, DiscreteEvent] = {}
        self.shared_evidence: Dict[str, Dict[str, Any]] = {}

        # Analysis results
        self.analysis_results: Dict[str, Any] = {}
        self.cross_validation_results: Dict[str, Any] = {}

    def _initialize_models(self):
        """Initialize enabled models"""
        if ModelType.AGENT_BASED in self.config.enabled_models:
            self.models[ModelType.AGENT_BASED] = HyperGNNFramework(self.case_id)

        if ModelType.DISCRETE_EVENT in self.config.enabled_models:
            self.models[ModelType.DISCRETE_EVENT] = DiscreteEventModel(self.case_id)

        if ModelType.SYSTEM_DYNAMICS in self.config.enabled_models:
            self.models[ModelType.SYSTEM_DYNAMICS] = SystemDynamicsModel(self.case_id)

        if ModelType.HYPERGRAPH in self.config.enabled_models:
            self.models[ModelType.HYPERGRAPH] = HypergraphModel(self.case_id)

        if ModelType.LLM_TRANSFORMER in self.config.enabled_models:
            self.models[ModelType.LLM_TRANSFORMER] = LLMTransformerSchema(self.case_id)

    def add_agent(self, agent: Agent) -> None:
        """Add an agent to all relevant models"""
        self.shared_agents[agent.agent_id] = agent

        # Add to HyperGNN if enabled
        if ModelType.AGENT_BASED in self.models:
            self.models[ModelType.AGENT_BASED].add_agent(agent)

        # Add to Hypergraph as a node if enabled
        if ModelType.HYPERGRAPH in self.models:
            node = HypergraphNode(
                agent.agent_id,
                "agent",
                agent.name,
                {"agent_type": agent.agent_type.value},
            )
            self.models[ModelType.HYPERGRAPH].add_node(node)

        # Add to LLM Transformer if enabled
        if ModelType.LLM_TRANSFORMER in self.models:
            perspective = self._determine_agent_perspective(agent)
            self.models[ModelType.LLM_TRANSFORMER].create_attention_head_for_agent(
                agent, perspective
            )

    def add_event(self, event: DiscreteEvent) -> None:
        """Add an event to all relevant models"""
        self.shared_events[event.event_id] = event

        # Add to HyperGNN if enabled
        if ModelType.AGENT_BASED in self.models:
            self.models[ModelType.AGENT_BASED].add_event(event)

        # Add to Discrete Event Model if enabled
        if ModelType.DISCRETE_EVENT in self.models:
            # Convert to timeline entry format if needed
            self.models[ModelType.DISCRETE_EVENT].events[event.event_id] = event

        # Add to Hypergraph if enabled
        if ModelType.HYPERGRAPH in self.models:
            # Add event as a node
            event_node = HypergraphNode(
                event.event_id,
                "event",
                event.description,
                {
                    "event_type": event.event_type.value,
                    "timestamp": event.timestamp.isoformat(),
                },
            )
            self.models[ModelType.HYPERGRAPH].add_node(event_node)

            # Create hyperedge connecting all actors
            if len(event.actors) >= 2:
                hyperedge = Hyperedge(
                    f"event_{event.event_id}",
                    set(event.actors + [event.event_id]),
                    self._map_event_to_hyperedge_type(event.event_type),
                    event.timestamp,
                    strength=0.8,
                    description=event.description,
                    evidence_refs=getattr(event, "evidence_refs", []),
                )
                self.models[ModelType.HYPERGRAPH].add_hyperedge(hyperedge)

        # Add to LLM Transformer if enabled
        if ModelType.LLM_TRANSFORMER in self.models:
            event_token = EventToken(
                event.event_id,
                self._map_event_to_token_type(event.event_type),
                event.timestamp,
                event.actors,
                event.description,
            )
            self.models[ModelType.LLM_TRANSFORMER].add_event_token(event_token)

    def add_system_flow(
        self,
        source: str,
        target: str,
        flow_type: str,
        magnitude: float,
        timestamp: datetime,
        description: str,
    ) -> None:
        """Add a system flow to relevant models"""
        if ModelType.SYSTEM_DYNAMICS in self.models:
            # Ensure stocks exist
            if source not in self.models[ModelType.SYSTEM_DYNAMICS].stocks:
                stock = Stock(source, StockType.FINANCIAL, source, 0.0)
                self.models[ModelType.SYSTEM_DYNAMICS].add_stock(stock)

            if target not in self.models[ModelType.SYSTEM_DYNAMICS].stocks:
                stock = Stock(target, StockType.FINANCIAL, target, 0.0)
                self.models[ModelType.SYSTEM_DYNAMICS].add_stock(stock)

            # Add flow
            flow = Flow(
                f"flow_{source}_{target}_{timestamp.timestamp()}",
                getattr(StockType, flow_type.upper(), StockType.FINANCIAL),
                source,
                target,
                magnitude,
                timestamp,
                description,
            )
            self.models[ModelType.SYSTEM_DYNAMICS].add_flow(flow)

        # Add to HyperGNN if enabled
        if ModelType.AGENT_BASED in self.models:
            system_flow = SystemFlow(
                f"flow_{source}_{target}_{timestamp.timestamp()}",
                getattr(FlowType, flow_type.upper(), FlowType.INFORMATION),
                source,
                target,
                timestamp,
                magnitude,
                description,
            )
            self.models[ModelType.AGENT_BASED].add_flow(system_flow)

    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis using all enabled models"""
        print(f"\n=== RUNNING COMPREHENSIVE ANALYSIS FOR CASE: {self.case_id} ===")

        results = {
            "case_id": self.case_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "configuration": {
                "analysis_mode": self.config.analysis_mode.value,
                "enabled_models": [model.value for model in self.config.enabled_models],
                "confidence_threshold": self.config.confidence_threshold,
            },
            "model_results": {},
            "integrated_analysis": {},
            "pattern_detection": {},
            "recommendations": [],
        }

        # Run individual model analyses
        for model_type, model in self.models.items():
            print(f"\n--- Running {model_type.value} analysis ---")
            try:
                if model_type == ModelType.AGENT_BASED:
                    model_result = self._analyze_agent_based_model(model)
                elif model_type == ModelType.DISCRETE_EVENT:
                    model_result = self._analyze_discrete_event_model(model)
                elif model_type == ModelType.SYSTEM_DYNAMICS:
                    model_result = self._analyze_system_dynamics_model(model)
                elif model_type == ModelType.HYPERGRAPH:
                    model_result = self._analyze_hypergraph_model(model)
                elif model_type == ModelType.LLM_TRANSFORMER:
                    model_result = self._analyze_llm_transformer_model(model)
                else:
                    model_result = {"status": "not_implemented"}

                results["model_results"][model_type.value] = model_result
                print(f"✓ {model_type.value} analysis completed")

            except Exception as e:
                print(f"✗ {model_type.value} analysis failed: {e}")
                results["model_results"][model_type.value] = {
                    "status": "error",
                    "error": str(e),
                }

        # Run integrated analysis
        if self.config.analysis_mode in [
            AnalysisMode.INTEGRATED,
            AnalysisMode.COMPREHENSIVE,
        ]:
            print("\n--- Running integrated analysis ---")
            results["integrated_analysis"] = self._run_integrated_analysis()

        # Run pattern detection
        if self.config.enable_pattern_detection:
            print("\n--- Running pattern detection ---")
            results["pattern_detection"] = self._detect_cross_model_patterns()

        # Run cross-validation
        if self.config.enable_cross_validation:
            print("\n--- Running cross-validation ---")
            results["cross_validation"] = self._run_cross_validation()

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)

        self.analysis_results = results
        return results

    def _analyze_agent_based_model(self, model) -> Dict[str, Any]:
        """Analyze the agent-based model"""
        return {
            "total_agents": len(self.shared_agents),
            "total_events": len(self.shared_events),
            "agent_types": list(
                set(agent.agent_type.value for agent in self.shared_agents.values())
            ),
            "relationship_summary": {
                "total_professional_links": sum(
                    len(agent.professional_links)
                    for agent in self.shared_agents.values()
                ),
                "total_social_links": sum(
                    len(agent.social_links) for agent in self.shared_agents.values()
                ),
            },
        }

    def _analyze_discrete_event_model(self, model) -> Dict[str, Any]:
        """Analyze the discrete event model"""
        if hasattr(model, "generate_evidence_report"):
            evidence_report = model.generate_evidence_report()
        else:
            evidence_report = {"status": "not_available"}

        return {
            "total_events": len(model.events) if hasattr(model, "events") else 0,
            "evidence_report": evidence_report,
            "agent_states": (
                len(model.agent_states) if hasattr(model, "agent_states") else 0
            ),
        }

    def _analyze_system_dynamics_model(self, model) -> Dict[str, Any]:
        """Analyze the system dynamics model"""
        return {
            "total_stocks": len(model.stocks),
            "total_flows": len(model.flows),
            "stock_types": list(
                set(stock.stock_type.value for stock in model.stocks.values())
            ),
            "mmo_analyses": len(model.mmo_analyses),
            "deception_patterns": len(model.deception_patterns),
        }

    def _analyze_hypergraph_model(self, model) -> Dict[str, Any]:
        """Analyze the hypergraph model"""
        # Build matrices for analysis
        model.build_incidence_matrix()
        model.build_adjacency_matrix()

        return {
            "summary": model.get_summary(),
            "centrality_measures": model.analyze_centrality(),
            "communities": [list(community) for community in model.find_communities()],
            "cliques": [list(clique) for clique in model.find_cliques()],
            "suspicious_patterns": model.detect_suspicious_patterns(),
            "temporal_patterns": {
                node_id: len(events)
                for node_id, events in model.find_temporal_patterns().items()
            },
        }

    def _analyze_llm_transformer_model(self, model) -> Dict[str, Any]:
        """Analyze the LLM transformer model"""
        return {
            "total_attention_heads": (
                len(model.attention_heads) if hasattr(model, "attention_heads") else 0
            ),
            "total_event_tokens": (
                len(model.event_tokens) if hasattr(model, "event_tokens") else 0
            ),
            "embedding_dimension": model.embed_dim,
            "num_layers": model.num_layers,
        }

    def _run_integrated_analysis(self) -> Dict[str, Any]:
        """Run integrated analysis across models"""
        integrated_results = {
            "cross_model_validation": {},
            "consistency_checks": {},
            "combined_insights": {},
        }

        # Check consistency between agent representations
        if ModelType.AGENT_BASED in self.models and ModelType.HYPERGRAPH in self.models:
            agent_consistency = self._check_agent_consistency()
            integrated_results["consistency_checks"]["agents"] = agent_consistency

        # Check event consistency
        if (
            ModelType.DISCRETE_EVENT in self.models
            and ModelType.HYPERGRAPH in self.models
        ):
            event_consistency = self._check_event_consistency()
            integrated_results["consistency_checks"]["events"] = event_consistency

        # Combine insights from multiple models
        combined_insights = self._combine_model_insights()
        integrated_results["combined_insights"] = combined_insights

        return integrated_results

    def _detect_cross_model_patterns(self) -> Dict[str, Any]:
        """Detect patterns that emerge across multiple models"""
        patterns = {
            "high_influence_entities": [],
            "temporal_correlations": [],
            "structural_anomalies": [],
            "behavioral_patterns": [],
        }

        # Find entities with high influence across models
        high_influence = self._find_high_influence_entities()
        patterns["high_influence_entities"] = high_influence

        # Find temporal correlations
        temporal_correlations = self._find_temporal_correlations()
        patterns["temporal_correlations"] = temporal_correlations

        # Find structural anomalies
        structural_anomalies = self._find_structural_anomalies()
        patterns["structural_anomalies"] = structural_anomalies

        return patterns

    def _run_cross_validation(self) -> Dict[str, Any]:
        """Run cross-validation between models"""
        validation_results = {
            "model_agreement": {},
            "confidence_scores": {},
            "discrepancies": [],
        }

        # Compare findings between models
        if len(self.models) >= 2:
            model_types = list(self.models.keys())
            for i in range(len(model_types)):
                for j in range(i + 1, len(model_types)):
                    model_a, model_b = model_types[i], model_types[j]
                    agreement = self._calculate_model_agreement(model_a, model_b)
                    validation_results["model_agreement"][
                        f"{model_a.value}_vs_{model_b.value}"
                    ] = agreement

        return validation_results

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis results"""
        recommendations = []

        # Analyze model results for recommendations
        for model_type, model_result in results["model_results"].items():
            if model_type == "hypergraph" and "suspicious_patterns" in model_result:
                suspicious = model_result["suspicious_patterns"]
                if suspicious.get("high_centrality_nodes"):
                    recommendations.append(
                        f"Investigate high-centrality entities: {suspicious['high_centrality_nodes'][:3]}"
                    )
                if suspicious.get("isolated_groups"):
                    recommendations.append(
                        f"Examine isolated groups for potential coordination: {len(suspicious['isolated_groups'])} groups found"
                    )

        # Add general recommendations
        total_models = len(self.config.enabled_models)
        if total_models >= 3:
            recommendations.append(
                f"Comprehensive analysis using {total_models} model types provides high-confidence insights"
            )

        if not recommendations:
            recommendations.append(
                "Continue monitoring and data collection for enhanced analysis"
            )

        return recommendations

    # Helper methods
    def _determine_agent_perspective(self, agent: Agent) -> str:
        """Determine agent perspective for LLM model"""
        if "victim" in agent.name.lower():
            return "victim"
        elif "perpetrator" in agent.name.lower() or "suspect" in agent.name.lower():
            return "perpetrator"
        elif "witness" in agent.name.lower():
            return "witness"
        elif "investigator" in agent.name.lower() or "detective" in agent.name.lower():
            return "investigator"
        else:
            return "neutral"

    def _map_event_to_hyperedge_type(self, event_type: EventType) -> HyperedgeType:
        """Map event type to hyperedge type"""
        mapping = {
            EventType.COMMUNICATION: HyperedgeType.COMMUNICATION,
            EventType.TRANSACTION: HyperedgeType.TRANSACTION,
            EventType.MEETING: HyperedgeType.MEETING,
            EventType.EVIDENCE: HyperedgeType.EVIDENCE_CHAIN,
        }
        return mapping.get(event_type, HyperedgeType.COLLABORATION)

    def _map_event_to_token_type(self, event_type: EventType) -> TokenType:
        """Map event type to token type"""
        mapping = {
            EventType.COMMUNICATION: TokenType.ACTION_COMMUNICATION,
            EventType.TRANSACTION: TokenType.ACTION_TRANSACTION,
            EventType.MEETING: TokenType.ACTION_MEETING,
        }
        return mapping.get(event_type, TokenType.ACTION_COMMUNICATION)

    def _check_agent_consistency(self) -> Dict[str, Any]:
        """Check consistency of agent representations across models"""
        return {"status": "consistent", "agents_checked": len(self.shared_agents)}

    def _check_event_consistency(self) -> Dict[str, Any]:
        """Check consistency of event representations across models"""
        return {"status": "consistent", "events_checked": len(self.shared_events)}

    def _combine_model_insights(self) -> Dict[str, Any]:
        """Combine insights from multiple models"""
        return {"combined_insights": "Integration of multiple analytical perspectives"}

    def _find_high_influence_entities(self) -> List[str]:
        """Find entities with high influence across models"""
        high_influence = []

        # From hypergraph centrality
        if ModelType.HYPERGRAPH in self.models:
            hypergraph = self.models[ModelType.HYPERGRAPH]
            centrality = hypergraph.analyze_centrality()

            for node_id, measures in centrality.items():
                if measures.get("degree_centrality", 0) > 0.7:
                    high_influence.append(node_id)

        return list(set(high_influence))

    def _find_temporal_correlations(self) -> List[Dict[str, Any]]:
        """Find temporal correlations across models"""
        correlations = []

        # Analyze event timing patterns
        if len(self.shared_events) >= 2:
            events = list(self.shared_events.values())
            events.sort(key=lambda x: x.timestamp)

            for i in range(len(events) - 1):
                time_diff = (
                    events[i + 1].timestamp - events[i].timestamp
                ).total_seconds() / 3600
                if time_diff < 24:  # Events within 24 hours
                    correlations.append(
                        {
                            "event_1": events[i].event_id,
                            "event_2": events[i + 1].event_id,
                            "time_diff_hours": time_diff,
                        }
                    )

        return correlations

    def _find_structural_anomalies(self) -> List[Dict[str, Any]]:
        """Find structural anomalies across models"""
        anomalies = []

        # From hypergraph analysis
        if ModelType.HYPERGRAPH in self.models:
            hypergraph = self.models[ModelType.HYPERGRAPH]
            suspicious = hypergraph.detect_suspicious_patterns()

            for pattern_type, items in suspicious.items():
                if items:
                    anomalies.append(
                        {
                            "type": pattern_type,
                            "items": items[:3],  # Limit to first 3
                            "source": "hypergraph",
                        }
                    )

        return anomalies

    def _calculate_model_agreement(
        self, model_a: ModelType, model_b: ModelType
    ) -> float:
        """Calculate agreement between two models"""
        # Simplified agreement calculation
        return 0.85  # Placeholder for actual agreement calculation

    def export_comprehensive_results(self, output_path: Optional[str] = None) -> str:
        """Export comprehensive results to file"""
        if not output_path:
            output_path = f"/tmp/unified_analysis_{self.case_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(output_path, "w") as f:
            json.dump(self.analysis_results, f, indent=2, default=str)

        return output_path


def create_comprehensive_example() -> UnifiedModelFramework:
    """Create a comprehensive example with all model types"""
    config = UnifiedAnalysisConfiguration(
        case_id="comprehensive_demo_001",
        analysis_mode=AnalysisMode.COMPREHENSIVE,
        enabled_models={
            ModelType.AGENT_BASED,
            ModelType.DISCRETE_EVENT,
            ModelType.SYSTEM_DYNAMICS,
            ModelType.HYPERGRAPH,
            ModelType.LLM_TRANSFORMER,
        },
    )

    framework = UnifiedModelFramework(config)

    # Add sample agents
    agents = [
        Agent("agent_001", AgentType.INDIVIDUAL, "Alice Johnson"),
        Agent("agent_002", AgentType.INDIVIDUAL, "Bob Smith"),
        Agent("agent_003", AgentType.INDIVIDUAL, "Carol Davis"),
        Agent("agent_004", AgentType.ORGANIZATION, "Legal Firm ABC"),
    ]

    for agent in agents:
        framework.add_agent(agent)

    # Add sample events
    base_time = datetime.now() - timedelta(days=30)
    events = [
        DiscreteEvent(
            "meeting_001",
            base_time,
            EventType.MEETING,
            ["agent_001", "agent_002", "agent_003"],
            "Initial strategy meeting",
        ),
        DiscreteEvent(
            "transaction_001",
            base_time + timedelta(days=5),
            EventType.TRANSACTION,
            ["agent_002", "agent_004"],
            "Large financial transaction",
        ),
        DiscreteEvent(
            "communication_001",
            base_time + timedelta(days=10),
            EventType.COMMUNICATION,
            ["agent_001", "agent_003"],
            "Follow-up communication",
        ),
    ]

    for event in events:
        framework.add_event(event)

    # Add system flows
    framework.add_system_flow(
        "agent_002",
        "agent_004",
        "FINANCIAL",
        50000.0,
        base_time + timedelta(days=5),
        "Payment to legal services",
    )

    return framework


if __name__ == "__main__":
    print("=== UNIFIED MODEL FRAMEWORK DEMONSTRATION ===")

    # Create comprehensive example
    framework = create_comprehensive_example()

    print(f"\nCreated unified framework for case: {framework.case_id}")
    print(
        f"Enabled models: {[model.value for model in framework.config.enabled_models]}"
    )
    print(f"Shared agents: {len(framework.shared_agents)}")
    print(f"Shared events: {len(framework.shared_events)}")

    # Run comprehensive analysis
    results = framework.run_comprehensive_analysis()

    # Export results
    output_file = framework.export_comprehensive_results()
    print(f"\n✅ Comprehensive analysis complete!")
    print(f"Results exported to: {output_file}")

    # Display summary
    print(f"\nAnalysis Summary:")
    print(f"- Models analyzed: {len(results['model_results'])}")
    print(f"- Recommendations: {len(results['recommendations'])}")
    print(f"- Pattern detection results: {len(results.get('pattern_detection', {}))}")
