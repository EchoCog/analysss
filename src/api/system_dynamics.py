"""
System Dynamics Model for Flow Tracking
======================================

Tracks stocks and flows of various transaction types including:
- Financial transactions
- Material resource flows
- Leverage and influence patterns
- Deception tracking
- Motive, means, opportunity analysis
- Speculative risk assessment based on documented actions

Focus: Professional investigative analysis with objective assessment.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np


class StockType(Enum):
    """Types of stocks in the system"""

    FINANCIAL = "financial"
    MATERIAL = "material"
    INFORMATION = "information"
    INFLUENCE = "influence"
    LEVERAGE = "leverage"
    REPUTATION = "reputation"
    ACCESS = "access"
    TRUST = "trust"


class FlowType(Enum):
    """Types of flows between stocks"""

    TRANSFER = "transfer"
    EXCHANGE = "exchange"
    CONVERSION = "conversion"
    ACCUMULATION = "accumulation"
    DEPLETION = "depletion"
    LEVERAGE_APPLICATION = "leverage_application"
    INFLUENCE_EXERCISE = "influence_exercise"
    DECEPTION_DEPLOYMENT = "deception_deployment"


class RiskLevel(Enum):
    """Risk assessment levels"""

    NEGLIGIBLE = "negligible"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Stock:
    """Represents a stock (accumulation) in the system"""

    stock_id: str
    stock_type: StockType
    owner: str
    current_level: float
    unit: str
    description: str
    last_updated: datetime
    historical_levels: List[Tuple[datetime, float]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Flow:
    """Represents a flow between stocks"""

    flow_id: str
    flow_type: FlowType
    source_stock: str
    target_stock: str
    rate: float
    timestamp: datetime
    description: str
    evidence_refs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MotiveMeansOpportunity:
    """Analysis of motive, means, and opportunity"""

    entity: str
    event: str
    motive_indicators: List[str] = field(default_factory=list)
    means_available: List[str] = field(default_factory=list)
    opportunity_factors: List[str] = field(default_factory=list)
    timeline_correlation: Optional[str] = None
    risk_assessment: RiskLevel = RiskLevel.MODERATE
    supporting_evidence: List[str] = field(default_factory=list)
    analysis_date: datetime = field(default_factory=datetime.now)


@dataclass
class DeceptionPattern:
    """Tracks deception patterns and mechanisms"""

    pattern_id: str
    description: str
    actors: List[str]
    mechanism: str
    detection_method: str
    timeline: List[Tuple[datetime, str]] = field(default_factory=list)
    impact_assessment: str = "pending_analysis"
    countermeasures: List[str] = field(default_factory=list)
    confidence_level: float = 0.5
    evidence_refs: List[str] = field(default_factory=list)


class SystemDynamicsModel:
    """
    System Dynamics Model for comprehensive flow tracking

    Provides professional analysis of resource flows, influence patterns,
    and risk assessments for investigative purposes.
    """

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.system_id = case_id  # Backward compatibility
        self.stocks: Dict[str, Stock] = {}
        self.flows: Dict[str, Flow] = {}
        self.mmo_analyses: Dict[str, MotiveMeansOpportunity] = {}
        self.deception_patterns: Dict[str, DeceptionPattern] = {}
        self.relationships: Dict[str, Dict[str, float]] = {}

    def add_stock(self, stock: Stock) -> None:
        """Add a stock to the system"""
        self.stocks[stock.stock_id] = stock

        # Initialize relationship tracking for this stock's owner
        if stock.owner not in self.relationships:
            self.relationships[stock.owner] = {}

    def add_flow(self, flow: Flow) -> None:
        """Add a flow to the system"""
        self.flows[flow.flow_id] = flow

        # Update stock levels if both stocks exist
        if flow.source_stock in self.stocks and flow.target_stock in self.stocks:
            self._update_stock_levels(flow)

    def _update_stock_levels(self, flow: Flow) -> None:
        """Update stock levels based on flow"""
        source_stock = self.stocks[flow.source_stock]
        target_stock = self.stocks[flow.target_stock]

        # Record historical levels
        source_stock.historical_levels.append(
            (flow.timestamp, source_stock.current_level)
        )
        target_stock.historical_levels.append(
            (flow.timestamp, target_stock.current_level)
        )

        # Update current levels
        if flow.flow_type == FlowType.TRANSFER:
            source_stock.current_level -= flow.rate
            target_stock.current_level += flow.rate
        elif flow.flow_type == FlowType.EXCHANGE:
            # Exchange flows may have different rates
            rate_ratio = flow.metadata.get("exchange_rate", 1.0)
            source_stock.current_level -= flow.rate
            target_stock.current_level += flow.rate * rate_ratio

        # Update timestamps
        source_stock.last_updated = flow.timestamp
        target_stock.last_updated = flow.timestamp

    def analyze_motive_means_opportunity(
        self, entity: str, event: str, context: Dict[str, Any] = None
    ) -> MotiveMeansOpportunity:
        """
        Conduct professional MMO analysis for an entity regarding a specific event
        """
        if context is None:
            context = {}

        mmo = MotiveMeansOpportunity(entity=entity, event=event)

        # Analyze motives based on stock positions and flows
        entity_stocks = [s for s in self.stocks.values() if s.owner == entity]

        # Financial pressure indicators
        financial_stocks = [
            s for s in entity_stocks if s.stock_type == StockType.FINANCIAL
        ]
        if financial_stocks:
            avg_financial = sum(s.current_level for s in financial_stocks) / len(
                financial_stocks
            )
            if avg_financial < 0:
                mmo.motive_indicators.append("financial_pressure_indicated")

        # Leverage position analysis
        leverage_stocks = [
            s for s in entity_stocks if s.stock_type == StockType.LEVERAGE
        ]
        if leverage_stocks:
            total_leverage = sum(s.current_level for s in leverage_stocks)
            if total_leverage > 1.0:
                mmo.motive_indicators.append("high_leverage_position")

        # Means analysis - access and influence
        access_stocks = [s for s in entity_stocks if s.stock_type == StockType.ACCESS]
        influence_stocks = [
            s for s in entity_stocks if s.stock_type == StockType.INFLUENCE
        ]

        if access_stocks:
            mmo.means_available.append("documented_access_capabilities")
        if influence_stocks:
            mmo.means_available.append("influence_network_available")

        # Opportunity analysis - timing and relationships
        recent_flows = [
            f
            for f in self.flows.values()
            if (
                f.source_stock in [s.stock_id for s in entity_stocks]
                or f.target_stock in [s.stock_id for s in entity_stocks]
            )
            and f.timestamp > datetime.now() - timedelta(days=30)
        ]

        if recent_flows:
            mmo.opportunity_factors.append("recent_transaction_activity")

        # Risk assessment based on analysis
        risk_factors = (
            len(mmo.motive_indicators)
            + len(mmo.means_available)
            + len(mmo.opportunity_factors)
        )

        if risk_factors >= 6:
            mmo.risk_assessment = RiskLevel.HIGH
        elif risk_factors >= 4:
            mmo.risk_assessment = RiskLevel.MODERATE
        elif risk_factors >= 2:
            mmo.risk_assessment = RiskLevel.LOW
        else:
            mmo.risk_assessment = RiskLevel.NEGLIGIBLE

        analysis_id = f"{entity}_{event}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.mmo_analyses[analysis_id] = mmo

        return mmo

    def track_deception_pattern(
        self,
        pattern_id: str,
        description: str,
        actors: List[str],
        mechanism: str,
        detection_method: str,
    ) -> DeceptionPattern:
        """
        Track and analyze deception patterns
        Returns objective analysis without emotional assessment
        """
        pattern = DeceptionPattern(
            pattern_id=pattern_id,
            description=description,
            actors=actors,
            mechanism=mechanism,
            detection_method=detection_method,
            timeline=[],
        )

        # Analyze pattern based on system flows
        actor_flows = []
        for actor in actors:
            actor_stocks = [
                s.stock_id for s in self.stocks.values() if s.owner == actor
            ]
            flows = [
                f
                for f in self.flows.values()
                if f.source_stock in actor_stocks or f.target_stock in actor_stocks
            ]
            actor_flows.extend(flows)

        # Timeline construction
        for flow in sorted(actor_flows, key=lambda x: x.timestamp):
            pattern.timeline.append((flow.timestamp, flow.description))

        # Impact assessment
        information_flows = [
            f
            for f in actor_flows
            if any(
                self.stocks[f.source_stock].stock_type == StockType.INFORMATION
                or self.stocks[f.target_stock].stock_type == StockType.INFORMATION
                for stock_id in [f.source_stock, f.target_stock]
                if stock_id in self.stocks
            )
        ]

        if len(information_flows) > 5:
            pattern.impact_assessment = "high_volume_information_manipulation_detected"
        elif len(information_flows) > 2:
            pattern.impact_assessment = "moderate_information_control_patterns"
        else:
            pattern.impact_assessment = "limited_information_flow_anomalies"

        # Confidence assessment
        evidence_quality = len([f for f in actor_flows if f.evidence_refs])
        total_flows = len(actor_flows)

        if total_flows > 0:
            pattern.confidence_level = min(evidence_quality / total_flows, 1.0)

        self.deception_patterns[pattern_id] = pattern
        return pattern

    def calculate_influence_network(self) -> Dict[str, Dict[str, float]]:
        """Calculate influence network based on flows"""
        influence_network = {}

        # Analyze influence flows
        influence_flows = [
            f for f in self.flows.values() if f.flow_type == FlowType.INFLUENCE_EXERCISE
        ]

        for flow in influence_flows:
            source_owner = None
            target_owner = None

            if flow.source_stock in self.stocks:
                source_owner = self.stocks[flow.source_stock].owner
            if flow.target_stock in self.stocks:
                target_owner = self.stocks[flow.target_stock].owner

            if source_owner and target_owner:
                if source_owner not in influence_network:
                    influence_network[source_owner] = {}

                if target_owner not in influence_network[source_owner]:
                    influence_network[source_owner][target_owner] = 0.0

                influence_network[source_owner][target_owner] += flow.rate

        return influence_network

    def assess_systemic_risk(self) -> Dict[str, Any]:
        """
        Assess systemic risk based on flow patterns and concentrations
        Returns professional risk assessment
        """
        risk_assessment = {
            "overall_risk_level": RiskLevel.LOW.value,
            "concentration_risks": [],
            "flow_anomalies": [],
            "deception_indicators": [],
            "recommendations": [],
        }

        # Concentration risk analysis
        owners = set(stock.owner for stock in self.stocks.values())
        for owner in owners:
            owner_stocks = [s for s in self.stocks.values() if s.owner == owner]
            total_value = sum(
                s.current_level
                for s in owner_stocks
                if s.stock_type in [StockType.FINANCIAL, StockType.MATERIAL]
            )

            if total_value > 1000000:  # Example threshold
                risk_assessment["concentration_risks"].append(
                    {
                        "entity": owner,
                        "concentration_value": total_value,
                        "risk_type": "high_asset_concentration",
                    }
                )

        # Flow anomaly detection
        recent_flows = [
            f
            for f in self.flows.values()
            if f.timestamp > datetime.now() - timedelta(days=7)
        ]

        if len(recent_flows) > 50:  # Example threshold
            risk_assessment["flow_anomalies"].append(
                {
                    "pattern": "high_frequency_transactions",
                    "count": len(recent_flows),
                    "timeframe": "7_days",
                }
            )

        # Deception pattern assessment
        high_confidence_patterns = [
            p for p in self.deception_patterns.values() if p.confidence_level > 0.7
        ]

        if high_confidence_patterns:
            risk_assessment["deception_indicators"] = [
                {
                    "pattern_id": p.pattern_id,
                    "confidence": p.confidence_level,
                    "impact": p.impact_assessment,
                }
                for p in high_confidence_patterns
            ]

        # Overall risk determination
        risk_factors = (
            len(risk_assessment["concentration_risks"])
            + len(risk_assessment["flow_anomalies"])
            + len(high_confidence_patterns)
        )

        if risk_factors >= 5:
            risk_assessment["overall_risk_level"] = RiskLevel.HIGH.value
        elif risk_factors >= 3:
            risk_assessment["overall_risk_level"] = RiskLevel.MODERATE.value

        # Professional recommendations
        if risk_assessment["concentration_risks"]:
            risk_assessment["recommendations"].append(
                "Review high-concentration entities for regulatory compliance"
            )

        if risk_assessment["flow_anomalies"]:
            risk_assessment["recommendations"].append(
                "Implement enhanced transaction monitoring protocols"
            )

        if high_confidence_patterns:
            risk_assessment["recommendations"].append(
                "Conduct detailed investigation of identified deception patterns"
            )

        return risk_assessment

    def export_professional_analysis(self) -> Dict[str, Any]:
        """Export comprehensive professional analysis"""
        return {
            "system_id": self.system_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "stock_summary": {
                "total_stocks": len(self.stocks),
                "stocks_by_type": {
                    t.value: len([s for s in self.stocks.values() if s.stock_type == t])
                    for t in StockType
                },
                "stock_owners": list(set(s.owner for s in self.stocks.values())),
            },
            "flow_analysis": {
                "total_flows": len(self.flows),
                "flows_by_type": {
                    t.value: len([f for f in self.flows.values() if f.flow_type == t])
                    for t in FlowType
                },
                "recent_activity": len(
                    [
                        f
                        for f in self.flows.values()
                        if f.timestamp > datetime.now() - timedelta(days=30)
                    ]
                ),
            },
            "mmo_analyses": {
                "total_analyses": len(self.mmo_analyses),
                "risk_distribution": {
                    r.value: len(
                        [
                            a
                            for a in self.mmo_analyses.values()
                            if a.risk_assessment == r
                        ]
                    )
                    for r in RiskLevel
                },
            },
            "deception_patterns": {
                "total_patterns": len(self.deception_patterns),
                "high_confidence_patterns": len(
                    [
                        p
                        for p in self.deception_patterns.values()
                        if p.confidence_level > 0.7
                    ]
                ),
            },
            "systemic_risk_assessment": self.assess_systemic_risk(),
        }

    def simulate_flow_dynamics(
        self, simulation_days: int = 30, time_step_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Simulate dynamic flow evolution over time with feedback loops
        """
        simulation_results = {
            "simulation_id": f"flow_sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "duration_days": simulation_days,
            "time_step_hours": time_step_hours,
            "stock_evolution": {},
            "flow_patterns": [],
            "system_states": [],
            "emergent_behaviors": [],
        }

        # Initialize stock evolution tracking
        for stock_id, stock in self.stocks.items():
            simulation_results["stock_evolution"][stock_id] = {
                "initial_level": stock.current_level,
                "timeline": [
                    {"time": 0, "level": stock.current_level, "change_rate": 0.0}
                ],
            }

        # Run simulation over time steps
        total_steps = (simulation_days * 24) // time_step_hours
        current_stocks = {sid: s.current_level for sid, s in self.stocks.items()}

        for step in range(1, total_steps + 1):
            simulation_time = step * time_step_hours / 24.0  # Convert to days

            # Calculate flow effects for this time step
            step_changes = {}
            active_flows = []

            for flow_id, flow in self.flows.items():
                # Check if flow is active during this period
                flow_age_days = (
                    datetime.now() - flow.timestamp
                ).total_seconds() / 86400
                flow_decay = max(
                    0.1, 1.0 - (flow_age_days / 100)
                )  # Flows decay over time

                if flow_decay > 0.1:  # Flow is still active
                    effective_magnitude = flow.rate * flow_decay

                    # Apply flow effects
                    if flow.source_stock in current_stocks:
                        if flow.source_stock not in step_changes:
                            step_changes[flow.source_stock] = 0
                        step_changes[flow.source_stock] -= effective_magnitude * (
                            time_step_hours / 24
                        )

                    if flow.target_stock in current_stocks:
                        if flow.target_stock not in step_changes:
                            step_changes[flow.target_stock] = 0
                        step_changes[flow.target_stock] += effective_magnitude * (
                            time_step_hours / 24
                        )

                    active_flows.append(
                        {
                            "flow_id": flow_id,
                            "effective_magnitude": effective_magnitude,
                            "decay_factor": flow_decay,
                        }
                    )

            # Apply feedback loops and system effects
            feedback_effects = self._calculate_feedback_effects(
                current_stocks, step_changes
            )
            for stock_id, feedback in feedback_effects.items():
                if stock_id not in step_changes:
                    step_changes[stock_id] = 0
                step_changes[stock_id] += feedback

            # Update stock levels
            for stock_id, change in step_changes.items():
                current_stocks[stock_id] = max(0, current_stocks[stock_id] + change)

                # Record timeline point
                change_rate = change / max(0.01, time_step_hours / 24)
                simulation_results["stock_evolution"][stock_id]["timeline"].append(
                    {
                        "time": simulation_time,
                        "level": current_stocks[stock_id],
                        "change_rate": change_rate,
                    }
                )

            # Record system state
            if step % (24 // time_step_hours) == 0:  # Daily snapshots
                system_state = {
                    "day": int(simulation_time),
                    "total_value": sum(current_stocks.values()),
                    "active_flows": len(active_flows),
                    "system_entropy": self._calculate_system_entropy(current_stocks),
                    "stability_index": self._calculate_stability_index(step_changes),
                }
                simulation_results["system_states"].append(system_state)

        # Analyze flow patterns
        flow_patterns = self._analyze_flow_patterns(
            simulation_results["stock_evolution"]
        )
        simulation_results["flow_patterns"] = flow_patterns

        # Identify emergent behaviors
        emergent_behaviors = self._identify_emergent_behaviors(
            simulation_results["system_states"]
        )
        simulation_results["emergent_behaviors"] = emergent_behaviors

        return simulation_results

    def optimize_resource_allocation(
        self, target_stocks: Dict[str, float], optimization_horizon: int = 14
    ) -> Dict[str, Any]:
        """
        Optimize resource allocation to achieve target stock levels
        """
        optimization_results = {
            "target_stocks": target_stocks,
            "optimization_horizon_days": optimization_horizon,
            "recommended_flows": [],
            "resource_requirements": {},
            "optimization_metrics": {},
            "implementation_timeline": [],
        }

        current_levels = {
            stock_id: stock.current_level for stock_id, stock in self.stocks.items()
        }
        gaps = {}

        # Calculate gaps between current and target levels
        for stock_id, target_level in target_stocks.items():
            if stock_id in current_levels:
                gap = target_level - current_levels[stock_id]
                gaps[stock_id] = gap

        # Generate optimization strategy
        for stock_id, gap in gaps.items():
            if abs(gap) > 0.1:  # Significant gap
                stock = self.stocks[stock_id]

                if gap > 0:  # Need to increase stock
                    # Find potential sources
                    potential_sources = self._find_resource_sources(
                        stock.stock_type, gap
                    )
                    for source in potential_sources:
                        recommended_flow = {
                            "source": source["stock_id"],
                            "target": stock_id,
                            "flow_type": self._determine_optimal_flow_type(
                                source["stock_type"], stock.stock_type
                            ),
                            "magnitude": min(gap, source["available_capacity"]),
                            "priority": "high" if abs(gap) > 0.5 else "medium",
                            "implementation_cost": source["transfer_cost"],
                        }
                        optimization_results["recommended_flows"].append(
                            recommended_flow
                        )

                        # Update remaining gap
                        gap -= recommended_flow["magnitude"]
                        if gap <= 0.1:
                            break

                else:  # Need to decrease stock (redistribute)
                    # Find potential targets
                    potential_targets = self._find_resource_targets(
                        stock.stock_type, abs(gap)
                    )
                    for target in potential_targets:
                        recommended_flow = {
                            "source": stock_id,
                            "target": target["stock_id"],
                            "flow_type": self._determine_optimal_flow_type(
                                stock.stock_type, target["stock_type"]
                            ),
                            "magnitude": min(abs(gap), target["capacity_demand"]),
                            "priority": "medium",
                            "implementation_cost": target["acceptance_cost"],
                        }
                        optimization_results["recommended_flows"].append(
                            recommended_flow
                        )

                        gap += recommended_flow["magnitude"]  # gap is negative
                        if gap >= -0.1:
                            break

        # Calculate resource requirements
        resource_requirements = self._calculate_resource_requirements(
            optimization_results["recommended_flows"]
        )
        optimization_results["resource_requirements"] = resource_requirements

        # Generate implementation timeline
        timeline = self._generate_implementation_timeline(
            optimization_results["recommended_flows"], optimization_horizon
        )
        optimization_results["implementation_timeline"] = timeline

        # Calculate optimization metrics
        metrics = self._calculate_optimization_metrics(
            gaps, optimization_results["recommended_flows"]
        )
        optimization_results["optimization_metrics"] = metrics

        return optimization_results

    def analyze_vulnerability_patterns(self) -> Dict[str, Any]:
        """
        Analyze system vulnerabilities and potential exploitation patterns
        """
        vulnerability_analysis = {
            "analysis_timestamp": datetime.now().isoformat(),
            "structural_vulnerabilities": [],
            "flow_vulnerabilities": [],
            "concentration_risks": [],
            "systemic_weaknesses": [],
            "mitigation_strategies": [],
        }

        # Analyze structural vulnerabilities
        for stock_id, stock in self.stocks.items():
            # Single points of failure
            incoming_flows = [
                f for f in self.flows.values() if f.target_stock == stock_id
            ]
            outgoing_flows = [
                f for f in self.flows.values() if f.source_stock == stock_id
            ]

            if len(incoming_flows) == 1 and stock.current_level > 0.5:
                vulnerability_analysis["structural_vulnerabilities"].append(
                    {
                        "type": "single_source_dependency",
                        "stock_id": stock_id,
                        "vulnerability_score": 0.8,
                        "description": f"Stock {stock_id} depends on single source",
                        "impact_potential": "high",
                    }
                )

            if len(outgoing_flows) > 5:
                vulnerability_analysis["structural_vulnerabilities"].append(
                    {
                        "type": "over_distribution",
                        "stock_id": stock_id,
                        "vulnerability_score": 0.6,
                        "description": f"Stock {stock_id} has excessive outflow dependencies",
                        "impact_potential": "medium",
                    }
                )

        # Analyze flow vulnerabilities
        for flow_id, flow in self.flows.items():
            flow_age = (datetime.now() - flow.timestamp).total_seconds() / 86400

            # High-value flows are vulnerable to disruption
            if flow.rate > 0.7:
                vulnerability_analysis["flow_vulnerabilities"].append(
                    {
                        "type": "high_value_flow",
                        "flow_id": flow_id,
                        "vulnerability_score": min(1.0, flow.rate),
                        "description": f"High-magnitude flow susceptible to targeted disruption",
                        "potential_impact": flow.rate * 0.8,
                    }
                )

            # Aging flows may be vulnerable
            if flow_age > 60:  # Flows older than 60 days
                vulnerability_analysis["flow_vulnerabilities"].append(
                    {
                        "type": "aging_flow",
                        "flow_id": flow_id,
                        "vulnerability_score": min(1.0, flow_age / 100),
                        "description": f"Aging flow may be subject to decay or interruption",
                        "potential_impact": 0.3,
                    }
                )

        # Concentration risk analysis
        stock_concentrations = {}
        for owner in set(stock.owner for stock in self.stocks.values()):
            owner_stocks = [s for s in self.stocks.values() if s.owner == owner]
            total_value = sum(s.current_level for s in owner_stocks)
            if total_value > 1.5:  # High concentration
                stock_concentrations[owner] = {
                    "total_value": total_value,
                    "stock_count": len(owner_stocks),
                    "concentration_ratio": total_value / max(1, len(self.stocks)),
                }

        for owner, concentration in stock_concentrations.items():
            if concentration["concentration_ratio"] > 0.3:
                vulnerability_analysis["concentration_risks"].append(
                    {
                        "type": "ownership_concentration",
                        "owner": owner,
                        "risk_score": concentration["concentration_ratio"],
                        "description": f"High concentration of resources in single entity",
                        "systemic_risk": (
                            "high"
                            if concentration["concentration_ratio"] > 0.5
                            else "medium"
                        ),
                    }
                )

        # Generate mitigation strategies
        mitigation_strategies = self._generate_mitigation_strategies(
            vulnerability_analysis
        )
        vulnerability_analysis["mitigation_strategies"] = mitigation_strategies

        return vulnerability_analysis

    def _calculate_feedback_effects(
        self, current_stocks: Dict[str, float], step_changes: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate feedback effects between stocks"""
        feedback_effects = {}

        # Simple feedback model: high stocks tend to resist further increases
        for stock_id, current_level in current_stocks.items():
            if stock_id in step_changes:
                change = step_changes[stock_id]

                # Saturation effect: harder to increase already high stocks
                if current_level > 0.8 and change > 0:
                    resistance = (current_level - 0.8) * 0.5
                    feedback_effects[stock_id] = -change * resistance

                # Network effects: stocks influence connected stocks
                connected_stocks = self._find_connected_stocks(stock_id)
                for connected_id in connected_stocks:
                    if connected_id not in feedback_effects:
                        feedback_effects[connected_id] = 0
                    # Small spillover effect
                    feedback_effects[connected_id] += change * 0.1

        return feedback_effects

    def _find_connected_stocks(self, stock_id: str) -> List[str]:
        """Find stocks connected via flows"""
        connected = []
        for flow in self.flows.values():
            if flow.source_stock == stock_id and flow.target_stock not in connected:
                connected.append(flow.target_stock)
            elif flow.target_stock == stock_id and flow.source_stock not in connected:
                connected.append(flow.source_stock)
        return connected

    def _calculate_system_entropy(self, stocks: Dict[str, float]) -> float:
        """Calculate system entropy as a measure of disorder"""
        if not stocks:
            return 0.0

        total_value = sum(stocks.values())
        if total_value == 0:
            return 1.0

        # Calculate entropy based on distribution
        entropy = 0.0
        for value in stocks.values():
            if value > 0:
                probability = value / total_value
                entropy -= probability * np.log2(probability)

        # Normalize by maximum possible entropy
        max_entropy = np.log2(len(stocks))
        return entropy / max_entropy if max_entropy > 0 else 0.0

    def _calculate_stability_index(self, changes: Dict[str, float]) -> float:
        """Calculate system stability index"""
        if not changes:
            return 1.0

        change_magnitudes = [abs(change) for change in changes.values()]
        avg_change = np.mean(change_magnitudes)

        # Stability is inverse of average change
        stability = 1.0 / (1.0 + avg_change)
        return stability

    def _analyze_flow_patterns(
        self, stock_evolution: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze patterns in stock evolution"""
        patterns = []

        for stock_id, evolution in stock_evolution.items():
            timeline = evolution["timeline"]
            if len(timeline) < 5:
                continue

            # Extract levels for analysis
            levels = [point["level"] for point in timeline]
            changes = [point["change_rate"] for point in timeline]

            # Detect patterns
            # 1. Monotonic trends
            if all(l2 >= l1 for l1, l2 in zip(levels[:-1], levels[1:])):
                patterns.append(
                    {
                        "stock_id": stock_id,
                        "pattern_type": "monotonic_increase",
                        "strength": np.std(changes),
                        "duration": len(timeline),
                    }
                )
            elif all(l2 <= l1 for l1, l2 in zip(levels[:-1], levels[1:])):
                patterns.append(
                    {
                        "stock_id": stock_id,
                        "pattern_type": "monotonic_decrease",
                        "strength": np.std(changes),
                        "duration": len(timeline),
                    }
                )

            # 2. Oscillatory patterns
            zero_crossings = sum(
                1 for c1, c2 in zip(changes[:-1], changes[1:]) if c1 * c2 < 0
            )
            if zero_crossings > len(changes) * 0.3:
                patterns.append(
                    {
                        "stock_id": stock_id,
                        "pattern_type": "oscillatory",
                        "frequency": zero_crossings / len(changes),
                        "amplitude": np.std(levels),
                    }
                )

        return patterns

    def _identify_emergent_behaviors(
        self, system_states: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify emergent system behaviors"""
        behaviors = []

        if len(system_states) < 5:
            return behaviors

        # Extract time series
        total_values = [state["total_value"] for state in system_states]
        entropies = [state["system_entropy"] for state in system_states]
        stabilities = [state["stability_index"] for state in system_states]

        # System growth/contraction
        total_change = total_values[-1] - total_values[0]
        if abs(total_change) > 0.2:
            behaviors.append(
                {
                    "behavior_type": (
                        "system_growth" if total_change > 0 else "system_contraction"
                    ),
                    "magnitude": abs(total_change),
                    "trend_strength": np.corrcoef(
                        range(len(total_values)), total_values
                    )[0, 1],
                }
            )

        # System stabilization/destabilization
        stability_trend = np.corrcoef(range(len(stabilities)), stabilities)[0, 1]
        if abs(stability_trend) > 0.5:
            behaviors.append(
                {
                    "behavior_type": (
                        "stabilization" if stability_trend > 0 else "destabilization"
                    ),
                    "trend_strength": abs(stability_trend),
                    "final_stability": stabilities[-1],
                }
            )

        return behaviors

    def _find_resource_sources(
        self, target_type: StockType, required_amount: float
    ) -> List[Dict[str, Any]]:
        """Find potential sources for resource allocation"""
        sources = []

        for stock_id, stock in self.stocks.items():
            # Consider compatible stock types and excess capacity
            if (
                stock.stock_type == target_type
                and stock.current_level > required_amount
            ):
                available_capacity = stock.current_level - 0.2  # Keep minimum reserve
                sources.append(
                    {
                        "stock_id": stock_id,
                        "stock_type": stock.stock_type,
                        "available_capacity": available_capacity,
                        "transfer_cost": 0.1
                        * available_capacity,  # Cost proportional to amount
                        "compatibility": 1.0,
                    }
                )
            elif (
                stock.current_level > 0.5
            ):  # Cross-type transfers with lower efficiency
                available_capacity = (
                    stock.current_level - 0.3
                ) * 0.7  # Lower efficiency
                sources.append(
                    {
                        "stock_id": stock_id,
                        "stock_type": stock.stock_type,
                        "available_capacity": available_capacity,
                        "transfer_cost": 0.2
                        * available_capacity,  # Higher cost for conversion
                        "compatibility": 0.6,
                    }
                )

        # Sort by efficiency (capacity/cost ratio)
        sources.sort(
            key=lambda x: x["available_capacity"] / max(0.01, x["transfer_cost"]),
            reverse=True,
        )
        return sources[:5]  # Return top 5 sources

    def _find_resource_targets(
        self, source_type: StockType, excess_amount: float
    ) -> List[Dict[str, Any]]:
        """Find potential targets for resource distribution"""
        targets = []

        for stock_id, stock in self.stocks.items():
            # Consider stocks that could benefit from additional resources
            if stock.stock_type == source_type and stock.current_level < 0.8:
                capacity_demand = min(excess_amount, 1.0 - stock.current_level)
                targets.append(
                    {
                        "stock_id": stock_id,
                        "stock_type": stock.stock_type,
                        "capacity_demand": capacity_demand,
                        "acceptance_cost": 0.05
                        * capacity_demand,  # Low cost for same type
                        "compatibility": 1.0,
                    }
                )
            elif stock.current_level < 0.6:  # Cross-type distributions
                capacity_demand = min(excess_amount * 0.6, 0.8 - stock.current_level)
                targets.append(
                    {
                        "stock_id": stock_id,
                        "stock_type": stock.stock_type,
                        "capacity_demand": capacity_demand,
                        "acceptance_cost": 0.15
                        * capacity_demand,  # Higher cost for conversion
                        "compatibility": 0.5,
                    }
                )

        targets.sort(
            key=lambda x: x["capacity_demand"] / max(0.01, x["acceptance_cost"]),
            reverse=True,
        )
        return targets[:5]

    def _determine_optimal_flow_type(
        self, source_type: StockType, target_type: StockType
    ) -> FlowType:
        """Determine optimal flow type for resource transfer"""
        if source_type == target_type:
            return FlowType.TRANSFER
        elif source_type in [
            StockType.FINANCIAL,
            StockType.MATERIAL,
        ] and target_type in [StockType.FINANCIAL, StockType.MATERIAL]:
            return FlowType.EXCHANGE
        else:
            return FlowType.CONVERSION

    def _generate_implementation_timeline(
        self, flows: List[Dict[str, Any]], horizon_days: int
    ) -> List[Dict[str, Any]]:
        """Generate implementation timeline for recommended flows"""
        timeline = []

        # Sort flows by priority
        prioritized_flows = sorted(
            flows,
            key=lambda x: {"high": 3, "medium": 2, "low": 1}[x["priority"]],
            reverse=True,
        )

        days_per_batch = (
            max(1, horizon_days // len(prioritized_flows)) if prioritized_flows else 1
        )

        for i, flow in enumerate(prioritized_flows):
            implementation_day = min(i * days_per_batch, horizon_days - 1)
            timeline.append(
                {
                    "day": implementation_day,
                    "flow": flow,
                    "prerequisites": self._identify_flow_prerequisites(flow),
                    "estimated_duration_days": max(1, int(flow["magnitude"] * 3)),
                    "resource_allocation": {
                        "personnel": max(1, int(flow["magnitude"] * 2)),
                        "systems": ["transfer_system", "monitoring_system"],
                    },
                }
            )

        return timeline

    def _identify_flow_prerequisites(self, flow: Dict[str, Any]) -> List[str]:
        """Identify prerequisites for implementing a flow"""
        prerequisites = []

        if flow["magnitude"] > 0.5:
            prerequisites.append("management_approval")

        if flow.get("flow_type") == FlowType.CONVERSION.value:
            prerequisites.append("conversion_system_setup")

        if flow["implementation_cost"] > 0.3:
            prerequisites.append("budget_allocation")

        return prerequisites

    def _calculate_resource_requirements(
        self, flows: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate resource requirements for implementing flows"""
        requirements = {
            "total_cost": sum(flow["implementation_cost"] for flow in flows),
            "personnel_hours": sum(
                flow["magnitude"] * 8 for flow in flows
            ),  # 8 hours per unit
            "system_resources": [],
            "risk_mitigation": [],
        }

        # Identify required systems
        unique_flow_types = set(flow.get("flow_type", "transfer") for flow in flows)
        for flow_type in unique_flow_types:
            requirements["system_resources"].append(f"{flow_type}_system")

        # Risk mitigation for high-value flows
        high_value_flows = [f for f in flows if f["magnitude"] > 0.7]
        if high_value_flows:
            requirements["risk_mitigation"].append("enhanced_monitoring")
            requirements["risk_mitigation"].append("backup_systems")

        return requirements

    def _calculate_optimization_metrics(
        self, gaps: Dict[str, float], flows: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate optimization performance metrics"""
        metrics = {
            "gap_coverage": 0.0,
            "efficiency_score": 0.0,
            "implementation_complexity": 0.0,
            "risk_score": 0.0,
        }

        if not gaps or not flows:
            return metrics

        # Gap coverage: how much of the target gaps can be filled
        total_gap = sum(abs(gap) for gap in gaps.values())
        covered_gap = sum(flow["magnitude"] for flow in flows)
        metrics["gap_coverage"] = min(1.0, covered_gap / max(0.01, total_gap))

        # Efficiency: value delivered per cost
        total_value = sum(flow["magnitude"] for flow in flows)
        total_cost = sum(flow["implementation_cost"] for flow in flows)
        metrics["efficiency_score"] = total_value / max(0.01, total_cost)

        # Implementation complexity
        complexity_factors = len(
            set(flow.get("flow_type", "transfer") for flow in flows)
        )
        metrics["implementation_complexity"] = min(1.0, complexity_factors / 5)

        # Risk score based on flow magnitudes and types
        high_magnitude_flows = sum(1 for flow in flows if flow["magnitude"] > 0.5)
        metrics["risk_score"] = min(1.0, high_magnitude_flows / max(1, len(flows)))

        return metrics

    def _generate_mitigation_strategies(
        self, vulnerability_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate mitigation strategies for identified vulnerabilities"""
        strategies = []

        # Diversification for single-source dependencies
        structural_vulns = vulnerability_analysis.get("structural_vulnerabilities", [])
        single_source_vulns = [
            v for v in structural_vulns if v["type"] == "single_source_dependency"
        ]

        if single_source_vulns:
            strategies.append(
                {
                    "strategy_type": "source_diversification",
                    "priority": "high",
                    "description": "Establish alternative sources for critical stocks",
                    "implementation_steps": [
                        "Identify alternative sources",
                        "Establish backup supply relationships",
                        "Implement redundant flow paths",
                    ],
                    "expected_impact": "reduces dependency risk by 60-80%",
                }
            )

        # Flow protection for high-value flows
        flow_vulns = vulnerability_analysis.get("flow_vulnerabilities", [])
        high_value_flow_vulns = [
            v for v in flow_vulns if v["type"] == "high_value_flow"
        ]

        if high_value_flow_vulns:
            strategies.append(
                {
                    "strategy_type": "flow_protection",
                    "priority": "high",
                    "description": "Implement protection mechanisms for critical flows",
                    "implementation_steps": [
                        "Deploy monitoring systems",
                        "Establish backup flow mechanisms",
                        "Implement access controls",
                    ],
                    "expected_impact": "reduces flow disruption risk by 70-90%",
                }
            )

        # Deconcentration for concentration risks
        concentration_risks = vulnerability_analysis.get("concentration_risks", [])
        if concentration_risks:
            strategies.append(
                {
                    "strategy_type": "risk_deconcentration",
                    "priority": "medium",
                    "description": "Distribute concentrated resources across multiple entities",
                    "implementation_steps": [
                        "Identify redistribution opportunities",
                        "Establish distribution mechanisms",
                        "Monitor concentration metrics",
                    ],
                    "expected_impact": "reduces concentration risk by 40-60%",
                }
            )

        return strategies

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the system dynamics model."""
        return {
            "total_stocks": len(self.stocks),
            "total_flows": len(self.flows),
            "stocks_by_type": {
                t.value: len([s for s in self.stocks.values() if s.stock_type == t])
                for t in StockType
            },
            "flows_by_type": {
                t.value: len([f for f in self.flows.values() if f.flow_type == t])
                for t in FlowType
            },
        }
