#!/usr/bin/env python3
"""
Integrated Settlement and Citizenship Analysis for Case 2025_137857

This script demonstrates how to combine the existing settlement agreement analysis 
with the new citizenship settlement analysis framework to provide comprehensive 
insights into the case.
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add the tools directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from citizenship_settlement_analyzer import (
        CitizenshipSettlementAnalyzer,
        CitizenshipProfile,
        CitizenshipStatus,
        SettlementType
    )
except ImportError:
    print("Error: citizenship_settlement_analyzer module not found")
    sys.exit(1)


class IntegratedCaseAnalyzer:
    """
    Integrated analyzer combining settlement agreement analysis with citizenship considerations
    for Case 2025_137857
    """
    
    def __init__(self):
        self.citizenship_analyzer = CitizenshipSettlementAnalyzer()
        self.case_id = "case_2025_137857"
        
    def create_case_profiles(self) -> Dict[str, CitizenshipProfile]:
        """Create citizenship profiles for the parties in Case 2025_137857"""
        
        # Based on the case documents, creating likely profiles for South African parties
        profiles = {
            "jacqueline_faucitt": CitizenshipProfile(
                primary_citizenship="South African",
                residency_status=CitizenshipStatus.FULL_CITIZEN,
                tax_residence="South Africa",
                legal_domicile="South Africa",
                years_of_residence=50,  # Assuming long-term residence
                language_preferences=["English", "Afrikaans"],
                cultural_background="South African"
            ),
            "daniel_faucitt": CitizenshipProfile(
                primary_citizenship="South African", 
                residency_status=CitizenshipStatus.FULL_CITIZEN,
                tax_residence="South Africa",
                legal_domicile="South Africa",
                years_of_residence=25,  # Younger party
                language_preferences=["English"],
                cultural_background="South African"
            ),
            "peter_faucitt": CitizenshipProfile(
                primary_citizenship="South African",
                residency_status=CitizenshipStatus.FULL_CITIZEN,
                tax_residence="South Africa", 
                legal_domicile="South Africa",
                years_of_residence=55,  # Older party
                language_preferences=["English", "Afrikaans"],
                cultural_background="South African"
            )
        }
        
        return profiles
    
    def analyze_settlement_elements(self) -> Dict[str, Any]:
        """Analyze the settlement agreement elements from citizenship perspective"""
        
        settlement_elements = {
            "medical_testing_agreement": {
                "type": SettlementType.PSYCHOLOGICAL,
                "description": "Mandatory psychiatric evaluations and drug testing",
                "citizenship_critical_factors": [
                    "Cultural competency of psychological assessments",
                    "Professional licensing in South African jurisdiction", 
                    "Language rights for evaluations",
                    "Appeal mechanisms available to South African citizens"
                ]
            },
            "forensic_investigation_agreement": {
                "type": SettlementType.COMMERCIAL,
                "description": "Forvis Mazars forensic investigation with attorney-controlled terms",
                "citizenship_critical_factors": [
                    "South African business law compliance",
                    "Cross-border asset investigation rights",
                    "Professional regulation of forensic investigators"
                ]
            },
            "financial_control_mechanisms": {
                "type": SettlementType.COMMERCIAL,
                "description": "Transaction controls and business payment restrictions",
                "citizenship_critical_factors": [
                    "South African banking and financial law",
                    "Constitutional property rights protections",
                    "Commercial law enforcement mechanisms"
                ]
            }
        }
        
        return settlement_elements
    
    def perform_comprehensive_analysis(self) -> Dict[str, Any]:
        """Perform comprehensive integrated analysis"""
        
        profiles = self.create_case_profiles()
        settlement_elements = self.analyze_settlement_elements()
        
        analysis_results = {
            "case_metadata": {
                "case_id": self.case_id,
                "analysis_date": datetime.now().isoformat(),
                "analysis_type": "Integrated Settlement and Citizenship Analysis"
            },
            "party_analyses": {},
            "settlement_element_analyses": {},
            "integrated_findings": {},
            "enhanced_recommendations": []
        }
        
        # Analyze each party
        for party_name, profile in profiles.items():
            party_analysis = {}
            
            # Analyze each settlement type for this party
            for element_name, element_info in settlement_elements.items():
                assessment = self.citizenship_analyzer.analyze_citizenship_impact(
                    profile, element_info["type"]
                )
                
                party_analysis[element_name] = {
                    "impact_level": assessment.citizenship_impact_level,
                    "enforcement_complexity": assessment.enforcement_complexity.value,
                    "enforceable_elements": assessment.enforceable_elements,
                    "unenforceable_elements": assessment.unenforceable_elements,
                    "cultural_considerations": assessment.cultural_considerations,
                    "risk_factors": assessment.risk_factors
                }
            
            analysis_results["party_analyses"][party_name] = party_analysis
        
        # Analyze settlement elements comprehensively
        for element_name, element_info in settlement_elements.items():
            element_analysis = {
                "settlement_type": element_info["type"].value,
                "description": element_info["description"],
                "citizenship_critical_factors": element_info["citizenship_critical_factors"],
                "cross_party_impacts": {}
            }
            
            # Compare impacts across all parties for this settlement element
            for party_name, profile in profiles.items():
                assessment = self.citizenship_analyzer.analyze_citizenship_impact(
                    profile, element_info["type"]
                )
                element_analysis["cross_party_impacts"][party_name] = {
                    "impact_level": assessment.citizenship_impact_level,
                    "enforcement_complexity": assessment.enforcement_complexity.value
                }
            
            analysis_results["settlement_element_analyses"][element_name] = element_analysis
        
        # Generate integrated findings
        analysis_results["integrated_findings"] = self._generate_integrated_findings(
            profiles, settlement_elements, analysis_results
        )
        
        # Generate enhanced recommendations
        analysis_results["enhanced_recommendations"] = self._generate_enhanced_recommendations(
            analysis_results
        )
        
        return analysis_results
    
    def _generate_integrated_findings(self, profiles: Dict[str, CitizenshipProfile], 
                                    settlement_elements: Dict[str, Any],
                                    analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate integrated findings combining settlement and citizenship analysis"""
        
        findings = {
            "citizenship_uniformity": "All parties are South African citizens with full rights",
            "highest_risk_settlement_type": "PSYCHOLOGICAL - due to medical testing provisions",
            "enforcement_advantages": [
                "Uniform South African jurisdiction for all parties",
                "Full domestic legal protections available",
                "Consistent cultural and legal frameworks",
                "No cross-border enforcement complications"
            ],
            "citizenship_specific_vulnerabilities": [
                "Medical testing cultural competency requirements",
                "Professional licensing verification needs",
                "Constitutional rights protections may be bypassed by settlement structure",
                "Appeal mechanisms may be limited by settlement terms"
            ],
            "trojan_horse_citizenship_exploitation": {
                "description": "Settlement exploits citizenship status to create enforceable medical obligations",
                "mechanism": "Uses South African legal system enforceability to compel psychological testing",
                "citizenship_shield_bypass": "Settlement structure bypasses normal citizenship protections"
            }
        }
        
        return findings
    
    def _generate_enhanced_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate enhanced recommendations combining both analysis frameworks"""
        
        recommendations = [
            # Original settlement analysis recommendations
            "Challenge settlement agreements as void due to connection to criminal activity",
            "Include medical testing witness intimidation in criminal investigation",
            "Report unethical medical professional involvement to regulatory bodies",
            "Protect respondents from unlimited financial settlement obligations",
            
            # Enhanced citizenship-aware recommendations
            "Verify cultural competency of all psychological assessment professionals under South African standards",
            "Confirm medical professional licensing in South African jurisdiction",
            "Assert constitutional rights protections available to South African citizens",
            "Leverage uniform South African jurisdiction to challenge cross-element enforceability",
            "Demand language rights compliance for all evaluations and proceedings",
            "Invoke South African appeal mechanisms to challenge settlement validity",
            "Assert that settlement structure violates South African constitutional protections",
            "Use citizenship-based legal protections to challenge coercive medical testing",
            
            # Cross-jurisdictional legal capacity recommendations
            "Assess legal capacity limitations for any foreign citizens involved in settlement",
            "Challenge medical testing clauses that exceed foreign citizens' legal capacity",
            "Separate economic clauses (enforceable) from civic/medical clauses (potentially unenforceable)",
            "Audit settlement language for convoluted inversions that create unintended obligations",
            "Require plain language for all clauses affecting foreign citizens",
            "Include severability provisions to void clauses exceeding legal capacity",
            
            # Strategic integration recommendations  
            "Integrate citizenship rights assertion into overall legal defense strategy",
            "Use South African constitutional law to challenge settlement enforceability",
            "Assert that settlement violates dignity and equality rights of South African citizens",
            "Challenge cultural competency of foreign-influenced assessment standards",
            "Demand South African professional standards compliance for all service providers",
            "Create separate voluntary family agreement for medical testing as private matter",
            "Explicitly exclude medical testing from financial audit agreement scope"
        ]
        
        return recommendations
    
    def generate_case_specific_report(self) -> Dict[str, Any]:
        """Generate a comprehensive case-specific report"""
        
        comprehensive_analysis = self.perform_comprehensive_analysis()
        
        # Add case-specific insights
        case_specific_insights = {
            "british_tax_vote_parallel": {
                "description": "Case demonstrates similar principle to British tax-vote disconnect",
                "parallel": "Parties retain citizenship protections but settlement bypasses civic rights",
                "exploitation_mechanism": "Uses legal enforceability while denying constitutional protections"
            },
            "psychological_vs_commercial_distinction": {
                "finding": "Medical testing (psychological) has CRITICAL citizenship impact vs MODERATE for commercial elements",
                "implication": "Citizenship protections most important for medical testing provisions",
                "strategic_focus": "Challenge psychological settlement elements using citizenship rights"
            },
            "south_african_constitutional_analysis": {
                "relevant_rights": [
                    "Right to dignity (Section 10)",
                    "Right to equality (Section 9)", 
                    "Right to privacy (Section 14)",
                    "Right to healthcare (Section 27)"
                ],
                "settlement_violations": [
                    "Coercive medical testing violates dignity",
                    "Discriminatory treatment violates equality",
                    "Forced psychological evaluation violates privacy",
                    "Weaponized medical testing perverts healthcare rights"
                ]
            }
        }
        
        comprehensive_analysis["case_specific_insights"] = case_specific_insights
        
        return comprehensive_analysis
    
    def save_analysis_report(self, output_path: str = None) -> str:
        """Save the comprehensive analysis report"""
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/tmp/integrated_settlement_citizenship_analysis_{timestamp}.json"
        
        report = self.generate_case_specific_report()
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return output_path


def demonstrate_british_tax_vote_principle():
    """
    Demonstrate how the British tax-vote disconnect principle applies to Case 2025_137857
    """
    
    print("=== BRITISH TAX-VOTE DISCONNECT PRINCIPLE DEMONSTRATION ===")
    print()
    
    analyzer = CitizenshipSettlementAnalyzer()
    
    # Create British permanent resident profile (the classic example)
    british_profile = CitizenshipProfile(
        primary_citizenship="British",
        residency_status=CitizenshipStatus.PERMANENT_RESIDENT,
        tax_residence="UK",
        legal_domicile="UK"
    )
    
    # Analyze civil settlement (covers tax obligations and voting rights)
    british_civil_assessment = analyzer.analyze_citizenship_impact(
        british_profile, SettlementType.CIVIL_PERSONAL
    )
    
    print("BRITISH PERMANENT RESIDENT - CIVIL SETTLEMENT:")
    print(f"  Enforceable Elements: {british_civil_assessment.enforceable_elements}")
    print(f"  Unenforceable Elements: {british_civil_assessment.unenforceable_elements}")
    print()
    
    # Now show the parallel in Case 2025_137857
    print("=== CASE 2025_137857 PARALLEL ===")
    print()
    
    sa_citizen_profile = CitizenshipProfile(
        primary_citizenship="South African",
        residency_status=CitizenshipStatus.FULL_CITIZEN,
        tax_residence="South Africa"
    )
    
    # Analyze psychological settlement (medical testing)
    sa_psychological_assessment = analyzer.analyze_citizenship_impact(
        sa_citizen_profile, SettlementType.PSYCHOLOGICAL
    )
    
    print("SOUTH AFRICAN CITIZEN - PSYCHOLOGICAL SETTLEMENT:")
    print(f"  Enforceable Elements: {sa_psychological_assessment.enforceable_elements}")
    print(f"  Unenforceable Elements: {sa_psychological_assessment.unenforceable_elements}")
    print()
    
    print("=== PARALLEL ANALYSIS ===")
    print("British Case: Can enforce TAX obligations but NOT VOTING rights")
    print("SA Case: Can enforce MEDICAL obligations but NOT CONSTITUTIONAL rights")
    print()
    print("Common Principle: Civic/Constitutional protections separate from legal enforceability")
    print("Strategic Implication: Assert constitutional rights to challenge settlement validity")


if __name__ == "__main__":
    print("Integrated Settlement and Citizenship Analysis for Case 2025_137857")
    print("=" * 70)
    print()
    
    # Demonstrate the British tax-vote principle
    demonstrate_british_tax_vote_principle()
    print()
    
    # Perform comprehensive case analysis
    print("=== COMPREHENSIVE CASE ANALYSIS ===")
    print()
    
    analyzer = IntegratedCaseAnalyzer()
    
    # Generate and save comprehensive report
    report_path = analyzer.save_analysis_report()
    print(f"Comprehensive analysis report saved to: {report_path}")
    
    # Show key findings
    analysis = analyzer.perform_comprehensive_analysis()
    
    print("\nKEY INTEGRATED FINDINGS:")
    for finding, value in analysis["integrated_findings"].items():
        if isinstance(value, str):
            print(f"  {finding}: {value}")
        elif isinstance(value, list):
            print(f"  {finding}:")
            for item in value:
                print(f"    - {item}")
    
    print(f"\nENHANCED RECOMMENDATIONS: {len(analysis['enhanced_recommendations'])} total")
    print("  (See full report for details)")
    
    print("\n" + "=" * 70)
    print("Analysis complete. Use the generated report for legal strategy development.")