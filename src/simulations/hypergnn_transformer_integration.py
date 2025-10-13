#!/usr/bin/env python3
"""
HyperGNN Transformer Integration
===============================

This module demonstrates the integration of the LLM/Transformer schema
with the existing HyperGNN framework, showing how agent perspectives
can be mapped to attention heads for comprehensive timeline analysis.

Example Usage:
    python3 hypergnn_transformer_integration.py
"""

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List

import numpy as np

from frameworks.hypergnn_core import (
    Agent,
    AgentType,
    DiscreteEvent,
    EventType,
    FlowType,
    HyperGNNFramework,
    SystemFlow,
    TensorType,
)
from frameworks.llm_transformer_schema import LLMTransformerSchema, TokenType


def create_comprehensive_case_example() -> (
    tuple[HyperGNNFramework, LLMTransformerSchema]
):
    """Create a comprehensive case example with multiple agents and events"""

    # Initialize HyperGNN Framework
    framework = HyperGNNFramework("comprehensive_case_001")

    # Create multiple agents with different perspectives
    agents = [
        Agent("victim_001", AgentType.INDIVIDUAL, "Alice Johnson"),
        Agent("perpetrator_001", AgentType.INDIVIDUAL, "Bob Smith"),
        Agent("witness_001", AgentType.INDIVIDUAL, "Carol Davis"),
        Agent("investigator_001", AgentType.INDIVIDUAL, "Detective Moore"),
        Agent("organization_001", AgentType.ORGANIZATION, "Legal Firm ABC"),
    ]

    # Set up relationships
    agents[0].social_links.add("witness_001")  # Victim knows witness
    agents[1].professional_links.add(
        "organization_001"
    )  # Perpetrator connected to firm
    agents[2].social_links.add("victim_001")  # Witness knows victim
    agents[3].professional_links.add(
        "investigator_001"
    )  # Self-reference for investigator

    # Add agents to framework
    for agent in agents:
        framework.add_agent(agent)

    # Create timeline of events
    base_time = datetime.now() - timedelta(days=30)

    events = [
        DiscreteEvent(
            "initial_contact",
            base_time,
            EventType.COMMUNICATION,
            ["victim_001", "perpetrator_001"],
            "Initial professional contact between parties",
            evidence_refs=["email_001", "phone_log_001"],
        ),
        DiscreteEvent(
            "financial_transaction",
            base_time + timedelta(days=5),
            EventType.TRANSACTION,
            ["perpetrator_001", "organization_001"],
            "Large financial transfer to legal firm",
            evidence_refs=["bank_record_001", "wire_transfer_001"],
        ),
        DiscreteEvent(
            "witness_meeting",
            base_time + timedelta(days=10),
            EventType.MEETING,
            ["victim_001", "witness_001"],
            "Private meeting between victim and witness",
            evidence_refs=["calendar_entry_001", "location_data_001"],
        ),
        DiscreteEvent(
            "strategic_decision",
            base_time + timedelta(days=15),
            EventType.DECISION,
            ["perpetrator_001", "organization_001"],
            "Decision to proceed with legal action",
            evidence_refs=["legal_memo_001", "strategy_document_001"],
        ),
        DiscreteEvent(
            "investigation_action",
            base_time + timedelta(days=20),
            EventType.ACTION,
            ["investigator_001"],
            "Formal investigation initiated",
            evidence_refs=["case_file_001", "warrant_001"],
        ),
        DiscreteEvent(
            "evidence_collection",
            base_time + timedelta(days=25),
            EventType.EVIDENCE,
            ["investigator_001", "witness_001"],
            "Evidence collection with witness testimony",
            evidence_refs=["testimony_001", "physical_evidence_001"],
        ),
    ]

    # Add events to framework
    for event in events:
        framework.add_event(event)

    # Create system flows
    flows = [
        SystemFlow(
            "financial_flow_001",
            FlowType.FINANCIAL,
            "perpetrator_001",
            "organization_001",
            base_time + timedelta(days=5),
            50000.0,
            "Large payment to legal representation",
        ),
        SystemFlow(
            "information_flow_001",
            FlowType.INFORMATION,
            "witness_001",
            "investigator_001",
            base_time + timedelta(days=25),
            1.0,
            "Witness information shared with investigation",
        ),
        SystemFlow(
            "influence_flow_001",
            FlowType.INFLUENCE,
            "organization_001",
            "perpetrator_001",
            base_time + timedelta(days=15),
            0.8,
            "Legal counsel influence on decision making",
        ),
    ]

    # Add flows to framework
    for flow in flows:
        framework.add_flow(flow)

    # Initialize Transformer Schema
    transformer_schema = LLMTransformerSchema(
        case_id=framework.case_id, num_layers=6, embed_dim=512, num_heads=8
    )

    # Create specialized attention heads for different perspectives
    perspectives = {
        "victim_001": "victim",
        "perpetrator_001": "perpetrator",
        "witness_001": "witness",
        "investigator_001": "investigator",
        "organization_001": "organization",
    }

    for agent_id, perspective in perspectives.items():
        if agent_id in framework.agents:
            transformer_schema.create_attention_head_for_agent(
                framework.agents[agent_id], perspective
            )

    return framework, transformer_schema


def demonstrate_attention_analysis(
    framework: HyperGNNFramework, transformer_schema: LLMTransformerSchema
) -> Dict[str, Any]:
    """Demonstrate comprehensive attention analysis"""

    print("=== HyperGNN Transformer Integration Demo ===\n")

    # Process timeline with transformer attention
    events = list(framework.events.values())
    agents = framework.agents

    print(f"Processing {len(events)} events with {len(agents)} agents...")

    # Run transformer analysis
    transformer_analysis = transformer_schema.process_timeline_with_attention(
        events, agents
    )

    print(f"Generated {transformer_analysis['tokenized_sequence_length']} tokens")
    print(f"Created {transformer_analysis['attention_heads']} attention heads")

    # Analyze traditional HyperGNN metrics
    hypergnn_analysis = framework.export_professional_report()

    # Combine analyses
    combined_analysis = {
        "case_overview": {
            "case_id": framework.case_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "total_agents": len(agents),
            "total_events": len(events),
            "total_flows": len(framework.flows),
        },
        "hypergnn_analysis": hypergnn_analysis,
        "transformer_analysis": transformer_analysis,
        "integrated_insights": generate_integrated_insights(
            hypergnn_analysis, transformer_analysis, transformer_schema
        ),
    }

    return combined_analysis


def generate_integrated_insights(
    hypergnn_analysis: Dict[str, Any],
    transformer_analysis: Dict[str, Any],
    transformer_schema: LLMTransformerSchema,
) -> Dict[str, Any]:
    """Generate insights by combining HyperGNN and Transformer analyses"""

    insights = {
        "perspective_agent_correlation": {},
        "attention_network_alignment": {},
        "mmo_transformer_enhancement": {},
        "deception_pattern_validation": {},
    }

    # Correlate transformer attention with HyperGNN network metrics
    if (
        "network_metrics" in hypergnn_analysis
        and "perspective_insights" in transformer_analysis
    ):
        network_density = hypergnn_analysis["network_metrics"].get("density", 0)
        avg_perspective_correlation = np.mean(
            list(transformer_analysis["perspective_insights"].values())
        )

        insights["attention_network_alignment"] = {
            "network_density": network_density,
            "average_perspective_correlation": avg_perspective_correlation,
            "alignment_score": float(network_density * avg_perspective_correlation),
            "interpretation": "Higher alignment suggests consistent perspective patterns",
        }

    # Enhance MMO analysis with transformer attention
    if "timeline_insights" in transformer_analysis:
        mmo_distribution = transformer_analysis["timeline_insights"].get(
            "mmo_attention_distribution", {}
        )
        insights["mmo_transformer_enhancement"] = {
            "attention_weighted_mmo": mmo_distribution,
            "primary_focus": (
                max(mmo_distribution.items(), key=lambda x: x[1])
                if mmo_distribution
                else None
            ),
            "mmo_balance_score": calculate_mmo_balance(mmo_distribution),
            "recommendation": generate_mmo_recommendation(mmo_distribution),
        }

    # Validate deception patterns with attention analysis
    if "deception_patterns" in hypergnn_analysis:
        deception_patterns = hypergnn_analysis["deception_patterns"]
        insights["deception_pattern_validation"] = {
            "hypergnn_patterns_detected": len(deception_patterns),
            "transformer_validation": validate_patterns_with_attention(
                deception_patterns, transformer_analysis
            ),
            "confidence_enhancement": calculate_confidence_enhancement(
                deception_patterns, transformer_analysis
            ),
        }

    # Agent perspective analysis
    transformer_export = transformer_schema.export_transformer_analysis()
    if "attention_heads" in transformer_export:
        for head_id, head_info in transformer_export["attention_heads"].items():
            agent_id = head_info["agent_id"]
            perspective = head_info["agent_perspective"]

            insights["perspective_agent_correlation"][agent_id] = {
                "perspective_type": perspective,
                "focus_token_types": head_info["focus_token_types"],
                "relationship_influence": head_info["relationship_bias_count"],
                "attention_effectiveness": calculate_attention_effectiveness(
                    head_id, transformer_analysis
                ),
            }

    return insights


def calculate_mmo_balance(mmo_distribution: Dict[str, float]) -> float:
    """Calculate balance score for motive, means, opportunity distribution"""
    if not mmo_distribution:
        return 0.0

    values = list(mmo_distribution.values())
    if len(values) < 2:
        return 0.0

    # Calculate coefficient of variation (lower = more balanced)
    mean_val = np.mean(values)
    std_val = np.std(values)

    if mean_val == 0:
        return 0.0

    cv = std_val / mean_val
    balance_score = max(0.0, 1.0 - cv)  # Invert so higher = more balanced

    return float(balance_score)


def generate_mmo_recommendation(mmo_distribution: Dict[str, float]) -> str:
    """Generate recommendation based on MMO attention distribution"""
    if not mmo_distribution:
        return "Insufficient data for MMO analysis"

    primary_focus = max(mmo_distribution.items(), key=lambda x: x[1])

    recommendations = {
        "motive_relevance": "Focus investigation on financial motivations and incentive structures",
        "means_relevance": "Examine capabilities and access patterns for opportunity exploitation",
        "opportunity_relevance": "Analyze timing and situational factors that enabled actions",
    }

    return recommendations.get(
        primary_focus[0], "Balanced investigation approach recommended"
    )


def validate_patterns_with_attention(
    deception_patterns: List[Dict], transformer_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """Validate HyperGNN deception patterns using transformer attention"""
    if not deception_patterns:
        return {"status": "no_patterns_to_validate"}

    validation_results = {
        "patterns_with_attention_support": 0,
        "attention_confidence_boost": 0.0,
        "validated_patterns": [],
    }

    # Simple validation based on attention focus
    if "self_attention_analysis" in transformer_analysis:
        attention_analyses = transformer_analysis["self_attention_analysis"]

        for pattern in deception_patterns:
            # Check if pattern agents have high attention entropy (indicating complex patterns)
            pattern_agent = pattern.get("agent", "")

            for head_id, attention_data in attention_analyses.items():
                if pattern_agent in head_id:
                    entropy = attention_data.get("attention_entropy", 0)
                    if entropy > 3.0:  # High entropy threshold
                        validation_results["patterns_with_attention_support"] += 1
                        validation_results["validated_patterns"].append(
                            {
                                "pattern": pattern.get("pattern_type", "unknown"),
                                "attention_entropy": entropy,
                                "validation_strength": (
                                    "high" if entropy > 3.5 else "moderate"
                                ),
                            }
                        )

    total_patterns = len(deception_patterns)
    if total_patterns > 0:
        validation_results["attention_confidence_boost"] = (
            validation_results["patterns_with_attention_support"] / total_patterns
        )

    return validation_results


def calculate_confidence_enhancement(
    deception_patterns: List[Dict], transformer_analysis: Dict[str, Any]
) -> float:
    """Calculate confidence enhancement from transformer analysis"""
    if not deception_patterns or "perspective_insights" in transformer_analysis:
        return 0.0

    # Higher perspective correlations suggest more consistent evidence
    correlations = list(transformer_analysis.get("perspective_insights", {}).values())

    if correlations:
        avg_correlation = np.mean(correlations)
        # Convert correlation to confidence enhancement
        return float(min(avg_correlation * 2.0, 1.0))  # Cap at 100% enhancement

    return 0.0


def calculate_attention_effectiveness(
    head_id: str, transformer_analysis: Dict[str, Any]
) -> Dict[str, float]:
    """Calculate effectiveness metrics for an attention head"""
    effectiveness = {
        "attention_focus": 0.0,
        "temporal_consistency": 0.0,
        "cross_perspective_engagement": 0.0,
    }

    # Self-attention effectiveness
    if "self_attention_analysis" in transformer_analysis:
        head_analysis = transformer_analysis["self_attention_analysis"].get(head_id, {})

        # Focus effectiveness (lower entropy = more focused)
        entropy = head_analysis.get("attention_entropy", 0)
        effectiveness["attention_focus"] = max(
            0.0, 1.0 - (entropy / 5.0)
        )  # Normalize entropy

        # Temporal consistency
        temporal_pattern = head_analysis.get("temporal_attention_pattern", {})
        consistency = temporal_pattern.get("temporal_consistency", 1.0)
        effectiveness["temporal_consistency"] = max(0.0, 1.0 - consistency)

    # Cross-perspective engagement
    cross_attention_count = 0
    total_correlation = 0.0

    if "cross_attention_analysis" in transformer_analysis:
        for key, analysis in transformer_analysis["cross_attention_analysis"].items():
            if head_id in key:
                cross_attention_count += 1
                total_correlation += analysis.get("perspective_correlation", 0.0)

    if cross_attention_count > 0:
        effectiveness["cross_perspective_engagement"] = (
            total_correlation / cross_attention_count
        )

    return effectiveness


def main():
    """Main demonstration function"""

    # Create comprehensive case example
    framework, transformer_schema = create_comprehensive_case_example()

    # Run integrated analysis
    analysis = demonstrate_attention_analysis(framework, transformer_schema)

    # Export results
    print("\n=== INTEGRATED ANALYSIS RESULTS ===")
    print(json.dumps(analysis, indent=2, default=str))

    # Generate summary report
    print("\n=== SUMMARY INSIGHTS ===")
    integrated_insights = analysis.get("integrated_insights", {})

    if "attention_network_alignment" in integrated_insights:
        alignment = integrated_insights["attention_network_alignment"]
        print(
            f"Network-Attention Alignment Score: {alignment.get('alignment_score', 0):.3f}"
        )
        print(
            f"Interpretation: {alignment.get('interpretation', 'No interpretation available')}"
        )

    if "mmo_transformer_enhancement" in integrated_insights:
        mmo = integrated_insights["mmo_transformer_enhancement"]
        primary_focus = mmo.get("primary_focus")
        if primary_focus:
            print(
                f"Primary MMO Focus: {primary_focus[0]} (strength: {primary_focus[1]:.3f})"
            )
        print(
            f"Recommendation: {mmo.get('recommendation', 'No recommendation available')}"
        )

    print("\n=== DEMONSTRATION COMPLETE ===")
    return analysis


if __name__ == "__main__":
    main()
