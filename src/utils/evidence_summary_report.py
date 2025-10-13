#!/usr/bin/env python3
"""
Evidence Summary Report Generator
=================================

Generates a comprehensive report of evidence submitted and required
for timeline events in the discrete event model.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def generate_evidence_summary_report():
    """Generate comprehensive evidence summary report"""

    # Load the discrete event model
    model_file = "/tmp/discrete_event_model_case_2025_137857.json"
    evidence_report_file = "/tmp/evidence_requirements_report_case_2025_137857.json"
    tensor_file = "/tmp/knowledge_tensors_data_case_2025_137857.json"

    if not Path(model_file).exists():
        print(
            "Error: Discrete event model not found. Please run discrete_event_model_simplified.py first."
        )
        return

    with open(model_file, "r") as f:
        model_data = json.load(f)

    with open(evidence_report_file, "r") as f:
        evidence_report = json.load(f)

    with open(tensor_file, "r") as f:
        tensor_data = json.load(f)

    # Create comprehensive report
    report_lines = [
        "# DISCRETE EVENT-DRIVEN MODEL & EVIDENCE SUMMARY",
        f"## Case: {model_data['case_id']}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## EXECUTIVE SUMMARY",
        "",
        f"- **Total Events Analyzed:** {model_data['model_summary']['total_events']}",
        f"- **Total Agents Identified:** {model_data['model_summary']['total_agents']}",
        f"- **Knowledge Tensors Generated:** {model_data['model_summary']['knowledge_tensors']}",
        f"- **Evidence Requirements:** {model_data['model_summary']['evidence_requirements']}",
        f"- **Evidence Completion:** {evidence_report['summary']['completion_percentage']}%",
        f"- **Critical Missing Evidence:** {len(evidence_report['critical_missing'])} items",
        "",
        "---",
        "",
        "## DISCRETE EVENT MODEL",
        "",
        "### Event Timeline with State Transitions",
        "",
    ]

    # Sort events by timestamp
    events = model_data["events"]
    sorted_events = sorted(events.items(), key=lambda x: x[1]["timestamp"])

    for event_id, event in sorted_events:
        report_lines.extend(
            [
                f"#### {event['timestamp'][:10]} - {event_id}",
                f"**Type:** {event['event_type']} | **State:** {event['state']}",
                f"**Actors:** {', '.join(event['actors'])}",
                "",
            ]
        )

        if event["preconditions"]:
            report_lines.extend(
                [
                    "**Preconditions:**",
                    *[f"- {pc}" for pc in event["preconditions"]],
                    "",
                ]
            )

        if event["postconditions"]:
            report_lines.extend(
                [
                    "**Postconditions:**",
                    *[f"- {pc}" for pc in event["postconditions"]],
                    "",
                ]
            )

        # Impact scores
        if event["impact_scores"]:
            report_lines.append("**Impact Scores:**")
            for impact_type, score in sorted(
                event["impact_scores"].items(), key=lambda x: x[1], reverse=True
            ):
                if score > 0:
                    report_lines.append(f"- {impact_type}: {score:.2f}")
            report_lines.append("")

    report_lines.extend(
        ["---", "", "## KNOWLEDGE TENSORS", "", "### Generated Tensor Structures", ""]
    )

    for tensor_id, tensor in tensor_data.items():
        report_lines.extend(
            [
                f"#### {tensor_id}",
                f"**Dimensions:** {tensor['dimensions']}",
                f"**Generated:** {tensor['timestamp']}",
                "",
            ]
        )

        if "feature_names" in tensor:
            for dim, features in tensor["feature_names"].items():
                if features:
                    report_lines.extend(
                        [
                            f"**{dim} features:**",
                            *[f"- {f}" for f in features[:10]],  # Show first 10
                            (
                                ""
                                if len(features) <= 10
                                else f"... and {len(features) - 10} more"
                            ),
                            "",
                        ]
                    )

    report_lines.extend(
        [
            "---",
            "",
            "## AGENT-BASED MODEL INTEGRATION",
            "",
            "### Agent Profiles and Relationships",
            "",
        ]
    )

    # Filter agents with roles
    agents_with_roles = {
        agent_id: state
        for agent_id, state in model_data["agent_states"].items()
        if state.get("roles")
    }

    for agent_id, state in sorted(agents_with_roles.items()):
        report_lines.extend(
            [
                f"#### Agent: {agent_id}",
                f"**Roles:** {', '.join(state['roles'])}",
                f"**Events Participated:** {len(state['events_participated'])}",
                "",
            ]
        )

        # Show significant relationships
        if state.get("relationships"):
            report_lines.append("**Key Relationships:**")
            for other_agent, rel in sorted(
                state["relationships"].items(),
                key=lambda x: x[1]["interaction_count"],
                reverse=True,
            )[:3]:
                report_lines.append(
                    f"- {other_agent}: {rel['interaction_count']} interactions "
                    f"({', '.join(rel['event_types'])})"
                )
            report_lines.append("")

        # Show impact profile
        impact_profile = sorted(
            state["impact_scores"].items(), key=lambda x: x[1], reverse=True
        )
        significant_impacts = [(k, v) for k, v in impact_profile if v > 0]
        if significant_impacts:
            report_lines.append("**Impact Profile:**")
            for impact_type, score in significant_impacts[:3]:
                report_lines.append(f"- {impact_type}: {score:.2f}")
            report_lines.append("")

    report_lines.extend(
        [
            "---",
            "",
            "## EVIDENCE REQUIREMENTS AND STATUS",
            "",
            "### Summary Statistics",
            "",
            f"- **Total Evidence Required:** {evidence_report['summary']['total_evidence_required']}",
            f"- **Evidence Submitted:** {evidence_report['summary']['total_evidence_submitted']}",
            f"- **Evidence Gap:** {evidence_report['summary']['evidence_gap']}",
            f"- **Completion Rate:** {evidence_report['summary']['completion_percentage']}%",
            "",
            "### Evidence by Event",
            "",
        ]
    )

    # Detailed evidence by event
    for event_id in [e[0] for e in sorted_events]:
        if event_id in evidence_report["by_event"]:
            event_evidence = evidence_report["by_event"][event_id]
            event_info = events[event_id]

            report_lines.extend(
                [
                    f"#### {event_info['timestamp'][:10]} - {event_id}",
                    f"**Event Type:** {event_evidence['event_type']}",
                    f"**Actors:** {', '.join(event_evidence['actors'])}",
                    "",
                ]
            )

            # Evidence submitted
            if event_evidence["evidence_submitted"]:
                report_lines.extend(
                    [
                        "**Evidence Submitted:**",
                        *[f"- ✅ {e}" for e in event_evidence["evidence_submitted"]],
                        "",
                    ]
                )

            # Evidence required but not submitted
            missing_evidence = set(event_evidence["evidence_required"]) - set(
                event_evidence["evidence_submitted"]
            )
            if missing_evidence:
                report_lines.extend(
                    [
                        "**Evidence Required (Not Submitted):**",
                        *[f"- ❌ {e}" for e in missing_evidence],
                        "",
                    ]
                )

            # Detailed requirements
            if event_evidence["requirements_detail"]:
                report_lines.append("**Detailed Requirements:**")
                for req in event_evidence["requirements_detail"]:
                    status_icon = "✅" if req["status"] == "submitted" else "❌"
                    priority_color = (
                        "🔴"
                        if req["priority"] == "critical"
                        else "🟡" if req["priority"] == "high" else "🟢"
                    )

                    report_lines.extend(
                        [
                            f"- {status_icon} **{req['type']}** {priority_color} {req['priority']}",
                            f"  - {req['description']}",
                        ]
                    )

                    if req["legal_reference"]:
                        report_lines.append(
                            f"  - Legal Reference: {req['legal_reference']}"
                        )
                    if req["deadline"]:
                        report_lines.append(f"  - Deadline: {req['deadline'][:10]}")

                report_lines.append("")

    report_lines.extend(
        [
            "---",
            "",
            "## CRITICAL MISSING EVIDENCE",
            "",
            "### Immediate Action Required",
            "",
        ]
    )

    if evidence_report["critical_missing"]:
        for missing in evidence_report["critical_missing"]:
            report_lines.extend(
                [
                    f"#### 🚨 {missing['evidence_type']}",
                    f"**Event:** {missing['event_id']} ({missing['event_date'][:10]})",
                    f"**Description:** {missing['description']}",
                    f"**Deadline:** {missing['deadline']}",
                ]
            )
            if missing.get("legal_reference"):
                report_lines.append(
                    f"**Legal Reference:** {missing['legal_reference']}"
                )
            report_lines.append("")
    else:
        report_lines.append("No critical evidence missing.")

    report_lines.extend(
        [
            "---",
            "",
            "## EVIDENCE TIMELINE",
            "",
            "### Chronological Evidence Requirements",
            "",
        ]
    )

    # Group evidence by date
    timeline_by_date = {}
    for item in evidence_report["evidence_timeline"]:
        date = item["date"][:10]
        if date not in timeline_by_date:
            timeline_by_date[date] = []
        timeline_by_date[date].append(item)

    for date in sorted(timeline_by_date.keys()):
        report_lines.append(f"#### {date}")
        for item in timeline_by_date[date]:
            status_icon = "✅" if item["status"] == "submitted" else "❌"
            priority_color = (
                "🔴"
                if item["priority"] == "critical"
                else "🟡" if item["priority"] == "high" else "🟢"
            )
            report_lines.append(
                f"- {status_icon} {item['evidence_type']} ({item['event_id']}) "
                f"{priority_color} {item['priority']}"
            )
        report_lines.append("")

    report_lines.extend(
        ["---", "", "## RECOMMENDATIONS", "", "### Immediate Actions Required", ""]
    )

    # Generate recommendations based on analysis
    recommendations = []

    # Critical evidence recommendations
    if evidence_report["critical_missing"]:
        recommendations.append(
            f"1. **Obtain Critical Evidence:** {len(evidence_report['critical_missing'])} "
            f"critical evidence items are missing and require immediate attention."
        )

    # Evidence gap recommendations
    if evidence_report["summary"]["evidence_gap"] > 5:
        recommendations.append(
            f"2. **Close Evidence Gap:** With only {evidence_report['summary']['completion_percentage']}% "
            f"evidence completion, additional investigation is required."
        )

    # Verification recommendations
    unverified_events = [
        e
        for e in events.values()
        if e["knowledge_attributes"].get("verification_level") == "alleged"
    ]
    if unverified_events:
        recommendations.append(
            f"3. **Verify Alleged Events:** {len(unverified_events)} events remain unverified "
            f"and require corroboration."
        )

    # Agent investigation recommendations
    high_impact_agents = [
        agent_id
        for agent_id, state in model_data["agent_states"].items()
        if sum(state["impact_scores"].values()) > 3.0
    ]
    if high_impact_agents:
        recommendations.append(
            f"4. **Focus Investigation:** {len(high_impact_agents)} agents show high impact "
            f"scores and warrant detailed investigation."
        )

    report_lines.extend(recommendations)

    report_lines.extend(
        [
            "",
            "---",
            "",
            "## CONCLUSION",
            "",
            "This discrete event-driven model analysis has identified key patterns, "
            "relationships, and evidence gaps in the case timeline. The knowledge tensors "
            "provide multi-dimensional analysis capabilities, while the agent-based model "
            "integration reveals complex relationships and behavioral patterns.",
            "",
            f"**Next Steps:** Focus on obtaining the {len(evidence_report['critical_missing'])} "
            f"critical missing evidence items and closing the {evidence_report['summary']['evidence_gap']} "
            f"item evidence gap to achieve comprehensive case coverage.",
            "",
            "---",
            "",
            f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        ]
    )

    # Save report
    report_content = "\n".join(report_lines)
    report_file = "/tmp/discrete_event_evidence_summary.md"
    with open(report_file, "w") as f:
        f.write(report_content)

    print(f"✅ Evidence summary report saved to: {report_file}")

    # Also save a JSON version for programmatic access
    json_summary = {
        "case_id": model_data["case_id"],
        "generated_at": datetime.now().isoformat(),
        "model_summary": model_data["model_summary"],
        "evidence_summary": evidence_report["summary"],
        "critical_missing": evidence_report["critical_missing"],
        "verification_status": evidence_report["verification_status"],
        "high_impact_agents": high_impact_agents,
        "unverified_events": [e["event_id"] for e in unverified_events],
        "recommendations": recommendations,
    }

    json_file = "/tmp/discrete_event_evidence_summary.json"
    with open(json_file, "w") as f:
        json.dump(json_summary, f, indent=2)

    print(f"✅ JSON summary saved to: {json_file}")

    return report_content


if __name__ == "__main__":
    print("=== GENERATING EVIDENCE SUMMARY REPORT ===")
    report = generate_evidence_summary_report()
    print("\n✅ Evidence summary report generation complete!")
