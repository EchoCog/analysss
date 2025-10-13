#!/usr/bin/env python3
"""
Payment Fraud Analyzer Module

This module provides specialized analysis capabilities for detecting and analyzing
payment fraud patterns in financial data, with particular focus on false accounting
entries and payment misdirection schemes.
"""

import datetime
import json
from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class FraudEvidence:
    """Represents a piece of evidence in a payment fraud case."""

    evidence_id: str
    evidence_type: (
        str  # 'accounting_record', 'bank_statement', 'pl_report', 'testimony'
    )
    source: str
    description: str
    date_collected: datetime.date
    reliability_score: float  # 0.0 to 1.0
    metadata: Dict[str, Any]


@dataclass
class FraudPattern:
    """Represents a detected fraud pattern."""

    pattern_id: str
    pattern_name: str
    description: str
    indicators: List[str]
    severity_score: float  # 0.0 to 10.0
    confidence_score: float  # 0.0 to 1.0
    supporting_evidence: List[str]  # List of evidence_ids


class PaymentFraudAnalyzer:
    """
    Advanced analyzer for payment fraud schemes.

    This class provides comprehensive tools for analyzing payment fraud patterns,
    calculating damages, generating criminal profiles, and creating investigation
    roadmaps based on financial evidence.
    """

    def __init__(
        self,
        case_id: str,
        claimed_amount: Optional[Decimal] = None,
        actual_amount: Optional[Decimal] = None,
        original_debt: Optional[Decimal] = None,
    ):
        """
        Initialize the payment fraud analyzer.

        Args:
            case_id: Unique identifier for the case
            claimed_amount: Amount claimed to have been paid
            actual_amount: Amount actually received
            original_debt: Original debt amount before alleged payments
        """
        self.case_id = case_id
        self.claimed_amount = claimed_amount or Decimal("0")
        self.actual_amount = actual_amount or Decimal("0")
        self.original_debt = original_debt or Decimal("0")
        self.fraud_amount = self.claimed_amount - self.actual_amount
        self.excess_fraud = max(Decimal("0"), self.fraud_amount - self.original_debt)

        self.evidence_collection = []
        self.detected_patterns = []
        self.criminal_profiles = {}
        self.investigation_roadmap = {}
        self.damages_calculation = {}

    def add_evidence(self, evidence: FraudEvidence) -> None:
        """Add a piece of evidence to the fraud case."""
        self.evidence_collection.append(evidence)

    def detect_fraud_patterns(self) -> List[FraudPattern]:
        """
        Analyze the evidence to detect fraud patterns.

        Returns:
            List of detected fraud patterns
        """
        # Implementation would contain sophisticated pattern detection algorithms
        # This is a simplified placeholder implementation

        if self.fraud_amount > 0:
            # Basic false accounting pattern
            false_accounting = FraudPattern(
                pattern_id=f"{self.case_id}_pattern_001",
                pattern_name="False Accounting Entries",
                description="Systematic recording of non-existent payments in accounting records",
                indicators=[
                    "Payment records exist without corresponding receipts",
                    "100% of claimed payments are missing",
                    "Timing coincides with governance disruption",
                ],
                severity_score=9.5 if self.fraud_amount > self.original_debt else 8.5,
                confidence_score=0.95,
                supporting_evidence=[
                    e.evidence_id
                    for e in self.evidence_collection
                    if e.evidence_type in ["accounting_record", "pl_report"]
                ],
            )
            self.detected_patterns.append(false_accounting)

            # Payment misdirection pattern
            if self.fraud_amount > Decimal("1000000"):
                misdirection = FraudPattern(
                    pattern_id=f"{self.case_id}_pattern_002",
                    pattern_name="Payment Misdirection Scheme",
                    description="Systematic diversion of funds to unauthorized accounts",
                    indicators=[
                        "Large discrepancy between claimed and received amounts",
                        "Multiple missing payments over extended period",
                        "Absence of payment confirmation receipts",
                    ],
                    severity_score=9.8,
                    confidence_score=0.90,
                    supporting_evidence=[
                        e.evidence_id
                        for e in self.evidence_collection
                        if e.evidence_type in ["bank_statement", "pl_report"]
                    ],
                )
                self.detected_patterns.append(misdirection)

            # Estate exploitation pattern if relevant evidence exists
            if any(
                e.metadata.get("estate_related", False)
                for e in self.evidence_collection
            ):
                estate_fraud = FraudPattern(
                    pattern_id=f"{self.case_id}_pattern_003",
                    pattern_name="Estate Exploitation",
                    description="Exploitation of deceased person's estate for financial fraud",
                    indicators=[
                        "Fraud timing coincides with estate complications",
                        "Unauthorized access to accounts during estate settlement",
                        "Governance vacuum exploitation",
                    ],
                    severity_score=10.0,
                    confidence_score=0.85,
                    supporting_evidence=[
                        e.evidence_id
                        for e in self.evidence_collection
                        if e.metadata.get("estate_related", False)
                    ],
                )
                self.detected_patterns.append(estate_fraud)

        return self.detected_patterns

    def analyze_fraud_pattern(self) -> Dict[str, Any]:
        """
        Analyze the payment fraud pattern and implications.

        Returns:
            Dictionary containing comprehensive fraud pattern analysis
        """
        # Ensure we have detected patterns
        if not self.detected_patterns:
            self.detect_fraud_patterns()

        # Calculate fraud percentage
        fraud_percentage = (
            (self.fraud_amount / self.original_debt * 100)
            if self.original_debt > 0
            else 0
        )
        excess_percentage = (
            (self.excess_fraud / self.original_debt * 100)
            if self.original_debt > 0
            else 0
        )

        # Determine if estate exploitation is involved
        estate_exploitation = any(
            p.pattern_name == "Estate Exploitation" for p in self.detected_patterns
        )

        analysis = {
            "fraud_scheme": {
                "total_fraudulent_amount": float(self.fraud_amount),
                "original_debt_amount": float(self.original_debt),
                "excess_fraud_amount": float(self.excess_fraud),
                "fraud_percentage": float(fraud_percentage),
                "excess_percentage": float(excess_percentage),
            },
            "criminal_elements": {
                "theft_by_false_pretenses": self.fraud_amount > 0,
                "money_laundering": self.fraud_amount > Decimal("100000"),
                "estate_fraud": estate_exploitation,
                "corporate_fraud": True,
                "systematic_deception": len(self.detected_patterns) > 1,
            },
            "timing_analysis": {
                "execution_period": (
                    "post_murder" if estate_exploitation else "systematic"
                ),
                "exploitation_factor": (
                    "estate_complications"
                    if estate_exploitation
                    else "financial_control"
                ),
                "governance_vacuum": estate_exploitation,
                "oversight_compromised": True,
            },
            "motive_enhancement": {
                "murder_for_financial_gain": estate_exploitation
                and self.fraud_amount > Decimal("1000000"),
                "premeditated_fraud": self.excess_fraud > 0,
                "estate_exploitation": estate_exploitation,
                "systematic_theft": self.fraud_amount > Decimal("500000"),
            },
            "evidence_strength": {
                "documentary_proof": (
                    "Strong" if len(self.evidence_collection) > 5 else "Moderate"
                ),
                "amount_discrepancy": f"{100 if self.actual_amount == 0 else (self.fraud_amount / self.claimed_amount * 100):.1f}% of claimed payments fraudulent",
                "pattern_evidence": f"{len(self.detected_patterns)} distinct fraud patterns detected",
                "criminal_intent": "Evident" if self.excess_fraud > 0 else "Implied",
            },
        }

        return analysis

    def generate_criminal_profile(self, suspect_name: str) -> Dict[str, Any]:
        """
        Generate criminal profile for a suspect based on fraud evidence.

        Args:
            suspect_name: Name of the suspect to profile

        Returns:
            Dictionary containing criminal profile analysis
        """
        # Get relevant evidence for this suspect
        suspect_evidence = [
            e
            for e in self.evidence_collection
            if suspect_name.lower() in e.description.lower()
            or suspect_name.lower() in json.dumps(e.metadata).lower()
        ]

        # Calculate evidence strength
        evidence_strength = len(suspect_evidence) / max(
            1, len(self.evidence_collection)
        )

        # Determine primary role based on evidence
        if evidence_strength > 0.7:
            role = "Architect of payment fraud scheme"
        elif evidence_strength > 0.4:
            role = "Key participant in payment fraud scheme"
        else:
            role = "Suspected participant in payment fraud scheme"

        # Generate profile
        profile = {
            "primary_suspect": suspect_name,
            "criminal_role": role,
            "evidence_strength": evidence_strength,
            "modus_operandi": {
                "method": "False accounting entries",
                "timing": (
                    "Post-murder exploitation"
                    if any(
                        p.pattern_name == "Estate Exploitation"
                        for p in self.detected_patterns
                    )
                    else "Systematic deception"
                ),
                "amount": f"R{float(self.fraud_amount):,.2f} systematic theft",
                "cover": (
                    "Estate complications"
                    if any(
                        p.pattern_name == "Estate Exploitation"
                        for p in self.detected_patterns
                    )
                    else "Financial complexity"
                ),
            },
            "criminal_charges_applicable": [
                "Theft (Criminal Procedure Act)",
                "Fraud (Prevention of Organised Crime Act)",
                (
                    "Money Laundering (Financial Intelligence Centre Act)"
                    if self.fraud_amount > Decimal("100000")
                    else None
                ),
                (
                    "Racketeering (Prevention of Organised Crime Act)"
                    if len(self.detected_patterns) > 1
                    else None
                ),
            ],
            "aggravating_factors": [
                (
                    "Exploitation of murder victim's estate"
                    if any(
                        p.pattern_name == "Estate Exploitation"
                        for p in self.detected_patterns
                    )
                    else None
                ),
                "Systematic deception over extended period",
                "Unauthorized access to company accounts",
                (
                    "Fraudulent amount exceeding actual debt"
                    if self.excess_fraud > 0
                    else None
                ),
            ],
            "investigation_priorities": [
                "Bank record analysis - trace diverted funds",
                "Forensic accounting - complete transaction audit",
                "Asset freezing - secure stolen funds",
                "Criminal referral - Hawks Commercial Crime Unit",
            ],
        }

        # Remove None values
        profile["criminal_charges_applicable"] = [
            c for c in profile["criminal_charges_applicable"] if c
        ]
        profile["aggravating_factors"] = [
            f for f in profile["aggravating_factors"] if f
        ]

        # Store profile
        self.criminal_profiles[suspect_name] = profile

        return profile

    def calculate_damages(
        self,
        interest_rate: float = 0.15,
        fraud_period_years: float = 1.5,
        consequential_rate: float = 0.25,
    ) -> Dict[str, Any]:
        """
        Calculate total damages including fraud, interest, and consequential losses.

        Args:
            interest_rate: Annual interest rate (default: 15%)
            fraud_period_years: Period since fraud occurred (default: 1.5 years)
            consequential_rate: Rate for consequential damages (default: 25% of fraud amount)

        Returns:
            Dictionary containing damages calculation
        """
        # Calculate interest
        interest_on_fraud = (
            self.fraud_amount
            * Decimal(str(interest_rate))
            * Decimal(str(fraud_period_years))
        )

        # Calculate consequential damages
        consequential_damages = self.fraud_amount * Decimal(str(consequential_rate))

        # Calculate total damages
        total_damages = self.fraud_amount + interest_on_fraud + consequential_damages

        # Create damages calculation
        damages = {
            "primary_fraud_amount": float(self.fraud_amount),
            "interest_on_fraud": float(interest_on_fraud),
            "consequential_damages": float(consequential_damages),
            "total_damages_claim": float(total_damages),
            "calculation_basis": {
                "interest_rate": f"{interest_rate * 100:.1f}% per annum",
                "fraud_period": f"{fraud_period_years} years",
                "consequential_rate": f"{consequential_rate * 100:.1f}% of fraud amount",
            },
            "recovery_targets": [
                f"{suspect}" for suspect in self.criminal_profiles.keys()
            ]
            + [
                "Diverted funds in unknown accounts",
                "Corporate liability of involved entities",
                "Any co-conspirators identified",
            ],
        }

        # Store damages calculation
        self.damages_calculation = damages

        return damages

    def generate_investigation_roadmap(self) -> Dict[str, Any]:
        """
        Generate comprehensive investigation roadmap for the fraud case.

        Returns:
            Dictionary containing investigation roadmap
        """
        # Determine priority level based on fraud amount
        if self.fraud_amount > Decimal("1000000"):
            priority_level = "CRITICAL"
        elif self.fraud_amount > Decimal("500000"):
            priority_level = "HIGH"
        else:
            priority_level = "MEDIUM"

        # Generate roadmap
        roadmap = {
            "priority_level": priority_level,
            "immediate_actions": {
                "priority_1": "Secure all financial records and prevent destruction",
                "priority_2": "Trace bank records to identify diverted fund destinations",
                "priority_3": "File criminal complaint with Hawks Commercial Crime Unit",
                "priority_4": "Seek urgent court order for asset freezing",
            },
            "evidence_collection": {
                "digital_forensics": "Preserve all electronic accounting systems",
                "document_seizure": "Secure physical financial documentation",
                "bank_records": "Subpoena complete transaction histories",
                "communication_records": "Preserve emails, messages, calls",
            },
            "legal_strategy": {
                "criminal_prosecution": "Support Hawks investigation with evidence",
                "civil_recovery": f"File damages claim for R{float(self.damages_calculation.get('total_damages_claim', 0)):,.2f} total losses",
                "asset_preservation": "Prevent dissipation of stolen funds",
                "injunctive_relief": "Stop ongoing fraudulent activities",
            },
            "timeline_targets": {
                "week_1": "Criminal complaint filed, evidence secured",
                "week_2": "Asset freezing orders obtained",
                "month_1": "Complete forensic accounting audit",
                "month_3": "Criminal charges laid, civil claim filed",
            },
        }

        # Store roadmap
        self.investigation_roadmap = roadmap

        return roadmap

    def export_fraud_analysis(self, filename: str = None) -> Dict[str, Any]:
        """
        Export complete fraud analysis to JSON format.

        Args:
            filename: Optional filename to save the analysis

        Returns:
            Dictionary containing complete fraud analysis
        """
        # Ensure all analyses are complete
        if not self.detected_patterns:
            self.detect_fraud_patterns()

        if not self.damages_calculation:
            self.calculate_damages()

        if not self.investigation_roadmap:
            self.generate_investigation_roadmap()

        # Create complete fraud analysis
        fraud_data = {
            "case_id": self.case_id,
            "case_update": "Payment Fraud Discovery",
            "analysis_date": datetime.datetime.now().isoformat(),
            "fraud_pattern_analysis": self.analyze_fraud_pattern(),
            "criminal_profiles": self.criminal_profiles,
            "damages_calculation": self.damages_calculation,
            "investigation_roadmap": self.investigation_roadmap,
            "detected_patterns": [
                asdict(pattern) for pattern in self.detected_patterns
            ],
            "evidence_summary": {
                "total_evidence_count": len(self.evidence_collection),
                "evidence_types": {
                    e_type: len(
                        [
                            e
                            for e in self.evidence_collection
                            if e.evidence_type == e_type
                        ]
                    )
                    for e_type in set(e.evidence_type for e in self.evidence_collection)
                },
                "evidence_reliability": sum(
                    e.reliability_score for e in self.evidence_collection
                )
                / max(1, len(self.evidence_collection)),
            },
            "case_classification": f"{self.investigation_roadmap.get('priority_level', 'HIGH')} - Payment Fraud",
            "urgency_level": (
                "MAXIMUM - Immediate Hawks referral required"
                if self.fraud_amount > Decimal("1000000")
                else "HIGH - Urgent investigation required"
            ),
        }

        # Save to file if filename provided
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(fraud_data, f, indent=2, ensure_ascii=False)

        return fraud_data

    @classmethod
    def from_financial_records(
        cls,
        case_id: str,
        accounting_records: Dict[str, Any],
        financial_statements: Dict[str, Any],
        bank_records: Optional[Dict[str, Any]] = None,
    ) -> "PaymentFraudAnalyzer":
        """
        Create a PaymentFraudAnalyzer from financial records.

        Args:
            case_id: Unique identifier for the case
            accounting_records: Dictionary containing accounting records
            financial_statements: Dictionary containing financial statements
            bank_records: Optional dictionary containing bank records

        Returns:
            Initialized PaymentFraudAnalyzer
        """
        # Extract key financial data
        claimed_amount = Decimal(str(accounting_records.get("total_payments", 0)))
        actual_amount = Decimal(str(financial_statements.get("total_receipts", 0)))
        original_debt = Decimal(str(financial_statements.get("opening_balance", 0)))

        # Create analyzer
        analyzer = cls(case_id, claimed_amount, actual_amount, original_debt)

        # Add evidence from accounting records
        for i, record in enumerate(accounting_records.get("payment_records", [])):
            analyzer.add_evidence(
                FraudEvidence(
                    evidence_id=f"{case_id}_acc_{i+1}",
                    evidence_type="accounting_record",
                    source=accounting_records.get("source", "Unknown"),
                    description=f"Payment record: {record.get('description', 'Unknown payment')}",
                    date_collected=datetime.date.today(),
                    reliability_score=0.9,
                    metadata=record,
                )
            )

        # Add evidence from financial statements
        for i, statement in enumerate(financial_statements.get("statements", [])):
            analyzer.add_evidence(
                FraudEvidence(
                    evidence_id=f"{case_id}_fin_{i+1}",
                    evidence_type="pl_report",
                    source=financial_statements.get("source", "Unknown"),
                    description=f"Financial statement: {statement.get('period', 'Unknown period')}",
                    date_collected=datetime.date.today(),
                    reliability_score=0.95,
                    metadata=statement,
                )
            )

        # Add evidence from bank records if available
        if bank_records:
            for i, transaction in enumerate(bank_records.get("transactions", [])):
                analyzer.add_evidence(
                    FraudEvidence(
                        evidence_id=f"{case_id}_bank_{i+1}",
                        evidence_type="bank_statement",
                        source=bank_records.get("source", "Unknown"),
                        description=f"Bank transaction: {transaction.get('description', 'Unknown transaction')}",
                        date_collected=datetime.date.today(),
                        reliability_score=0.98,
                        metadata=transaction,
                    )
                )

        return analyzer


def create_rezonance_fraud_analyzer() -> PaymentFraudAnalyzer:
    """
    Create a PaymentFraudAnalyzer for the ReZonance case.

    Returns:
        Initialized PaymentFraudAnalyzer for the ReZonance case
    """
    # Create analyzer with ReZonance case data
    analyzer = PaymentFraudAnalyzer(
        case_id="rezonance_2017_2025",
        claimed_amount=Decimal("1235361.34"),
        actual_amount=Decimal("0"),
        original_debt=Decimal("1035361.34"),
    )

    # Add evidence
    analyzer.add_evidence(
        FraudEvidence(
            evidence_id="rezonance_acc_1",
            evidence_type="accounting_record",
            source="RegimA Skin Treatments",
            description="RegimA accounting records showing alleged payments to ReZonance",
            date_collected=datetime.date.today(),
            reliability_score=0.9,
            metadata={
                "total_payments": 1235361.34,
                "payment_period": "2022-2023",
                "estate_related": True,
            },
        )
    )

    analyzer.add_evidence(
        FraudEvidence(
            evidence_id="rezonance_pl_1",
            evidence_type="pl_report",
            source="ReZonance (Pty) Ltd",
            description="ReZonance P&L reports showing zero receipts from RegimA",
            date_collected=datetime.date.today(),
            reliability_score=0.95,
            metadata={
                "total_receipts": 0.00,
                "reporting_period": "2022-2023",
                "estate_related": True,
            },
        )
    )

    analyzer.add_evidence(
        FraudEvidence(
            evidence_id="rezonance_est_1",
            evidence_type="testimony",
            source="Estate Documentation",
            description="Kayla Pretorius estate documentation showing governance vacuum",
            date_collected=datetime.date.today(),
            reliability_score=0.85,
            metadata={
                "estate_status": "Unresolved",
                "estate_related": True,
                "governance_impact": "Severe",
            },
        )
    )

    # Generate analysis
    analyzer.detect_fraud_patterns()
    analyzer.generate_criminal_profile("Rynette Farrar")
    analyzer.calculate_damages()
    analyzer.generate_investigation_roadmap()

    return analyzer


if __name__ == "__main__":
    # Create and run ReZonance fraud analyzer
    analyzer = create_rezonance_fraud_analyzer()

    print("🚨 CRITICAL: Analyzing ReZonance Payment Fraud Evidence")
    print("=" * 60)

    fraud_analysis = analyzer.analyze_fraud_pattern()
    print(
        f"💰 Total Fraudulent Amount: R{fraud_analysis['fraud_scheme']['total_fraudulent_amount']:,.2f}"
    )
    print(
        f"📈 Excess Fraud: R{fraud_analysis['fraud_scheme']['excess_fraud_amount']:,.2f}"
    )
    print(
        f"🎯 Fraud Percentage: {fraud_analysis['fraud_scheme']['fraud_percentage']:.1f}%"
    )

    criminal_profile = analyzer.criminal_profiles.get("Rynette Farrar", {})
    print(f"\n🔍 Primary Suspect: {criminal_profile.get('primary_suspect', 'Unknown')}")
    print(
        f"⚖️ Criminal Charges: {len(criminal_profile.get('criminal_charges_applicable', []))} applicable"
    )

    damages = analyzer.damages_calculation
    print(f"\n💸 Total Damages Claim: R{damages.get('total_damages_claim', 0):,.2f}")
    print(f"📊 Interest Component: R{damages.get('interest_on_fraud', 0):,.2f}")

    analysis = analyzer.export_fraud_analysis("rezonance_fraud_analysis.json")
    print(f"\n📄 Fraud analysis exported to: rezonance_fraud_analysis.json")

    print("\n🚨 URGENT ACTION REQUIRED:")
    for i, action in enumerate(
        analyzer.investigation_roadmap.get("immediate_actions", {}).values(), 1
    ):
        print(f"{i}. {action}")
