#!/usr/bin/env python3
"""
Citizenship Settlement Analyzer

Provides analysis tools for assessing citizenship status impacts on settlement agreements,
particularly distinguishing between civil/psychological and commercial matters.

This module supports the analysis framework for understanding how citizenship status
affects settlement agreement enforceability and structure.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class CitizenshipStatus(Enum):
    FULL_CITIZEN = "full_citizen"
    PERMANENT_RESIDENT = "permanent_resident"
    TEMPORARY_RESIDENT = "temporary_resident"
    VISA_HOLDER = "visa_holder"
    STATELESS = "stateless"
    DUAL_CITIZEN = "dual_citizen"


class SettlementType(Enum):
    PSYCHOLOGICAL = "psychological"
    CIVIL_PERSONAL = "civil_personal"
    COMMERCIAL = "commercial"
    PROPERTY = "property"
    FAMILY = "family"
    CRIMINAL = "criminal"


class EnforcementComplexity(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    CRITICAL = "critical"


@dataclass
class CitizenshipProfile:
    """Profile of an individual's citizenship and residency status"""
    primary_citizenship: str
    secondary_citizenship: Optional[str] = None
    residency_status: CitizenshipStatus = CitizenshipStatus.FULL_CITIZEN
    tax_residence: str = ""
    legal_domicile: str = ""
    years_of_residence: int = 0
    language_preferences: List[str] = None
    cultural_background: str = ""
    
    def __post_init__(self):
        if self.language_preferences is None:
            self.language_preferences = []


@dataclass
class SettlementImpactAssessment:
    """Assessment of citizenship impact on settlement agreement"""
    settlement_type: SettlementType
    citizenship_impact_level: str
    enforceable_elements: List[str]
    unenforceable_elements: List[str]
    enforcement_complexity: EnforcementComplexity
    required_jurisdictions: List[str]
    cultural_considerations: List[str]
    appeal_mechanisms: List[str]
    risk_factors: List[str]


class CitizenshipSettlementAnalyzer:
    """Analyzer for citizenship impacts on settlement agreements"""
    
    def __init__(self):
        self.impact_matrix = self._initialize_impact_matrix()
        self.enforcement_rules = self._initialize_enforcement_rules()
    
    def _initialize_impact_matrix(self) -> Dict[SettlementType, Dict[CitizenshipStatus, str]]:
        """Initialize the citizenship impact matrix for different settlement types"""
        return {
            SettlementType.PSYCHOLOGICAL: {
                CitizenshipStatus.FULL_CITIZEN: "CRITICAL",
                CitizenshipStatus.PERMANENT_RESIDENT: "CRITICAL", 
                CitizenshipStatus.TEMPORARY_RESIDENT: "VERY_HIGH",
                CitizenshipStatus.VISA_HOLDER: "VERY_HIGH",
                CitizenshipStatus.DUAL_CITIZEN: "CRITICAL",
                CitizenshipStatus.STATELESS: "CRITICAL"
            },
            SettlementType.CIVIL_PERSONAL: {
                CitizenshipStatus.FULL_CITIZEN: "HIGH",
                CitizenshipStatus.PERMANENT_RESIDENT: "HIGH",
                CitizenshipStatus.TEMPORARY_RESIDENT: "MODERATE",
                CitizenshipStatus.VISA_HOLDER: "HIGH",
                CitizenshipStatus.DUAL_CITIZEN: "VERY_HIGH",
                CitizenshipStatus.STATELESS: "CRITICAL"
            },
            SettlementType.COMMERCIAL: {
                CitizenshipStatus.FULL_CITIZEN: "MODERATE",
                CitizenshipStatus.PERMANENT_RESIDENT: "MODERATE",
                CitizenshipStatus.TEMPORARY_RESIDENT: "MODERATE",
                CitizenshipStatus.VISA_HOLDER: "HIGH",
                CitizenshipStatus.DUAL_CITIZEN: "MODERATE",
                CitizenshipStatus.STATELESS: "HIGH"
            },
            SettlementType.PROPERTY: {
                CitizenshipStatus.FULL_CITIZEN: "HIGH",
                CitizenshipStatus.PERMANENT_RESIDENT: "HIGH",
                CitizenshipStatus.TEMPORARY_RESIDENT: "VERY_HIGH",
                CitizenshipStatus.VISA_HOLDER: "VERY_HIGH",
                CitizenshipStatus.DUAL_CITIZEN: "MODERATE",
                CitizenshipStatus.STATELESS: "CRITICAL"
            }
        }
    
    def _initialize_enforcement_rules(self) -> Dict[str, Dict[str, any]]:
        """Initialize enforcement rules based on citizenship patterns"""
        return {
            "british_tax_vote_disconnect": {
                "description": "British citizens with permanent residency can pay tax but not vote",
                "principle": "Civic rights vs fiscal obligations separation",
                "enforceable": ["tax_obligations", "financial_disclosure", "economic_activity"],
                "unenforceable": ["voting_agreements", "political_participation", "civic_duty_impositions"],
                "jurisdictional_complexity": "MODERATE"
            },
            "dual_citizenship_conflicts": {
                "description": "Conflicting obligations from multiple citizenships",
                "principle": "Jurisdictional layering effect",
                "enforceable": ["economic_settlements", "property_agreements"],
                "unenforceable": ["military_service_agreements", "conflicting_civic_duties"],
                "jurisdictional_complexity": "VERY_HIGH"
            },
            "incomplete_integration": {
                "description": "Economic integration before civic integration",
                "principle": "Incomplete integration principle",
                "enforceable": ["business_licensing", "property_rights", "financial_obligations"],
                "unenforceable": ["professional_licensing_guarantees", "political_rights"],
                "jurisdictional_complexity": "HIGH"
            }
        }
    
    def analyze_citizenship_impact(self, 
                                 citizenship_profile: CitizenshipProfile,
                                 settlement_type: SettlementType) -> SettlementImpactAssessment:
        """Analyze the impact of citizenship status on a settlement agreement"""
        
        # Get base impact level
        impact_level = self.impact_matrix[settlement_type][citizenship_profile.residency_status]
        
        # Determine enforcement complexity
        enforcement_complexity = self._assess_enforcement_complexity(citizenship_profile, settlement_type)
        
        # Identify enforceable and unenforceable elements
        enforceable, unenforceable = self._categorize_settlement_elements(
            citizenship_profile, settlement_type
        )
        
        # Identify required jurisdictions
        jurisdictions = self._identify_jurisdictions(citizenship_profile)
        
        # Assess cultural considerations
        cultural_considerations = self._assess_cultural_considerations(
            citizenship_profile, settlement_type
        )
        
        # Identify appeal mechanisms
        appeal_mechanisms = self._identify_appeal_mechanisms(citizenship_profile)
        
        # Assess risk factors
        risk_factors = self._assess_risk_factors(citizenship_profile, settlement_type)
        
        return SettlementImpactAssessment(
            settlement_type=settlement_type,
            citizenship_impact_level=impact_level,
            enforceable_elements=enforceable,
            unenforceable_elements=unenforceable,
            enforcement_complexity=enforcement_complexity,
            required_jurisdictions=jurisdictions,
            cultural_considerations=cultural_considerations,
            appeal_mechanisms=appeal_mechanisms,
            risk_factors=risk_factors
        )
    
    def _assess_enforcement_complexity(self, 
                                     citizenship_profile: CitizenshipProfile,
                                     settlement_type: SettlementType) -> EnforcementComplexity:
        """Assess enforcement complexity based on citizenship and settlement type"""
        
        # Base complexity from settlement type
        base_complexity = {
            SettlementType.PSYCHOLOGICAL: EnforcementComplexity.VERY_HIGH,
            SettlementType.CIVIL_PERSONAL: EnforcementComplexity.HIGH,
            SettlementType.COMMERCIAL: EnforcementComplexity.MODERATE,
            SettlementType.PROPERTY: EnforcementComplexity.HIGH
        }[settlement_type]
        
        # Adjust for citizenship complexity
        if citizenship_profile.secondary_citizenship:
            # Dual citizenship increases complexity
            complexity_levels = [EnforcementComplexity.LOW, EnforcementComplexity.MODERATE, 
                               EnforcementComplexity.HIGH, EnforcementComplexity.VERY_HIGH, 
                               EnforcementComplexity.CRITICAL]
            current_index = complexity_levels.index(base_complexity)
            if current_index < len(complexity_levels) - 1:
                base_complexity = complexity_levels[current_index + 1]
        
        if citizenship_profile.residency_status in [CitizenshipStatus.TEMPORARY_RESIDENT, 
                                                   CitizenshipStatus.VISA_HOLDER]:
            # Temporary status increases complexity
            complexity_levels = [EnforcementComplexity.LOW, EnforcementComplexity.MODERATE, 
                               EnforcementComplexity.HIGH, EnforcementComplexity.VERY_HIGH, 
                               EnforcementComplexity.CRITICAL]
            current_index = complexity_levels.index(base_complexity)
            if current_index < len(complexity_levels) - 1:
                base_complexity = complexity_levels[current_index + 1]
        
        return base_complexity
    
    def _categorize_settlement_elements(self, 
                                      citizenship_profile: CitizenshipProfile,
                                      settlement_type: SettlementType) -> Tuple[List[str], List[str]]:
        """Categorize settlement elements as enforceable or unenforceable"""
        
        if settlement_type == SettlementType.PSYCHOLOGICAL:
            enforceable = [
                "medical_assessment_compliance",
                "treatment_cost_obligations", 
                "confidentiality_agreements",
                "professional_licensing_verification"
            ]
            unenforceable = [
                "cultural_assessment_guarantees",
                "specific_outcome_requirements",
                "cross_border_enforcement_without_treaty"
            ]
            
            # Adjust based on citizenship status
            if citizenship_profile.residency_status != CitizenshipStatus.FULL_CITIZEN:
                unenforceable.extend([
                    "appeal_mechanism_guarantees",
                    "language_service_guarantees"
                ])
            
            # Special case: British citizen in foreign jurisdiction psychological settlement
            if (citizenship_profile.primary_citizenship == "British" and 
                citizenship_profile.legal_domicile != "UK"):
                unenforceable.extend([
                    "medical_assessments_by_non_uk_licensed_professionals",
                    "psychological_evaluations_under_foreign_standards",
                    "mental_health_determinations_without_uk_oversight",
                    "medical_privacy_waivers_exceeding_uk_standards"
                ])
                # Only UK-compliant medical obligations remain enforceable
                enforceable = [item for item in enforceable if "licensing" in item or "cost" in item]
        
        elif settlement_type == SettlementType.COMMERCIAL:
            enforceable = [
                "financial_obligations",
                "business_compliance_requirements",
                "asset_disclosure",
                "tax_obligations"
            ]
            unenforceable = [
                "political_activity_restrictions",
                "civic_participation_requirements"
            ]
            
        elif settlement_type == SettlementType.CIVIL_PERSONAL:
            enforceable = [
                "financial_support_obligations",
                "property_transfer_agreements",
                "disclosure_requirements"
            ]
            unenforceable = [
                "voting_behavior_agreements",
                "political_affiliation_restrictions",
                "civic_duty_modifications"
            ]
            
            # British tax-vote disconnect example
            if (citizenship_profile.primary_citizenship == "British" and 
                citizenship_profile.residency_status == CitizenshipStatus.PERMANENT_RESIDENT):
                enforceable.extend([
                    "tax_payment_schedules",
                    "financial_disclosure_requirements"
                ])
                unenforceable.extend([
                    "voting_rights_agreements",
                    "political_participation_settlements"
                ])
            
            # British citizen in foreign jurisdiction civil settlement capacity limitations
            if (citizenship_profile.primary_citizenship == "British" and 
                citizenship_profile.legal_domicile != "UK"):
                unenforceable.extend([
                    "foreign_civic_duties_binding_british_citizens",
                    "personal_status_changes_under_foreign_law",
                    "family_law_obligations_conflicting_with_uk_law",
                    "civil_rights_waivers_exceeding_uk_standards"
                ])
        
        else:
            # Default categorization
            enforceable = [
                "financial_obligations",
                "compliance_requirements"
            ]
            unenforceable = [
                "political_rights_modifications",
                "civic_status_changes"
            ]
        
        return enforceable, unenforceable
    
    def _identify_jurisdictions(self, citizenship_profile: CitizenshipProfile) -> List[str]:
        """Identify relevant jurisdictions for enforcement"""
        jurisdictions = []
        
        # Primary citizenship jurisdiction
        if citizenship_profile.primary_citizenship:
            jurisdictions.append(citizenship_profile.primary_citizenship)
        
        # Secondary citizenship jurisdiction
        if citizenship_profile.secondary_citizenship:
            jurisdictions.append(citizenship_profile.secondary_citizenship)
        
        # Tax residence jurisdiction
        if (citizenship_profile.tax_residence and 
            citizenship_profile.tax_residence not in jurisdictions):
            jurisdictions.append(citizenship_profile.tax_residence)
        
        # Legal domicile jurisdiction
        if (citizenship_profile.legal_domicile and 
            citizenship_profile.legal_domicile not in jurisdictions):
            jurisdictions.append(citizenship_profile.legal_domicile)
        
        return jurisdictions
    
    def _assess_cultural_considerations(self, 
                                     citizenship_profile: CitizenshipProfile,
                                     settlement_type: SettlementType) -> List[str]:
        """Assess cultural considerations for the settlement"""
        considerations = []
        
        if settlement_type == SettlementType.PSYCHOLOGICAL:
            considerations.extend([
                "Cultural competency in psychological assessment",
                "Language rights for evaluation",
                "Cultural background appropriate standards",
                "Religious/cultural sensitivity requirements"
            ])
        
        if citizenship_profile.language_preferences:
            considerations.append(
                f"Language services required: {', '.join(citizenship_profile.language_preferences)}"
            )
        
        if citizenship_profile.cultural_background:
            considerations.append(
                f"Cultural background considerations: {citizenship_profile.cultural_background}"
            )
        
        # Dual citizenship cultural complexity
        if citizenship_profile.secondary_citizenship:
            considerations.append(
                "Dual citizenship cultural identity considerations"
            )
        
        return considerations
    
    def _identify_appeal_mechanisms(self, citizenship_profile: CitizenshipProfile) -> List[str]:
        """Identify available appeal mechanisms based on citizenship"""
        mechanisms = []
        
        if citizenship_profile.residency_status == CitizenshipStatus.FULL_CITIZEN:
            mechanisms.extend([
                "Full domestic court system access",
                "Constitutional rights protection",
                "Administrative law appeals",
                "Human rights tribunal access"
            ])
        
        elif citizenship_profile.residency_status == CitizenshipStatus.PERMANENT_RESIDENT:
            mechanisms.extend([
                "Limited domestic court access",
                "Administrative appeals for residency matters",
                "Human rights protections (limited)"
            ])
        
        elif citizenship_profile.residency_status in [CitizenshipStatus.TEMPORARY_RESIDENT, 
                                                     CitizenshipStatus.VISA_HOLDER]:
            mechanisms.extend([
                "Immigration court access only",
                "Limited administrative appeals",
                "Consular assistance from home country"
            ])
        
        # Dual citizenship additional mechanisms
        if citizenship_profile.secondary_citizenship:
            mechanisms.append("Consular assistance from secondary citizenship country")
        
        return mechanisms
    
    def _assess_risk_factors(self, 
                           citizenship_profile: CitizenshipProfile,
                           settlement_type: SettlementType) -> List[str]:
        """Assess risk factors based on citizenship and settlement type"""
        risks = []
        
        # Status change risks
        if citizenship_profile.residency_status in [CitizenshipStatus.TEMPORARY_RESIDENT, 
                                                   CitizenshipStatus.VISA_HOLDER]:
            risks.append("Settlement enforceability at risk if residency status changes")
        
        # Jurisdictional conflict risks
        if citizenship_profile.secondary_citizenship:
            risks.append("Conflicting jurisdictional obligations from dual citizenship")
        
        # Cultural assessment risks for psychological settlements
        if settlement_type == SettlementType.PSYCHOLOGICAL:
            risks.extend([
                "Cross-cultural assessment validity challenges",
                "Professional licensing jurisdiction issues",
                "Cultural bias in evaluation standards"
            ])
        
        # Cross-jurisdictional legal capacity risks
        if (citizenship_profile.primary_citizenship and 
            citizenship_profile.legal_domicile and 
            citizenship_profile.primary_citizenship.lower() != citizenship_profile.legal_domicile.lower()):
            risks.extend([
                "Legal capacity limitations for foreign citizenship settlement clauses",
                "Convoluted legal language may create obligations exceeding legal capacity",
                "Home country law conflicts with settlement jurisdiction requirements"
            ])
            
            # Specific risks for British citizens in foreign settlements
            if citizenship_profile.primary_citizenship == "British":
                risks.extend([
                    "UK legal standards may not recognize foreign professional assessments",
                    "British constitutional rights may conflict with settlement obligations",
                    "Medical/psychological clauses may lack validity without UK professional oversight"
                ])
        
        # Language barrier risks
        if (citizenship_profile.language_preferences and 
            len(citizenship_profile.language_preferences) > 1):
            risks.append("Language barrier complications in settlement implementation")
        
        # Enforcement jurisdiction risks
        jurisdictions = self._identify_jurisdictions(citizenship_profile)
        if len(jurisdictions) > 2:
            risks.append("Multiple jurisdiction enforcement complexity")
        
        return risks
    
    def assess_cross_jurisdictional_legal_capacity(self, 
                                                 citizenship_profile: CitizenshipProfile,
                                                 settlement_jurisdiction: str) -> Dict[str, any]:
        """Assess legal capacity for cross-jurisdictional settlement agreements"""
        
        capacity_assessment = {
            "primary_citizenship": citizenship_profile.primary_citizenship,
            "settlement_jurisdiction": settlement_jurisdiction,
            "capacity_by_clause_type": {},
            "restrictions": [],
            "recommendations": []
        }
        
        # Assess capacity for different clause types
        clause_types = {
            "economic_financial_tax": "FULL_CAPACITY",
            "civic_civil_personal": "LIMITED_CAPACITY", 
            "psychological_medical": "HIGHLY_RESTRICTED_CAPACITY"
        }
        
        for clause_type, base_capacity in clause_types.items():
            capacity_details = {
                "capacity_level": base_capacity,
                "enforceable_elements": [],
                "unenforceable_elements": [],
                "special_requirements": []
            }
            
            # Adjust based on specific citizenship and jurisdiction combinations
            if (citizenship_profile.primary_citizenship == "British" and 
                settlement_jurisdiction == "South Africa"):
                
                if clause_type == "economic_financial_tax":
                    capacity_details["enforceable_elements"] = [
                        "tax_payment_obligations",
                        "financial_disclosure_requirements",
                        "asset_transfer_agreements",
                        "business_compliance_requirements"
                    ]
                    capacity_details["special_requirements"] = [
                        "UK tax treaty provisions may apply",
                        "Double taxation agreements must be considered"
                    ]
                
                elif clause_type == "civic_civil_personal":
                    capacity_details["capacity_level"] = "NO_CAPACITY"
                    capacity_details["unenforceable_elements"] = [
                        "south_african_civic_duties",
                        "political_participation_requirements",
                        "family_law_under_sa_standards",
                        "personal_status_determinations"
                    ]
                    capacity_details["restrictions"] = [
                        "Cannot bind British citizens to South African civic obligations",
                        "Personal status governed by UK law for British citizens"
                    ]
                
                elif clause_type == "psychological_medical":
                    capacity_details["capacity_level"] = "NO_CAPACITY"
                    capacity_details["unenforceable_elements"] = [
                        "psychological_evaluations_by_sa_professionals",
                        "mental_health_determinations_under_sa_law",
                        "medical_privacy_waivers_exceeding_uk_standards",
                        "treatment_requirements_without_uk_oversight"
                    ]
                    capacity_details["restrictions"] = [
                        "UK medical privacy laws may prohibit certain disclosures",
                        "Professional licensing jurisdiction conflicts",
                        "Cultural competency standards differences"
                    ]
            
            capacity_assessment["capacity_by_clause_type"][clause_type] = capacity_details
        
        # General recommendations
        capacity_assessment["recommendations"] = [
            "Separate settlement clauses by capacity level",
            "Include severability provisions for invalid clauses",
            "Require home country legal review for complex language",
            "Explicitly exclude obligations exceeding legal capacity",
            "Consider creating separate agreements for different clause types"
        ]
        
        return capacity_assessment
    
    def generate_citizenship_settlement_report(self, 
                                             citizenship_profile: CitizenshipProfile,
                                             settlement_type: SettlementType,
                                             case_id: Optional[str] = None) -> Dict[str, any]:
        """Generate a comprehensive citizenship settlement analysis report"""
        
        assessment = self.analyze_citizenship_impact(citizenship_profile, settlement_type)
        
        # Convert enums to strings for JSON serialization
        profile_dict = asdict(citizenship_profile)
        profile_dict['residency_status'] = citizenship_profile.residency_status.value
        
        assessment_dict = asdict(assessment)
        assessment_dict['settlement_type'] = assessment.settlement_type.value
        assessment_dict['enforcement_complexity'] = assessment.enforcement_complexity.value
        
        report = {
            "analysis_metadata": {
                "case_id": case_id,
                "analysis_date": datetime.now().isoformat(),
                "analyzer_version": "1.0.0"
            },
            "citizenship_profile": profile_dict,
            "settlement_assessment": assessment_dict,
            "recommendations": self._generate_recommendations(citizenship_profile, assessment),
            "applicable_enforcement_rules": self._get_applicable_rules(citizenship_profile),
            "compliance_checklist": self._generate_compliance_checklist(citizenship_profile, settlement_type)
        }
        
        return report
    
    def _generate_recommendations(self, 
                                citizenship_profile: CitizenshipProfile,
                                assessment: SettlementImpactAssessment) -> List[str]:
        """Generate recommendations based on citizenship analysis"""
        recommendations = []
        
        # Jurisdictional recommendations
        if len(assessment.required_jurisdictions) > 1:
            recommendations.append(
                "Include jurisdictional specification clauses for each settlement element"
            )
            recommendations.append(
                "Add severability provisions to handle jurisdictional conflicts"
            )
        
        # Cultural competency recommendations
        if assessment.settlement_type == SettlementType.PSYCHOLOGICAL:
            recommendations.append(
                "Verify cultural competency of all psychological assessment professionals"
            )
            recommendations.append(
                "Ensure language services meet citizenship-based requirements"
            )
        
        # Status change contingencies
        if citizenship_profile.residency_status in [CitizenshipStatus.TEMPORARY_RESIDENT, 
                                                   CitizenshipStatus.VISA_HOLDER]:
            recommendations.append(
                "Include contingency clauses for potential residency status changes"
            )
        
        # Appeal mechanism clarification
        recommendations.append(
            "Clearly specify available appeal mechanisms based on citizenship status"
        )
        
        return recommendations
    
    def _get_applicable_rules(self, citizenship_profile: CitizenshipProfile) -> List[Dict[str, any]]:
        """Get enforcement rules applicable to the citizenship profile"""
        applicable_rules = []
        
        # British tax-vote disconnect rule
        if (citizenship_profile.primary_citizenship == "British" and 
            citizenship_profile.residency_status == CitizenshipStatus.PERMANENT_RESIDENT):
            applicable_rules.append(self.enforcement_rules["british_tax_vote_disconnect"])
        
        # Dual citizenship conflicts
        if citizenship_profile.secondary_citizenship:
            applicable_rules.append(self.enforcement_rules["dual_citizenship_conflicts"])
        
        # Incomplete integration
        if citizenship_profile.residency_status != CitizenshipStatus.FULL_CITIZEN:
            applicable_rules.append(self.enforcement_rules["incomplete_integration"])
        
        return applicable_rules
    
    def _generate_compliance_checklist(self, 
                                     citizenship_profile: CitizenshipProfile,
                                     settlement_type: SettlementType) -> List[str]:
        """Generate a compliance checklist for citizenship-aware settlements"""
        checklist = [
            "Verify exact citizenship and residency status of all parties",
            "Confirm legal capacity in all relevant jurisdictions",
            "Map enforcement pathways for each settlement element",
            "Assess cultural competency requirements",
            "Verify professional licensing in applicable jurisdictions",
            "Clarify available appeal mechanisms",
            "Include status change contingency provisions",
            "Add jurisdictional specification clauses",
            "Include severability provisions for cross-jurisdictional conflicts"
        ]
        
        # Settlement type specific items
        if settlement_type == SettlementType.PSYCHOLOGICAL:
            checklist.extend([
                "Verify cultural competency of assessment professionals",
                "Confirm language service availability and quality",
                "Assess cultural bias risks in evaluation standards",
                "Verify medical licensing across relevant jurisdictions"
            ])
        
        return checklist


# Example usage and testing functions
def create_sample_profiles() -> Dict[str, CitizenshipProfile]:
    """Create sample citizenship profiles for testing"""
    return {
        "british_permanent_resident": CitizenshipProfile(
            primary_citizenship="British",
            residency_status=CitizenshipStatus.PERMANENT_RESIDENT,
            tax_residence="UK",
            legal_domicile="UK",
            years_of_residence=10,
            language_preferences=["English"],
            cultural_background="British"
        ),
        "dual_citizen_us_canada": CitizenshipProfile(
            primary_citizenship="US",
            secondary_citizenship="Canada",
            residency_status=CitizenshipStatus.DUAL_CITIZEN,
            tax_residence="US",
            legal_domicile="Canada",
            years_of_residence=15,
            language_preferences=["English", "French"],
            cultural_background="North American"
        ),
        "temporary_resident": CitizenshipProfile(
            primary_citizenship="India",
            residency_status=CitizenshipStatus.TEMPORARY_RESIDENT,
            tax_residence="Australia",
            legal_domicile="India",
            years_of_residence=3,
            language_preferences=["Hindi", "English"],
            cultural_background="South Asian"
        )
    }


if __name__ == "__main__":
    # Example usage
    analyzer = CitizenshipSettlementAnalyzer()
    profiles = create_sample_profiles()
    
    # Analyze British citizen legal capacity in South African settlement
    print("=== BRITISH CITIZEN LEGAL CAPACITY IN SOUTH AFRICAN SETTLEMENT ===")
    british_in_sa = CitizenshipProfile(
        primary_citizenship="British",
        residency_status=CitizenshipStatus.FULL_CITIZEN,
        legal_domicile="South Africa",  # British citizen in SA jurisdiction
        tax_residence="South Africa"
    )
    
    # Assess cross-jurisdictional legal capacity
    capacity_assessment = analyzer.assess_cross_jurisdictional_legal_capacity(
        british_in_sa, "South Africa"
    )
    
    print(f"Primary Citizenship: {capacity_assessment['primary_citizenship']}")
    print(f"Settlement Jurisdiction: {capacity_assessment['settlement_jurisdiction']}")
    print("\nCapacity by Clause Type:")
    for clause_type, details in capacity_assessment['capacity_by_clause_type'].items():
        print(f"\n{clause_type.upper().replace('_', ' ')}:")
        print(f"  Capacity Level: {details['capacity_level']}")
        if details['enforceable_elements']:
            print(f"  Enforceable: {details['enforceable_elements']}")
        if details['unenforceable_elements']:
            print(f"  Unenforceable: {details['unenforceable_elements']}")
        if details.get('restrictions'):
            print(f"  Restrictions: {details['restrictions']}")
    
    print(f"\nRecommendations: {capacity_assessment['recommendations']}")
    
    # Test different settlement types for British citizen
    print("\n=== SETTLEMENT TYPE ANALYSIS FOR BRITISH CITIZEN ===")
    settlement_types = [SettlementType.PSYCHOLOGICAL, SettlementType.CIVIL_PERSONAL, SettlementType.COMMERCIAL]
    
    for settlement_type in settlement_types:
        assessment = analyzer.analyze_citizenship_impact(british_in_sa, settlement_type)
        print(f"\n{settlement_type.value.upper()} Settlement:")
        print(f"  Impact Level: {assessment.citizenship_impact_level}")
        print(f"  Risk Factors: {len(assessment.risk_factors)} identified")
        print(f"  Enforcement Complexity: {assessment.enforcement_complexity.value}")
    
    # Generate full report
    report = analyzer.generate_citizenship_settlement_report(
        british_in_sa, SettlementType.PSYCHOLOGICAL, "british_sa_capacity_analysis"
    )
    
    # Save report to file
    output_path = Path("/tmp/british_sa_legal_capacity_report.json")
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nFull legal capacity analysis report saved to: {output_path}")