#!/usr/bin/env python3
"""
Enhanced Simulation Runner
=========================

This module creates a comprehensive simulation runner that leverages all the enhanced
model capabilities to generate new insights through advanced simulations:

1. Agent-Based Simulations with behavioral dynamics
2. Discrete Event Cascade Simulations
3. System Dynamics Flow Optimization
4. Hypergraph Network Evolution
5. LLM Transformer Attention Analysis

The runner demonstrates the refined capabilities and generates actionable insights.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

# Import enhanced frameworks
from frameworks.hypergnn_core import Agent, AgentType, create_sample_framework
from frameworks.hypergraph_model import (
    Hyperedge,
    HyperedgeType,
    HypergraphModel,
    HypergraphNode,
    create_sample_hypergraph,
)
from frameworks.llm_transformer_schema import LLMTransformerSchema
from frameworks.system_dynamics import (
    Flow,
    FlowType,
    Stock,
    StockType,
    SystemDynamicsModel,
)
from src.models.discrete_event_model import DiscreteEventModel
from src.models.unified_model_framework import (
    AnalysisMode,
    ModelType,
    UnifiedAnalysisConfiguration,
    UnifiedModelFramework,
)


class EnhancedSimulationRunner:
    """
    Advanced simulation runner with enhanced model capabilities
    """

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.simulation_results = {}
        self.insights_generated = []

        # Initialize enhanced models
        self.hypergnn = create_sample_framework()
        self.discrete_event = DiscreteEventModel(case_id)
        self.system_dynamics = SystemDynamicsModel(case_id)
        self.hypergraph = create_sample_hypergraph()
        self.llm_transformer = LLMTransformerSchema(case_id)

        print(f"🚀 Enhanced Simulation Runner initialized for case: {case_id}")

    def run_comprehensive_simulation(self, simulation_days: int = 60) -> Dict[str, Any]:
        """
        Run comprehensive simulation across all enhanced model types
        """
        print(f"\n{'='*80}")
        print(f"ENHANCED COMPREHENSIVE SIMULATION - CASE: {self.case_id}")
        print(f"Duration: {simulation_days} days")
        print(f"{'='*80}")

        simulation_results = {
            "case_id": self.case_id,
            "simulation_start": datetime.now().isoformat(),
            "duration_days": simulation_days,
            "enhanced_simulations": {},
            "cross_model_insights": [],
            "predictive_analytics": {},
            "actionable_recommendations": [],
        }

        # 1. Enhanced Agent-Based Simulation
        print(f"\n{'-'*60}")
        print("1. ENHANCED AGENT-BASED SIMULATION")
        print(f"{'-'*60}")

        agent_simulation = self._run_enhanced_agent_simulation(simulation_days)
        simulation_results["enhanced_simulations"]["agent_based"] = agent_simulation

        # 2. Advanced Discrete Event Simulation
        print(f"\n{'-'*60}")
        print("2. ADVANCED DISCRETE EVENT SIMULATION")
        print(f"{'-'*60}")

        event_simulation = self._run_enhanced_event_simulation(simulation_days)
        simulation_results["enhanced_simulations"]["discrete_event"] = event_simulation

        # 3. Dynamic System Flows Simulation
        print(f"\n{'-'*60}")
        print("3. DYNAMIC SYSTEM FLOWS SIMULATION")
        print(f"{'-'*60}")

        flow_simulation = self._run_enhanced_flow_simulation(simulation_days)
        simulation_results["enhanced_simulations"]["system_dynamics"] = flow_simulation

        # 4. Network Evolution Analysis
        print(f"\n{'-'*60}")
        print("4. NETWORK EVOLUTION ANALYSIS")
        print(f"{'-'*60}")

        network_analysis = self._run_enhanced_network_analysis(simulation_days)
        simulation_results["enhanced_simulations"]["hypergraph"] = network_analysis

        # 5. Advanced Attention Analysis
        print(f"\n{'-'*60}")
        print("5. ADVANCED ATTENTION ANALYSIS")
        print(f"{'-'*60}")

        attention_analysis = self._run_enhanced_attention_analysis(simulation_days)
        simulation_results["enhanced_simulations"][
            "llm_transformer"
        ] = attention_analysis

        # 6. Cross-Model Integration & Insights
        print(f"\n{'-'*60}")
        print("6. CROSS-MODEL INTEGRATION & INSIGHTS")
        print(f"{'-'*60}")

        cross_insights = self._generate_cross_model_insights(
            simulation_results["enhanced_simulations"]
        )
        simulation_results["cross_model_insights"] = cross_insights

        # 7. Predictive Analytics
        print(f"\n{'-'*60}")
        print("7. PREDICTIVE ANALYTICS")
        print(f"{'-'*60}")

        predictive_analytics = self._generate_predictive_analytics(simulation_results)
        simulation_results["predictive_analytics"] = predictive_analytics

        # 8. Generate Actionable Recommendations
        print(f"\n{'-'*60}")
        print("8. ACTIONABLE RECOMMENDATIONS")
        print(f"{'-'*60}")

        recommendations = self._generate_actionable_recommendations(simulation_results)
        simulation_results["actionable_recommendations"] = recommendations

        # Export results
        self._export_simulation_results(simulation_results)

        return simulation_results

    def _run_enhanced_agent_simulation(self, days: int) -> Dict[str, Any]:
        """Run enhanced multi-agent simulation"""
        print("Running multi-agent behavioral simulation...")

        # Run the enhanced multi-agent simulation
        multi_agent_sim = self.hypergnn.run_multi_agent_simulation(days)

        # Extract key insights
        insights = {
            "emergent_patterns_count": len(
                multi_agent_sim.get("emergent_patterns", [])
            ),
            "system_stability_trend": self._analyze_stability_trend(
                multi_agent_sim.get("system_dynamics", [])
            ),
            "network_evolution_score": self._calculate_network_evolution_score(
                multi_agent_sim.get("interaction_network_evolution", [])
            ),
            "agent_adaptation_metrics": self._summarize_adaptation_metrics(
                multi_agent_sim.get("agent_simulations", {})
            ),
        }

        print(f"✓ Multi-agent simulation complete:")
        print(f"  - Emergent patterns: {insights['emergent_patterns_count']}")
        print(f"  - System stability: {insights['system_stability_trend']:.3f}")
        print(f"  - Network evolution: {insights['network_evolution_score']:.3f}")

        return {
            "simulation_data": multi_agent_sim,
            "insights": insights,
            "recommendations": self._generate_agent_recommendations(insights),
        }

    def _run_enhanced_event_simulation(self, days: int) -> Dict[str, Any]:
        """Run enhanced discrete event simulation"""
        print("Running event cascade and temporal analysis...")

        # First, create some sample events for simulation
        self._populate_sample_events()

        # Run temporal sensitivity analysis
        sensitivity_analysis = self.discrete_event.run_temporal_sensitivity_analysis()

        # Generate predictive insights
        predictive_insights = self.discrete_event.generate_predictive_insights(days)

        insights = {
            "critical_windows_count": len(
                sensitivity_analysis.get("critical_windows", [])
            ),
            "temporal_dependencies": len(
                sensitivity_analysis.get("temporal_dependencies", [])
            ),
            "prediction_confidence": predictive_insights.get(
                "prediction_confidence", 0.0
            ),
            "likely_events_count": len(predictive_insights.get("likely_events", [])),
        }

        print(f"✓ Event simulation complete:")
        print(f"  - Critical windows: {insights['critical_windows_count']}")
        print(f"  - Temporal dependencies: {insights['temporal_dependencies']}")
        print(f"  - Prediction confidence: {insights['prediction_confidence']:.3f}")

        return {
            "sensitivity_analysis": sensitivity_analysis,
            "predictive_insights": predictive_insights,
            "insights": insights,
            "recommendations": self._generate_event_recommendations(insights),
        }

    def _run_enhanced_flow_simulation(self, days: int) -> Dict[str, Any]:
        """Run enhanced system dynamics simulation"""
        print("Running dynamic flow simulation and optimization...")

        # First, populate sample stocks and flows
        self._populate_sample_stocks_flows()

        # Run flow dynamics simulation
        flow_simulation = self.system_dynamics.simulate_flow_dynamics(days)

        # Run vulnerability analysis
        vulnerability_analysis = self.system_dynamics.analyze_vulnerability_patterns()

        # Test optimization
        target_stocks = {
            list(self.system_dynamics.stocks.keys())[0]: 0.8
        }  # Sample target
        optimization = self.system_dynamics.optimize_resource_allocation(target_stocks)

        insights = {
            "emergent_behaviors_count": len(
                flow_simulation.get("emergent_behaviors", [])
            ),
            "system_stability": (
                np.mean(
                    [
                        s["stability_index"]
                        for s in flow_simulation.get("system_states", [])
                    ]
                )
                if flow_simulation.get("system_states")
                else 0
            ),
            "vulnerability_score": len(
                vulnerability_analysis.get("structural_vulnerabilities", [])
            )
            + len(vulnerability_analysis.get("flow_vulnerabilities", [])),
            "optimization_efficiency": optimization.get("optimization_metrics", {}).get(
                "efficiency_score", 0.0
            ),
        }

        print(f"✓ Flow simulation complete:")
        print(f"  - Emergent behaviors: {insights['emergent_behaviors_count']}")
        print(f"  - System stability: {insights['system_stability']:.3f}")
        print(f"  - Vulnerability score: {insights['vulnerability_score']}")

        return {
            "flow_simulation": flow_simulation,
            "vulnerability_analysis": vulnerability_analysis,
            "optimization": optimization,
            "insights": insights,
            "recommendations": self._generate_flow_recommendations(insights),
        }

    def _run_enhanced_network_analysis(self, days: int) -> Dict[str, Any]:
        """Run enhanced hypergraph network analysis"""
        print("Running network evolution and community analysis...")

        # Analyze current network structure
        communities = self.hypergraph.find_communities()
        patterns = self.hypergraph.detect_suspicious_patterns()
        centrality_analysis = self.hypergraph.analyze_centrality()

        insights = {
            "community_count": len(communities),
            "suspicious_patterns_count": len(patterns),
            "network_density": len(self.hypergraph.hyperedges)
            / max(1, len(self.hypergraph.nodes)),
            "influence_concentration": self._calculate_influence_concentration(
                centrality_analysis
            ),
        }

        print(f"✓ Network analysis complete:")
        print(f"  - Communities detected: {insights['community_count']}")
        print(f"  - Suspicious patterns: {insights['suspicious_patterns_count']}")
        print(f"  - Network density: {insights['network_density']:.3f}")

        return {
            "communities": communities,
            "suspicious_patterns": patterns,
            "centrality_analysis": centrality_analysis,
            "insights": insights,
            "recommendations": self._generate_network_recommendations(insights),
        }

    def _run_enhanced_attention_analysis(self, days: int) -> Dict[str, Any]:
        """Run enhanced LLM attention analysis"""
        print("Running advanced attention mechanism analysis...")

        # Create sample timeline for attention analysis
        timeline = self._create_sample_timeline()

        # Analyze attention patterns - convert timeline to events format
        from frameworks.hypergnn_core import DiscreteEvent, EventType

        timeline_events = []
        for item in timeline:
            event = DiscreteEvent(
                event_id=f"timeline_{len(timeline_events)}",
                timestamp=datetime.fromisoformat(item["timestamp"]),
                event_type=getattr(
                    EventType, item["event_type"].upper(), EventType.COMMUNICATION
                ),
                actors=item["agents"],
                description=item["description"],
            )
            timeline_events.append(event)

        # Process timeline with attention
        attention_analysis = self.llm_transformer.process_timeline_with_attention(
            timeline_events, self.hypergnn.agents
        )
        transformer_export = self.llm_transformer.export_transformer_analysis()

        insights = {
            "attention_heads_active": len(
                attention_analysis.get("attention_weights", {})
            ),
            "perspective_diversity": self._calculate_perspective_diversity(
                transformer_export
            ),
            "temporal_focus_strength": len(
                attention_analysis.get("timeline_sequence", [])
            )
            / max(1, len(timeline)),
            "cross_attention_complexity": len(
                attention_analysis.get("agent_perspectives", {})
            ),
        }

        print(f"✓ Attention analysis complete:")
        print(f"  - Active attention heads: {insights['attention_heads_active']}")
        print(f"  - Perspective diversity: {insights['perspective_diversity']:.3f}")
        print(f"  - Temporal focus: {insights['temporal_focus_strength']:.3f}")

        return {
            "attention_analysis": attention_analysis,
            "transformer_export": transformer_export,
            "insights": insights,
            "recommendations": self._generate_attention_recommendations(insights),
        }

    def _generate_cross_model_insights(
        self, simulations: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate insights by correlating across all model types"""
        print("Generating cross-model insights...")

        insights = []

        # Agent-Event correlation
        agent_insights = simulations.get("agent_based", {}).get("insights", {})
        event_insights = simulations.get("discrete_event", {}).get("insights", {})

        if (
            agent_insights.get("emergent_patterns_count", 0) > 2
            and event_insights.get("critical_windows_count", 0) > 1
        ):
            insights.append(
                {
                    "insight_type": "behavioral_temporal_correlation",
                    "confidence": 0.85,
                    "description": "Agent behavioral patterns correlate with critical temporal windows",
                    "actionable": True,
                    "priority": "high",
                }
            )

        # Flow-Network correlation
        flow_insights = simulations.get("system_dynamics", {}).get("insights", {})
        network_insights = simulations.get("hypergraph", {}).get("insights", {})

        if (
            flow_insights.get("vulnerability_score", 0) > 3
            and network_insights.get("suspicious_patterns_count", 0) > 2
        ):
            insights.append(
                {
                    "insight_type": "flow_network_vulnerability",
                    "confidence": 0.78,
                    "description": "System flow vulnerabilities align with suspicious network patterns",
                    "actionable": True,
                    "priority": "high",
                }
            )

        # Attention-Behavioral correlation
        attention_insights = simulations.get("llm_transformer", {}).get("insights", {})

        if (
            attention_insights.get("temporal_focus_strength", 0) > 0.6
            and agent_insights.get("system_stability_trend", 0) < 0.5
        ):
            insights.append(
                {
                    "insight_type": "attention_instability_correlation",
                    "confidence": 0.72,
                    "description": "Strong temporal attention focus correlates with system instability",
                    "actionable": True,
                    "priority": "medium",
                }
            )

        print(f"✓ Generated {len(insights)} cross-model insights")
        return insights

    def _generate_predictive_analytics(
        self, simulation_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate predictive analytics from simulation results"""
        print("Generating predictive analytics...")

        analytics = {
            "forecast_horizon_days": 90,
            "confidence_intervals": {},
            "risk_predictions": [],
            "opportunity_predictions": [],
            "scenario_probabilities": {},
        }

        # Extract prediction data from discrete event model
        event_predictions = (
            simulation_results.get("enhanced_simulations", {})
            .get("discrete_event", {})
            .get("predictive_insights", {})
        )
        likely_events = event_predictions.get("likely_events", [])

        # Risk predictions
        high_risk_events = [e for e in likely_events if e["probability"] > 0.7]
        for event in high_risk_events[:3]:  # Top 3 risks
            analytics["risk_predictions"].append(
                {
                    "risk_type": event["event_type"],
                    "probability": event["probability"],
                    "predicted_timeframe": event["predicted_date"],
                    "mitigation_priority": (
                        "high" if event["probability"] > 0.8 else "medium"
                    ),
                }
            )

        # Scenario probabilities
        agent_stability = (
            simulation_results.get("enhanced_simulations", {})
            .get("agent_based", {})
            .get("insights", {})
            .get("system_stability_trend", 0.5)
        )
        flow_stability = (
            simulation_results.get("enhanced_simulations", {})
            .get("system_dynamics", {})
            .get("insights", {})
            .get("system_stability", 0.5)
        )

        analytics["scenario_probabilities"] = {
            "stable_outcome": min(agent_stability, flow_stability),
            "moderate_disruption": 1 - max(agent_stability, flow_stability),
            "high_volatility": max(0, 1 - agent_stability - flow_stability),
        }

        print(f"✓ Predictive analytics complete:")
        print(f"  - Risk predictions: {len(analytics['risk_predictions'])}")
        print(f"  - Scenario probabilities calculated")

        return analytics

    def _generate_actionable_recommendations(
        self, simulation_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations from all simulations"""
        print("Generating actionable recommendations...")

        recommendations = []

        # High-priority recommendations from cross-model insights
        cross_insights = simulation_results.get("cross_model_insights", [])
        for insight in cross_insights:
            if insight.get("priority") == "high" and insight.get("actionable"):
                recommendations.append(
                    {
                        "recommendation_id": f"cross_{len(recommendations)}",
                        "type": "strategic",
                        "priority": "high",
                        "title": f"Address {insight['insight_type']}",
                        "description": insight["description"],
                        "confidence": insight["confidence"],
                        "implementation_timeframe": "immediate",
                        "expected_impact": "high",
                        "resource_requirements": [
                            "analysis_team",
                            "monitoring_systems",
                        ],
                    }
                )

        # Predictive recommendations
        risk_predictions = simulation_results.get("predictive_analytics", {}).get(
            "risk_predictions", []
        )
        for risk in risk_predictions:
            if risk["probability"] > 0.75:
                recommendations.append(
                    {
                        "recommendation_id": f"pred_{len(recommendations)}",
                        "type": "preventive",
                        "priority": risk["mitigation_priority"],
                        "title": f"Mitigate {risk['risk_type']} risk",
                        "description": f"High probability ({risk['probability']:.2f}) of {risk['risk_type']} event",
                        "confidence": risk["probability"],
                        "implementation_timeframe": "within_7_days",
                        "expected_impact": "risk_reduction",
                        "resource_requirements": [
                            "incident_response_team",
                            "monitoring_enhancement",
                        ],
                    }
                )

        # System optimization recommendations
        flow_insights = (
            simulation_results.get("enhanced_simulations", {})
            .get("system_dynamics", {})
            .get("insights", {})
        )
        if flow_insights.get("optimization_efficiency", 0) < 0.6:
            recommendations.append(
                {
                    "recommendation_id": f"opt_{len(recommendations)}",
                    "type": "optimization",
                    "priority": "medium",
                    "title": "Optimize resource allocation",
                    "description": "System flow efficiency is below optimal levels",
                    "confidence": 0.8,
                    "implementation_timeframe": "within_30_days",
                    "expected_impact": "efficiency_improvement",
                    "resource_requirements": [
                        "resource_management_team",
                        "optimization_tools",
                    ],
                }
            )

        print(f"✓ Generated {len(recommendations)} actionable recommendations")

        # Sort by priority and confidence
        priority_order = {"high": 3, "medium": 2, "low": 1}
        recommendations.sort(
            key=lambda x: (priority_order.get(x["priority"], 0), x["confidence"]),
            reverse=True,
        )

        return recommendations

    def _export_simulation_results(self, results: Dict[str, Any]) -> str:
        """Export comprehensive simulation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/tmp/enhanced_simulation_{self.case_id}_{timestamp}.json"

        # Create a summary for easy reading
        summary = {
            "case_id": self.case_id,
            "simulation_summary": {
                "total_simulations": 5,
                "cross_model_insights": len(results.get("cross_model_insights", [])),
                "risk_predictions": len(
                    results.get("predictive_analytics", {}).get("risk_predictions", [])
                ),
                "actionable_recommendations": len(
                    results.get("actionable_recommendations", [])
                ),
                "highest_confidence_recommendation": max(
                    results.get("actionable_recommendations", []),
                    key=lambda x: x["confidence"],
                    default={},
                ),
            },
        }
        results["simulation_summary"] = summary["simulation_summary"]

        with open(filename, "w") as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n✅ Enhanced simulation results exported to: {filename}")
        return filename

    # Helper methods for simulation components
    def _populate_sample_events(self):
        """Populate discrete event model with sample events"""
        from enhanced_timeline_processor import (
            TimelineEntry,
            TimelineEntryType,
            VerificationLevel,
        )

        sample_entries = {
            "event_1": TimelineEntry(
                entry_id="event_1",
                date=datetime.now() - timedelta(days=10),
                title="Initial Contact",
                description="Initial contact established",
                entry_type=TimelineEntryType.COMMUNICATION,
                verification_level=VerificationLevel.DOCUMENTED,
                evidence_references=["doc1"],
                participants=["agent_001", "agent_002"],
            ),
            "event_2": TimelineEntry(
                entry_id="event_2",
                date=datetime.now() - timedelta(days=5),
                title="Financial Transaction",
                description="Financial transaction recorded",
                entry_type=TimelineEntryType.EVIDENCE_DISCOVERY,
                verification_level=VerificationLevel.RECORDED,
                evidence_references=["doc2"],
                participants=["agent_001"],
            ),
        }

        self.discrete_event.process_timeline(sample_entries)

    def _populate_sample_stocks_flows(self):
        """Populate system dynamics with sample stocks and flows"""
        # Add sample stocks
        stocks = [
            Stock(
                "financial_001",
                StockType.FINANCIAL,
                "entity_001",
                1000.0,
                "USD",
                "Financial reserves",
                datetime.now(),
            ),
            Stock(
                "influence_001",
                StockType.INFLUENCE,
                "entity_001",
                0.7,
                "score",
                "Network influence",
                datetime.now(),
            ),
            Stock(
                "information_001",
                StockType.INFORMATION,
                "entity_002",
                0.8,
                "level",
                "Information access",
                datetime.now(),
            ),
            Stock(
                "leverage_001",
                StockType.LEVERAGE,
                "entity_002",
                0.4,
                "factor",
                "Leverage position",
                datetime.now(),
            ),
        ]

        for stock in stocks:
            self.system_dynamics.add_stock(stock)

        # Add sample flows
        flows = [
            Flow(
                "flow_001",
                FlowType.TRANSFER,
                "financial_001",
                "influence_001",
                100.0,
                datetime.now() - timedelta(days=3),
                "Financial to influence conversion",
            ),
            Flow(
                "flow_002",
                FlowType.EXCHANGE,
                "information_001",
                "leverage_001",
                0.3,
                datetime.now() - timedelta(days=1),
                "Information-leverage exchange",
            ),
        ]

        for flow in flows:
            self.system_dynamics.add_flow(flow)

    def _create_sample_timeline(self) -> List[Dict[str, Any]]:
        """Create sample timeline for attention analysis"""
        return [
            {
                "timestamp": (datetime.now() - timedelta(days=10)).isoformat(),
                "event_type": "communication",
                "agents": ["agent_001", "agent_002"],
                "description": "Initial communication event",
            },
            {
                "timestamp": (datetime.now() - timedelta(days=5)).isoformat(),
                "event_type": "transaction",
                "agents": ["agent_001"],
                "description": "Financial transaction",
            },
        ]

    # Analysis helper methods
    def _analyze_stability_trend(self, system_dynamics: List[Dict[str, Any]]) -> float:
        """Analyze system stability trend"""
        if not system_dynamics:
            return 0.5

        stabilities = [s.get("system_stability", 0.5) for s in system_dynamics]
        if len(stabilities) < 2:
            return stabilities[0] if stabilities else 0.5

        # Calculate trend (positive = improving, negative = declining)
        trend = np.corrcoef(range(len(stabilities)), stabilities)[0, 1]
        return max(0, min(1, 0.5 + trend))

    def _calculate_network_evolution_score(
        self, network_evolution: List[Dict[str, Any]]
    ) -> float:
        """Calculate network evolution score"""
        if not network_evolution:
            return 0.5

        # Average network density over time
        densities = [n.get("network_density", 0.5) for n in network_evolution]
        return np.mean(densities) if densities else 0.5

    def _summarize_adaptation_metrics(
        self, agent_sims: Dict[str, Any]
    ) -> Dict[str, float]:
        """Summarize agent adaptation metrics"""
        if not agent_sims:
            return {"adaptation_rate": 0.0, "learning_rate": 0.0, "stability": 0.5}

        all_metrics = []
        for sim_data in agent_sims.values():
            metrics = sim_data.get("adaptation_metrics", {})
            if metrics:
                all_metrics.append(metrics)

        if not all_metrics:
            return {"adaptation_rate": 0.0, "learning_rate": 0.0, "stability": 0.5}

        return {
            "adaptation_rate": np.mean(
                [m.get("adaptation_rate", 0) for m in all_metrics]
            ),
            "learning_rate": np.mean([m.get("learning_rate", 0) for m in all_metrics]),
            "stability": np.mean([m.get("stability", 0.5) for m in all_metrics]),
        }

    def _calculate_influence_concentration(
        self, centrality_analysis: Dict[str, Any]
    ) -> float:
        """Calculate influence concentration score"""
        if not centrality_analysis:
            return 0.5

        # Try to extract centrality scores from any available centrality measure
        scores = []
        for measure_name, measure_data in centrality_analysis.items():
            if isinstance(measure_data, dict):
                scores.extend(measure_data.values())

        if not scores:
            return 0.5

        # Gini coefficient for concentration
        sorted_scores = sorted(
            [float(s) for s in scores if isinstance(s, (int, float))]
        )
        if not sorted_scores:
            return 0.5

        n = len(sorted_scores)
        cumsum = np.cumsum(sorted_scores)
        return (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n if cumsum[-1] > 0 else 0

    def _calculate_perspective_diversity(
        self, transformer_data: Dict[str, Any]
    ) -> float:
        """Calculate perspective diversity score"""
        if not transformer_data:
            return 0.5

        # Look for perspective insights or agent perspectives
        perspectives = transformer_data.get("perspective_insights", {})
        if not perspectives:
            perspectives = transformer_data.get("agent_perspectives", {})

        if not perspectives:
            return 0.5

        # Simple diversity measure based on number of unique perspectives
        unique_perspectives = len(set(str(p) for p in perspectives.values()))
        total_perspectives = len(perspectives)

        return (
            unique_perspectives / max(1, total_perspectives)
            if total_perspectives > 0
            else 0.5
        )

    # Recommendation generators for individual models
    def _generate_agent_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate recommendations from agent simulation insights"""
        recommendations = []

        if insights.get("emergent_patterns_count", 0) > 2:
            recommendations.append(
                "Monitor emergent behavioral patterns for potential coordinated activity"
            )

        if insights.get("system_stability_trend", 0.5) < 0.4:
            recommendations.append(
                "Implement stability monitoring due to declining system stability"
            )

        return recommendations

    def _generate_event_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate recommendations from event simulation insights"""
        recommendations = []

        if insights.get("critical_windows_count", 0) > 2:
            recommendations.append(
                "Focus investigation on identified critical temporal windows"
            )

        if insights.get("prediction_confidence", 0) > 0.7:
            recommendations.append(
                "Utilize high-confidence predictions for proactive planning"
            )

        return recommendations

    def _generate_flow_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate recommendations from flow simulation insights"""
        recommendations = []

        if insights.get("vulnerability_score", 0) > 4:
            recommendations.append(
                "Address identified system vulnerabilities immediately"
            )

        if insights.get("optimization_efficiency", 0) < 0.6:
            recommendations.append("Implement resource allocation optimization")

        return recommendations

    def _generate_network_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate recommendations from network analysis insights"""
        recommendations = []

        if insights.get("suspicious_patterns_count", 0) > 2:
            recommendations.append("Investigate detected suspicious network patterns")

        if insights.get("influence_concentration", 0) > 0.7:
            recommendations.append(
                "Monitor high influence concentration for potential risks"
            )

        return recommendations

    def _generate_attention_recommendations(
        self, insights: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations from attention analysis insights"""
        recommendations = []

        if insights.get("temporal_focus_strength", 0) > 0.8:
            recommendations.append(
                "Investigate periods of high temporal attention focus"
            )

        if insights.get("perspective_diversity", 0) < 0.3:
            recommendations.append(
                "Consider diverse perspectives to reduce analytical blind spots"
            )

        return recommendations


def main():
    """Main execution function for enhanced simulation"""
    print("🚀 ENHANCED SIMULATION RUNNER")
    print("============================")

    # Create simulation runner
    case_id = f"enhanced_sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    runner = EnhancedSimulationRunner(case_id)

    # Run comprehensive simulation
    try:
        results = runner.run_comprehensive_simulation(simulation_days=45)

        # Print summary
        print(f"\n{'='*80}")
        print("ENHANCED SIMULATION COMPLETE")
        print(f"{'='*80}")

        summary = results.get("simulation_summary", {})
        print(f"Case ID: {case_id}")
        print(f"Simulations Run: {summary.get('total_simulations', 0)}")
        print(f"Cross-Model Insights: {summary.get('cross_model_insights', 0)}")
        print(f"Risk Predictions: {summary.get('risk_predictions', 0)}")
        print(
            f"Actionable Recommendations: {summary.get('actionable_recommendations', 0)}"
        )

        # Show top recommendations
        recommendations = results.get("actionable_recommendations", [])
        if recommendations:
            print(f"\n🎯 TOP RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"  {i}. [{rec['priority'].upper()}] {rec['title']}")
                print(
                    f"     Confidence: {rec['confidence']:.2f} | Impact: {rec['expected_impact']}"
                )

        print(f"\n✅ Enhanced simulation successfully completed!")

    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
