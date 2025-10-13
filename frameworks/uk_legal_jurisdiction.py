#!/usr/bin/env python3
"""
UK Legal Jurisdiction Interpreter
================================

Interprets legal matters according to UK law, focusing on:
1. Corporate law and director duties
2. Fraud Act 2006 and theft offenses
3. Cross-border commercial obligations
4. Evidence standards and civil procedure
5. International cooperation and enforcement

Key UK Legal Framework:
- Companies Act 2006
- Fraud Act 2006
- Proceeds of Crime Act 2002
- Civil Procedure Rules (CPR)
- Private International Law (Miscellaneous Provisions) Act 1995
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


class UKLegalCategory(Enum):
    """UK legal categories"""
    CORPORATE = "corporate"
    FRAUD = "fraud"
    DIRECTORS_DUTIES = "directors_duties"
    COMMERCIAL = "commercial"
    CROSS_BORDER = "cross_border"
    EVIDENCE = "evidence"
    CIVIL_PROCEDURE = "civil_procedure"


class UKEvidenceStandard(Enum):
    """UK evidence standards"""
    BALANCE_OF_PROBABILITIES = "balance_of_probabilities"  # Civil standard (51%)
    BEYOND_REASONABLE_DOUBT = "beyond_reasonable_doubt"    # Criminal standard
    COGENT_EVIDENCE = "cogent_evidence"                    # Higher civil standard


class UKCourtLevel(Enum):
    """UK court hierarchy levels"""
    MAGISTRATES = "magistrates_court"
    COUNTY = "county_court"
    HIGH_COURT = "high_court"
    COURT_OF_APPEAL = "court_of_appeal"
    SUPREME_COURT = "supreme_court"


@dataclass
class UKLegalPrinciple:
    """Represents a UK legal principle"""
    principle_id: str
    name: str
    description: str
    legal_authority: str  # Statute or case law
    category: UKLegalCategory
    applicability_conditions: List[str]
    legal_consequences: List[str]
    evidence_required: UKEvidenceStandard
    appropriate_court: UKCourtLevel
    
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
        
        # Financial thresholds (UK)
        if "financial loss" in condition_lower or "financial_amount" in condition_lower:
            return facts.get("financial_amount", 0) > 0
        elif "substantial amount" in condition_lower:
            return facts.get("financial_amount", 0) > 25000  # £25k threshold
        elif "director relationship" in condition_lower:
            return facts.get("director_relationship", False)
        elif "cross-border" in condition_lower:
            return facts.get("multiple_jurisdictions", False)
        elif "fraudulent conduct" in condition_lower:
            return facts.get("fraudulent_activity", False)
        elif "uk company" in condition_lower:
            return facts.get("uk_company_involved", False)
        elif "breach_of_duty" in condition_lower:
            return facts.get("director_relationship", False) and facts.get("financial_amount", 0) > 0
        elif "false_representation" in condition_lower:
            return facts.get("fraudulent_activity", False)
        elif "enforcement_required" in condition_lower:
            return facts.get("multiple_jurisdictions", False)
        elif "civil_proceedings" in condition_lower or "documentary_evidence" in condition_lower or "witness_evidence" in condition_lower:
            return True  # Assume these are present in legal cases
        
        return False


@dataclass
class UKLegalAnalysis:
    """UK legal analysis result"""
    analysis_id: str
    applicable_principles: List[UKLegalPrinciple]
    legal_category: UKLegalCategory
    evidence_standard: UKEvidenceStandard
    appropriate_court: UKCourtLevel
    strength_assessment: float  # 0.0 to 1.0
    recommended_actions: List[str]
    jurisdictional_notes: List[str]
    international_considerations: List[str]
    
    def generate_legal_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive legal summary for UK jurisdiction"""
        return {
            "jurisdiction": "United Kingdom",
            "legal_strength": self.strength_assessment,
            "primary_category": self.legal_category.value,
            "evidence_standard": self.evidence_standard.value,
            "appropriate_court": self.appropriate_court.value,
            "applicable_laws": [p.legal_authority for p in self.applicable_principles],
            "recommended_actions": self.recommended_actions,
            "international_notes": self.international_considerations
        }


class UKLegalJurisdictionInterpreter:
    """
    UK legal jurisdiction interpreter for case analysis.
    Applies UK law to case facts and generates legal assessments.
    """
    
    def __init__(self, atomspace: Optional[AtomSpace] = None):
        self.atomspace = atomspace
        self.legal_principles = self._initialize_uk_principles()
        self.inference_rules = self._initialize_uk_inference_rules()
        logger.info("Initialized UK Legal Jurisdiction Interpreter")
    
    def _initialize_uk_principles(self) -> List[UKLegalPrinciple]:
        """Initialize core UK legal principles"""
        principles = []
        
        # Directors' Duties
        principles.append(UKLegalPrinciple(
            principle_id="uk_directors_duties",
            name="Directors' General Duties",
            description="Statutory duties of company directors under Companies Act 2006",
            legal_authority="Companies Act 2006 ss170-177",
            category=UKLegalCategory.DIRECTORS_DUTIES,
            applicability_conditions=[
                "director_relationship",
                "uk_company",
                "breach_of_duty"
            ],
            legal_consequences=[
                "Personal liability to company",
                "Disgorgement of profits",
                "Disqualification proceedings"
            ],
            evidence_required=UKEvidenceStandard.BALANCE_OF_PROBABILITIES,
            appropriate_court=UKCourtLevel.HIGH_COURT
        ))
        
        # Fraud Act 2006
        principles.append(UKLegalPrinciple(
            principle_id="uk_fraud_act",
            name="Fraud by False Representation",
            description="Fraud Act 2006 s2 - fraud by false representation",
            legal_authority="Fraud Act 2006 s2",
            category=UKLegalCategory.FRAUD,
            applicability_conditions=[
                "false_representation",
                "fraudulent_conduct",
                "financial_loss"
            ],
            legal_consequences=[
                "Criminal prosecution",
                "Civil recovery proceedings", 
                "Confiscation under POCA 2002"
            ],
            evidence_required=UKEvidenceStandard.BEYOND_REASONABLE_DOUBT,
            appropriate_court=UKCourtLevel.MAGISTRATES
        ))
        
        # Cross-border Commercial
        principles.append(UKLegalPrinciple(
            principle_id="uk_cross_border_enforcement",
            name="Cross-Border Commercial Enforcement",
            description="Enforcement of UK judgments and obligations across borders",
            legal_authority="Private International Law (Miscellaneous Provisions) Act 1995",
            category=UKLegalCategory.CROSS_BORDER,
            applicability_conditions=[
                "cross-border",
                "commercial_relationship",
                "enforcement_required"
            ],
            legal_consequences=[
                "Recognition of foreign judgments",
                "Enforcement proceedings",
                "International cooperation"
            ],
            evidence_required=UKEvidenceStandard.BALANCE_OF_PROBABILITIES,
            appropriate_court=UKCourtLevel.HIGH_COURT
        ))
        
        # Civil Procedure
        principles.append(UKLegalPrinciple(
            principle_id="uk_civil_evidence",
            name="Civil Evidence and Procedure",
            description="Standards for civil evidence and procedural requirements",
            legal_authority="Civil Evidence Act 1995, CPR Part 32",
            category=UKLegalCategory.EVIDENCE,
            applicability_conditions=[
                "civil_proceedings",
                "documentary_evidence",
                "witness_evidence"
            ],
            legal_consequences=[
                "Admissible evidence standards",
                "Burden of proof allocation",
                "Procedural compliance requirements"
            ],
            evidence_required=UKEvidenceStandard.BALANCE_OF_PROBABILITIES,
            appropriate_court=UKCourtLevel.COUNTY
        ))
        
        return principles
    
    def _initialize_uk_inference_rules(self) -> List[InferenceRule]:
        """Initialize UK-specific inference rules"""
        rules = []
        
        # Directors' duty breach rule
        directors_rule = InferenceRule(
            rule_id="uk_directors_duty_breach",
            rule_type=RuleType.DEDUCTION,
            name="UK Directors' Duty Breach",
            description="Detect breaches of statutory directors' duties",
            premises=[
                {"atom_type": AtomType.ENTITY, "role": "director", "jurisdiction": "uk"},
                {"atom_type": AtomType.EVENT, "type": "corporate_decision"},
                {"personal_benefit": True}
            ],
            conclusion={
                "atom_type": AtomType.PATTERN,
                "name": "directors_duty_breach_uk",
                "legal_significance": 0.8
            }
        )
        rules.append(directors_rule)
        
        # Cross-border fraud rule
        fraud_rule = InferenceRule(
            rule_id="uk_international_fraud",
            rule_type=RuleType.INDUCTION,
            name="International Fraud Pattern",
            description="Detect international fraudulent patterns involving UK entities",
            premises=[
                {"atom_type": AtomType.EVENT, "jurisdiction": "multiple"},
                {"atom_type": AtomType.ENTITY, "type": "uk_company"},
                {"fraudulent_indicators": "present"}
            ],
            conclusion={
                "atom_type": AtomType.PATTERN,
                "name": "international_fraud_uk",
                "legal_significance": 0.9
            }
        )
        rules.append(fraud_rule)
        
        return rules
    
    def analyze_case_facts(self, case_facts: Dict[str, Any]) -> UKLegalAnalysis:
        """Analyze case facts under UK jurisdiction"""
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
            primary_category = UKLegalCategory.COMMERCIAL
        
        # Determine evidence standard
        evidence_standard = UKEvidenceStandard.BALANCE_OF_PROBABILITIES
        if any(p.category == UKLegalCategory.FRAUD for p in applicable_principles):
            evidence_standard = UKEvidenceStandard.BEYOND_REASONABLE_DOUBT
        
        # Determine appropriate court
        court_level = UKCourtLevel.COUNTY
        if applicable_principles:
            # Use highest court level from applicable principles
            court_hierarchy = [
                UKCourtLevel.MAGISTRATES,
                UKCourtLevel.COUNTY,
                UKCourtLevel.HIGH_COURT,
                UKCourtLevel.COURT_OF_APPEAL,
                UKCourtLevel.SUPREME_COURT
            ]
            max_court_idx = max(
                court_hierarchy.index(p.appropriate_court) 
                for p in applicable_principles
            )
            court_level = court_hierarchy[max_court_idx]
        
        # Calculate overall strength
        strength = self._calculate_legal_strength(applicable_principles, case_facts)
        
        # Generate recommendations
        recommendations = self._generate_uk_recommendations(applicable_principles, case_facts)
        
        # International considerations
        international_notes = self._analyze_international_implications(case_facts)
        
        return UKLegalAnalysis(
            analysis_id=f"uk_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            applicable_principles=applicable_principles,
            legal_category=primary_category,
            evidence_standard=evidence_standard,
            appropriate_court=court_level,
            strength_assessment=strength,
            recommended_actions=recommendations,
            jurisdictional_notes=[
                "UK Companies Act 2006 applies to UK-incorporated companies",
                "Civil Procedure Rules govern civil proceedings",
                "Fraud Act 2006 provides criminal fraud framework"
            ],
            international_considerations=international_notes
        )
    
    def _calculate_legal_strength(self, principles: List[UKLegalPrinciple], facts: Dict[str, Any]) -> float:
        """Calculate the overall legal strength of the case under UK law"""
        if not principles:
            return 0.0
        
        total_strength = 0.0
        for principle in principles:
            applicability = principle.evaluate_applicability(facts)
            
            # Weight by legal category significance
            category_weight = {
                UKLegalCategory.FRAUD: 1.0,
                UKLegalCategory.DIRECTORS_DUTIES: 0.9,
                UKLegalCategory.COMMERCIAL: 0.7,
                UKLegalCategory.CROSS_BORDER: 0.8,
                UKLegalCategory.CORPORATE: 0.8,
                UKLegalCategory.EVIDENCE: 0.6,
                UKLegalCategory.CIVIL_PROCEDURE: 0.5
            }.get(principle.category, 0.5)
            
            total_strength += applicability * category_weight
        
        return min(1.0, total_strength / len(principles))
    
    def _generate_uk_recommendations(self, principles: List[UKLegalPrinciple], facts: Dict[str, Any]) -> List[str]:
        """Generate UK-specific legal recommendations"""
        recommendations = []
        
        if any(p.category == UKLegalCategory.FRAUD for p in principles):
            recommendations.extend([
                "Consider reporting to Action Fraud (UK's national fraud reporting centre)",
                "Engage with Serious Fraud Office for complex fraud matters",
                "Pursue civil recovery under Proceeds of Crime Act 2002"
            ])
        
        if any(p.category == UKLegalCategory.DIRECTORS_DUTIES for p in principles):
            recommendations.extend([
                "Pursue derivative claim under Companies Act 2006 s260-264",
                "Consider unfair prejudice petition under s994",
                "Document breaches for potential disqualification proceedings"
            ])
        
        if any(p.category == UKLegalCategory.CROSS_BORDER for p in principles):
            recommendations.extend([
                "Consider Brussels Recast Regulation for EU enforcement",
                "Explore bilateral treaties for non-EU enforcement",
                "Engage specialist international litigation counsel"
            ])
        
        return recommendations
    
    def _analyze_international_implications(self, facts: Dict[str, Any]) -> List[str]:
        """Analyze international legal implications from UK perspective"""
        implications = []
        
        if facts.get("multiple_jurisdictions", False):
            implications.extend([
                "UK courts may exercise jurisdiction over UK companies worldwide",
                "Forum non conveniens may apply for foreign proceedings",
                "Service out of jurisdiction requires court permission under CPR 6.36"
            ])
        
        if facts.get("sa_involvement", False):
            implications.extend([
                "UK-South Africa mutual legal assistance available",
                "Commonwealth legal cooperation frameworks applicable",
                "Consider bilateral investment treaty protections"
            ])
        
        return implications
    
    def get_inference_rules(self) -> List[InferenceRule]:
        """Get UK-specific inference rules for integration with Hyper-Holmes"""
        return self.inference_rules
    
    def interpret_shopify_evidence(self, shopify_data: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret Shopify payment evidence under UK jurisdiction"""
        uk_interpretation = {
            "jurisdiction": "United Kingdom", 
            "legal_implications": [],
            "evidence_weight": 0.0,
            "applicable_statutes": [],
            "procedural_considerations": []
        }
        
        # Analyze UK company payment obligations
        if shopify_data.get("uk_company_payments", False):
            uk_interpretation["legal_implications"].extend([
                "UK company has clear payment obligations documented",
                "Documentary evidence of commercial relationship",
                "Potential claims for recovery if payments unauthorized"
            ])
            uk_interpretation["evidence_weight"] = 0.8
            uk_interpretation["applicable_statutes"].extend([
                "Companies Act 2006 - corporate capacity and authority",
                "Civil Evidence Act 1995 - documentary evidence standards"
            ])
        
        # Directors' authority analysis
        if shopify_data.get("director_authorization_unclear", False):
            uk_interpretation["legal_implications"].extend([
                "Questions over directors' authority for payments",
                "Potential breach of fiduciary duties under s171-177 CA 2006",
                "Ultra vires doctrine may apply to unauthorized payments"
            ])
            uk_interpretation["applicable_statutes"].extend([
                "Companies Act 2006 ss170-177 - directors' duties",
                "Companies Act 2006 s40 - authority of directors"
            ])
        
        # Cross-border enforcement
        if shopify_data.get("international_elements", False):
            uk_interpretation["procedural_considerations"].extend([
                "Service of proceedings may require court permission",
                "Consider appropriate jurisdiction clauses",
                "Enforcement may require recognition proceedings in foreign courts"
            ])
            uk_interpretation["applicable_statutes"].extend([
                "Civil Procedure Rules Part 6 - service out of jurisdiction",
                "Private International Law Act 1995"
            ])
        
        return uk_interpretation


__all__ = [
    "UKLegalCategory",
    "UKEvidenceStandard",
    "UKCourtLevel",
    "UKLegalPrinciple", 
    "UKLegalAnalysis",
    "UKLegalJurisdictionInterpreter"
]