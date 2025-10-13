#!/usr/bin/env python3
"""
South African Legal Jurisdiction Interpreter
===========================================

Interprets legal matters according to South African law, focusing on:
1. Commercial law and fiduciary duties
2. Fraud and theft statutes
3. Corporate governance and director liability
4. Cross-border transaction regulations
5. Evidence standards and burden of proof

Key South African Legal Framework:
- Companies Act 71 of 2008
- Prevention and Combating of Corrupt Activities Act 12 of 2004
- Financial Intelligence Centre Act 38 of 2001
- Cross-Border Insolvency Act 42 of 2000
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from frameworks.opencog_hgnnql import Atom, AtomSpace, AtomType, TruthValue
from frameworks.hyper_holmes_inference import InferenceRule, RuleType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ZALegalCategory(Enum):
    """South African legal categories"""
    COMMERCIAL = "commercial"
    CRIMINAL_FRAUD = "criminal_fraud"
    FIDUCIARY_DUTY = "fiduciary_duty"
    CORPORATE_GOVERNANCE = "corporate_governance"
    CROSS_BORDER = "cross_border"
    EVIDENCE = "evidence"
    DAMAGES = "damages"


class ZAEvidenceStandard(Enum):
    """South African evidence standards"""
    BALANCE_OF_PROBABILITIES = "balance_of_probabilities"  # Civil standard
    BEYOND_REASONABLE_DOUBT = "beyond_reasonable_doubt"    # Criminal standard
    PRIMA_FACIE = "prima_facie"                           # Initial evidence


@dataclass
class ZALegalPrinciple:
    """Represents a South African legal principle"""
    principle_id: str
    name: str
    description: str
    legal_authority: str  # Case law or statute
    category: ZALegalCategory
    applicability_conditions: List[str]
    legal_consequences: List[str]
    evidence_required: ZAEvidenceStandard
    
    def evaluate_applicability(self, case_facts: Dict[str, Any]) -> float:
        """Evaluate how applicable this principle is to given facts"""
        applicability_score = 0.0
        
        for condition in self.applicability_conditions:
            if self._check_condition(condition, case_facts):
                applicability_score += 1.0
                
        return applicability_score / len(self.applicability_conditions) if self.applicability_conditions else 0.0
    
    def _check_condition(self, condition: str, facts: Dict[str, Any]) -> bool:
        """Check if a condition is met by the case facts"""
        condition_lower = condition.lower()
        
        # Financial thresholds
        if "financial loss" in condition_lower or "financial_amount" in condition_lower:
            return facts.get("financial_amount", 0) > 0
        elif "substantial amount" in condition_lower:
            return facts.get("financial_amount", 0) > 100000  # R100k threshold
        elif "fiduciary relationship" in condition_lower or "director_relationship" in condition_lower:
            return facts.get("director_relationship", False)
        elif "cross-border" in condition_lower:
            return facts.get("multiple_jurisdictions", False)
        elif "fraudulent conduct" in condition_lower:
            return facts.get("fraudulent_activity", False)
        elif "company_involved" in condition_lower:
            return True  # Assume company involvement in most cases
        elif "financial_decision_making" in condition_lower:
            return facts.get("financial_amount", 0) > 0  # If there's money involved
        
        return False


@dataclass
class ZALegalAnalysis:
    """South African legal analysis result"""
    analysis_id: str
    applicable_principles: List[ZALegalPrinciple]
    legal_category: ZALegalCategory
    evidence_standard: ZAEvidenceStandard
    strength_assessment: float  # 0.0 to 1.0
    recommended_actions: List[str]
    jurisdictional_notes: List[str]
    cross_border_considerations: List[str]
    
    def generate_legal_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive legal summary for ZA jurisdiction"""
        return {
            "jurisdiction": "South Africa",
            "legal_strength": self.strength_assessment,
            "primary_category": self.legal_category.value,
            "evidence_standard": self.evidence_standard.value,
            "applicable_laws": [p.legal_authority for p in self.applicable_principles],
            "recommended_actions": self.recommended_actions,
            "cross_border_notes": self.cross_border_considerations
        }


class ZALegalJurisdictionInterpreter:
    """
    South African legal jurisdiction interpreter for case analysis.
    Applies ZA law to case facts and generates legal assessments.
    """
    
    def __init__(self, atomspace: Optional[AtomSpace] = None):
        self.atomspace = atomspace
        self.legal_principles = self._initialize_za_principles()
        self.inference_rules = self._initialize_za_inference_rules()
        logger.info("Initialized ZA Legal Jurisdiction Interpreter")
    
    def _initialize_za_principles(self) -> List[ZALegalPrinciple]:
        """Initialize core South African legal principles"""
        principles = []
        
        # Commercial Law Principles
        principles.append(ZALegalPrinciple(
            principle_id="za_fiduciary_duty",
            name="Directors' Fiduciary Duty",
            description="Directors owe fiduciary duties to the company and must act in good faith",
            legal_authority="Companies Act 71 of 2008, s76",
            category=ZALegalCategory.FIDUCIARY_DUTY,
            applicability_conditions=[
                "director_relationship",
                "company_involved",
                "financial_decision_making"
            ],
            legal_consequences=[
                "Personal liability for losses",
                "Disgorgement of profits",
                "Removal from office"
            ],
            evidence_required=ZAEvidenceStandard.BALANCE_OF_PROBABILITIES
        ))
        
        # Criminal Fraud Principles
        principles.append(ZALegalPrinciple(
            principle_id="za_fraud_theft",
            name="Fraud and Theft",
            description="Unlawful appropriation of property with intent to defraud",
            legal_authority="Prevention and Combating of Corrupt Activities Act 12 of 2004",
            category=ZALegalCategory.CRIMINAL_FRAUD,
            applicability_conditions=[
                "fraudulent_conduct",
                "financial_loss",
                "intent_to_defraud"
            ],
            legal_consequences=[
                "Criminal prosecution",
                "Civil damages",
                "Asset forfeiture"
            ],
            evidence_required=ZAEvidenceStandard.BEYOND_REASONABLE_DOUBT
        ))
        
        # Cross-Border Commercial Law
        principles.append(ZALegalPrinciple(
            principle_id="za_cross_border_commercial",
            name="Cross-Border Commercial Obligations",
            description="Commercial obligations between SA and foreign entities",
            legal_authority="Cross-Border Insolvency Act 42 of 2000",
            category=ZALegalCategory.CROSS_BORDER,
            applicability_conditions=[
                "cross-border",
                "commercial_relationship",
                "financial_obligations"
            ],
            legal_consequences=[
                "Enforcement across jurisdictions",
                "Currency conversion obligations",
                "International arbitration"
            ],
            evidence_required=ZAEvidenceStandard.BALANCE_OF_PROBABILITIES
        ))
        
        return principles
    
    def _initialize_za_inference_rules(self) -> List[InferenceRule]:
        """Initialize ZA-specific inference rules"""
        rules = []
        
        # Fiduciary breach rule
        fiduciary_rule = InferenceRule(
            rule_id="za_fiduciary_breach",
            rule_type=RuleType.DEDUCTION,
            name="ZA Fiduciary Duty Breach",
            description="Detect breaches of fiduciary duty under SA law",
            premises=[
                {"atom_type": AtomType.ENTITY, "role": "director"},
                {"atom_type": AtomType.EVENT, "type": "financial_transaction"},
                {"financial_benefit": "personal"}
            ],
            conclusion={
                "atom_type": AtomType.PATTERN, 
                "name": "fiduciary_breach_za",
                "legal_significance": 0.8
            }
        )
        rules.append(fiduciary_rule)
        
        # Cross-border fraud rule
        fraud_rule = InferenceRule(
            rule_id="za_cross_border_fraud",
            rule_type=RuleType.INDUCTION,
            name="Cross-Border Fraud Pattern",
            description="Detect cross-border fraudulent patterns under ZA jurisdiction",
            premises=[
                {"atom_type": AtomType.EVENT, "jurisdiction": "multiple"},
                {"atom_type": AtomType.ENTITY, "type": "financial_flow"},
                {"fraudulent_indicators": "present"}
            ],
            conclusion={
                "atom_type": AtomType.PATTERN,
                "name": "cross_border_fraud_za",
                "legal_significance": 0.9
            }
        )
        rules.append(fraud_rule)
        
        return rules
    
    def analyze_case_facts(self, case_facts: Dict[str, Any]) -> ZALegalAnalysis:
        """Analyze case facts under South African jurisdiction"""
        applicable_principles = []
        
        # Evaluate each principle against the facts
        for principle in self.legal_principles:
            applicability = principle.evaluate_applicability(case_facts)
            if applicability > 0.5:  # Threshold for applicability
                applicable_principles.append(principle)
        
        # Determine primary legal category
        if applicable_principles:
            primary_category = max(
                set(p.category for p in applicable_principles),
                key=lambda cat: sum(1 for p in applicable_principles if p.category == cat)
            )
        else:
            primary_category = ZALegalCategory.COMMERCIAL
        
        # Determine evidence standard
        evidence_standard = ZAEvidenceStandard.BALANCE_OF_PROBABILITIES
        if any(p.category == ZALegalCategory.CRIMINAL_FRAUD for p in applicable_principles):
            evidence_standard = ZAEvidenceStandard.BEYOND_REASONABLE_DOUBT
        
        # Calculate overall strength
        strength = self._calculate_legal_strength(applicable_principles, case_facts)
        
        # Generate recommendations
        recommendations = self._generate_za_recommendations(applicable_principles, case_facts)
        
        # Cross-border considerations
        cross_border_notes = self._analyze_cross_border_implications(case_facts)
        
        return ZALegalAnalysis(
            analysis_id=f"za_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            applicable_principles=applicable_principles,
            legal_category=primary_category,
            evidence_standard=evidence_standard,
            strength_assessment=strength,
            recommended_actions=recommendations,
            jurisdictional_notes=[
                "South African Companies Act 71 of 2008 applies",
                "SARB exchange control regulations may apply for cross-border transactions",
                "Financial Intelligence Centre Act requirements for large transactions"
            ],
            cross_border_considerations=cross_border_notes
        )
    
    def _calculate_legal_strength(self, principles: List[ZALegalPrinciple], facts: Dict[str, Any]) -> float:
        """Calculate the overall legal strength of the case under ZA law"""
        if not principles:
            return 0.0
        
        total_strength = 0.0
        for principle in principles:
            applicability = principle.evaluate_applicability(facts)
            
            # Weight by legal category significance
            category_weight = {
                ZALegalCategory.CRIMINAL_FRAUD: 1.0,
                ZALegalCategory.FIDUCIARY_DUTY: 0.9,
                ZALegalCategory.COMMERCIAL: 0.7,
                ZALegalCategory.CROSS_BORDER: 0.8,
                ZALegalCategory.CORPORATE_GOVERNANCE: 0.8,
                ZALegalCategory.EVIDENCE: 0.6,
                ZALegalCategory.DAMAGES: 0.7
            }.get(principle.category, 0.5)
            
            total_strength += applicability * category_weight
        
        return min(1.0, total_strength / len(principles))
    
    def _generate_za_recommendations(self, principles: List[ZALegalPrinciple], facts: Dict[str, Any]) -> List[str]:
        """Generate ZA-specific legal recommendations"""
        recommendations = []
        
        if any(p.category == ZALegalCategory.CRIMINAL_FRAUD for p in principles):
            recommendations.extend([
                "Consider criminal complaint to SA Police Service Commercial Crimes Unit",
                "Engage with Asset Forfeiture Unit for asset recovery",
                "Document all evidence according to Criminal Procedure Act requirements"
            ])
        
        if any(p.category == ZALegalCategory.FIDUCIARY_DUTY for p in principles):
            recommendations.extend([
                "Pursue derivative action under Companies Act s165",
                "Consider personal liability claim against directors",
                "Document breach of fiduciary duty with expert evidence"
            ])
        
        if any(p.category == ZALegalCategory.CROSS_BORDER for p in principles):
            recommendations.extend([
                "Engage international legal counsel for cross-border enforcement",
                "Consider Hague Convention procedures for service",
                "Review bilateral investment treaties for protection"
            ])
        
        return recommendations
    
    def _analyze_cross_border_implications(self, facts: Dict[str, Any]) -> List[str]:
        """Analyze cross-border legal implications specific to ZA jurisdiction"""
        implications = []
        
        if facts.get("multiple_jurisdictions", False):
            implications.extend([
                "SA courts have jurisdiction over SA-incorporated entities",
                "Foreign judgment enforcement requires High Court recognition",
                "Exchange control approval may be required for settlements > R10M"
            ])
        
        if facts.get("uk_involvement", False):
            implications.extend([
                "Consider UK-SA Double Taxation Agreement implications",
                "Review Investment Promotion and Protection Agreement",
                "Mutual Legal Assistance Treaty available for criminal matters"
            ])
        
        return implications
    
    def get_inference_rules(self) -> List[InferenceRule]:
        """Get ZA-specific inference rules for integration with Hyper-Holmes"""
        return self.inference_rules
    
    def interpret_shopify_evidence(self, shopify_data: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret Shopify payment evidence under ZA jurisdiction"""
        za_interpretation = {
            "jurisdiction": "South Africa",
            "legal_implications": [],
            "evidence_weight": 0.0,
            "applicable_statutes": []
        }
        
        # Analyze payment flow direction
        if shopify_data.get("uk_funding_sa", False):
            za_interpretation["legal_implications"].extend([
                "UK entity funding SA operations creates creditor-debtor relationship",
                "May constitute financial assistance under Companies Act",
                "Potential tax implications for both SA and UK entities"
            ])
            za_interpretation["evidence_weight"] = 0.8
            za_interpretation["applicable_statutes"].extend([
                "Companies Act 71 of 2008 s44-s46 (Financial Assistance)",
                "Income Tax Act 58 of 1962",
                "Exchange Control Regulations"
            ])
        
        # False claims analysis
        if shopify_data.get("contradicts_sworn_statements", False):
            za_interpretation["legal_implications"].extend([
                "Documentary evidence contradicts sworn affidavits - potential perjury",
                "Misrepresentation in legal proceedings under Perjury Act",
                "Breach of good faith in litigation"
            ])
            za_interpretation["applicable_statutes"].extend([
                "Perjury Act 1963",
                "Criminal Procedure Act 51 of 1977"
            ])
            za_interpretation["evidence_weight"] = max(za_interpretation["evidence_weight"], 0.9)
        
        return za_interpretation


__all__ = [
    "ZALegalCategory",
    "ZAEvidenceStandard", 
    "ZALegalPrinciple",
    "ZALegalAnalysis",
    "ZALegalJurisdictionInterpreter"
]