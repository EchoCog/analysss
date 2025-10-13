#!/usr/bin/env python3
"""
Unified Legal Analysis Framework
===============================

Integrates ZA/UK legal jurisdiction interpreters, relevance summarization,
and GGML engines for comprehensive cross-jurisdictional legal analysis.

This module provides a unified interface for:
1. Cross-jurisdictional legal interpretation (ZA and UK)
2. Relevance scoring and summarization
3. GGML-optimized inference for legal pattern recognition
4. Comprehensive legal analysis reporting
"""

import logging
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from pathlib import Path
from frameworks.opencog_hgnnql import AtomSpace
from frameworks.za_legal_jurisdiction import ZALegalJurisdictionInterpreter, ZALegalAnalysis
from frameworks.uk_legal_jurisdiction import UKLegalJurisdictionInterpreter, UKLegalAnalysis  
from frameworks.relevance_summarizer import RelevanceSummarizer, ComprehensiveRelevanceSummary
from frameworks.ggml_legal_engine import GGMLLegalEngine, GGMLTensorType
from frameworks.hyper_holmes_inference import HyperHolmesInferenceEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class UnifiedLegalAnalysisResult:
    """Comprehensive result of unified legal analysis"""
    analysis_id: str
    analysis_timestamp: datetime
    
    # Jurisdictional analyses
    za_analysis: ZALegalAnalysis
    uk_analysis: UKLegalAnalysis
    
    # Relevance analysis
    relevance_summary: ComprehensiveRelevanceSummary
    
    # GGML analysis results
    ggml_document_analysis: Dict[str, Any]
    ggml_cross_jurisdictional: Dict[str, Any]
    ggml_fraud_detection: Dict[str, Any]
    
    # Integrated findings
    overall_legal_strength: float
    recommended_jurisdiction: str
    priority_actions: List[str]
    risk_assessment: Dict[str, float]
    
    def generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary for stakeholders"""
        return {
            "analysis_id": self.analysis_id,
            "analysis_date": self.analysis_timestamp.isoformat(),
            "overall_legal_strength": self.overall_legal_strength,
            "recommended_jurisdiction": self.recommended_jurisdiction,
            "za_strength": self.za_analysis.strength_assessment,
            "uk_strength": self.uk_analysis.strength_assessment,
            "critical_evidence_items": len(self.relevance_summary.critical_items),
            "fraud_risk_detected": self.ggml_fraud_detection.get("fraud_detected", False),
            "priority_actions": self.priority_actions[:5],
            "risk_scores": self.risk_assessment
        }
    
    def generate_detailed_report(self) -> Dict[str, Any]:
        """Generate comprehensive detailed report"""
        return {
            "executive_summary": self.generate_executive_summary(),
            "jurisdictional_analysis": {
                "south_africa": self.za_analysis.generate_legal_summary(),
                "united_kingdom": self.uk_analysis.generate_legal_summary()
            },
            "relevance_analysis": self.relevance_summary.generate_executive_summary(),
            "ggml_analysis": {
                "document_analysis": self.ggml_document_analysis,
                "cross_jurisdictional": self.ggml_cross_jurisdictional,
                "fraud_detection": self.ggml_fraud_detection
            },
            "integrated_findings": {
                "overall_strength": self.overall_legal_strength,
                "recommended_approach": self.recommended_jurisdiction,
                "risk_assessment": self.risk_assessment
            },
            "actionable_recommendations": self.priority_actions
        }


class UnifiedLegalAnalysisFramework:
    """
    Main unified framework integrating all legal analysis components.
    Provides comprehensive cross-jurisdictional legal analysis capabilities.
    """
    
    def __init__(self, 
                 atomspace: Optional[AtomSpace] = None,
                 enable_ggml: bool = True,
                 ggml_quantization: bool = True):
        
        # Initialize core components
        self.atomspace = atomspace or AtomSpace("unified_legal_analysis")
        
        # Initialize legal jurisdiction interpreters
        self.za_interpreter = ZALegalJurisdictionInterpreter(self.atomspace)
        self.uk_interpreter = UKLegalJurisdictionInterpreter(self.atomspace)
        
        # Initialize relevance summarizer
        self.relevance_summarizer = RelevanceSummarizer(self.atomspace)
        
        # Initialize GGML engine if enabled
        self.ggml_enabled = enable_ggml
        if enable_ggml:
            self.ggml_engine = GGMLLegalEngine(
                quantization_enabled=ggml_quantization,
                quantization_bits=8
            )
        
        # Initialize inference engine
        self.inference_engine = HyperHolmesInferenceEngine(self.atomspace)
        
        # Add jurisdiction-specific inference rules
        self._integrate_jurisdictional_rules()
        
        logger.info("Initialized Unified Legal Analysis Framework")
    
    def _integrate_jurisdictional_rules(self):
        """Integrate jurisdiction-specific inference rules"""
        # Add ZA rules
        za_rules = self.za_interpreter.get_inference_rules()
        for rule in za_rules:
            self.inference_engine.add_rule(rule)
        
        # Add UK rules  
        uk_rules = self.uk_interpreter.get_inference_rules()
        for rule in uk_rules:
            self.inference_engine.add_rule(rule)
        
        logger.info(f"Integrated {len(za_rules + uk_rules)} jurisdictional inference rules")
    
    def analyze_shopify_case(self, shopify_data: Dict[str, Any], 
                           additional_evidence: Optional[Dict[str, Any]] = None) -> UnifiedLegalAnalysisResult:
        """
        Perform comprehensive analysis of the Shopify payment case.
        Integrates all analysis components for complete assessment.
        """
        
        analysis_id = f"unified_shopify_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Starting unified Shopify case analysis: {analysis_id}")
        
        # Prepare case facts for jurisdictional analysis
        case_facts = self._extract_case_facts_from_shopify(shopify_data)
        if additional_evidence:
            case_facts.update(additional_evidence)
        
        # Perform jurisdictional analyses
        za_analysis = self.za_interpreter.analyze_case_facts(case_facts)
        uk_analysis = self.uk_interpreter.analyze_case_facts(case_facts)
        
        # Perform relevance analysis
        relevance_case_data = {
            "shopify_data": shopify_data,
            "financial_evidence": case_facts.get("financial_evidence"),
            "corporate_documents": case_facts.get("corporate_documents")
        }
        relevance_summary = self.relevance_summarizer.analyze_cross_jurisdictional_case(relevance_case_data)
        
        # Perform GGML analyses if enabled
        ggml_results = {}
        if self.ggml_enabled:
            ggml_results = self._perform_ggml_analysis(shopify_data, case_facts)
        
        # Calculate overall legal strength
        overall_strength = self._calculate_overall_strength(za_analysis, uk_analysis, relevance_summary, ggml_results)
        
        # Determine recommended jurisdiction
        recommended_jurisdiction = self._determine_recommended_jurisdiction(za_analysis, uk_analysis, case_facts)
        
        # Generate priority actions
        priority_actions = self._generate_priority_actions(za_analysis, uk_analysis, relevance_summary)
        
        # Perform risk assessment
        risk_assessment = self._assess_risks(za_analysis, uk_analysis, ggml_results)
        
        return UnifiedLegalAnalysisResult(
            analysis_id=analysis_id,
            analysis_timestamp=datetime.now(),
            za_analysis=za_analysis,
            uk_analysis=uk_analysis,
            relevance_summary=relevance_summary,
            ggml_document_analysis=ggml_results.get("document_analysis", {}),
            ggml_cross_jurisdictional=ggml_results.get("cross_jurisdictional", {}),
            ggml_fraud_detection=ggml_results.get("fraud_detection", {}),
            overall_legal_strength=overall_strength,
            recommended_jurisdiction=recommended_jurisdiction,
            priority_actions=priority_actions,
            risk_assessment=risk_assessment
        )
    
    def _extract_case_facts_from_shopify(self, shopify_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured case facts from Shopify data"""
        return {
            "multiple_jurisdictions": True,
            "uk_company_involved": True,
            "sa_company_involved": True,
            "financial_amount": shopify_data.get("total_funding_amount", 0),
            "director_relationship": True,
            "fraudulent_activity": shopify_data.get("contradicts_debt_claims", False),
            "uk_funding_sa": shopify_data.get("uk_funding_sa_operations", False),
            "contradicts_sworn_statements": shopify_data.get("contradicts_debt_claims", False),
            "documentary_evidence": True,
            "cross_border": True
        }
    
    def _perform_ggml_analysis(self, shopify_data: Dict[str, Any], case_facts: Dict[str, Any]) -> Dict[str, Any]:
        """Perform GGML-based analysis"""
        results = {}
        
        # Document analysis
        shopify_text = self._shopify_data_to_text(shopify_data)
        results["document_analysis"] = self.ggml_engine.analyze_legal_document(
            shopify_text, "financial_evidence"
        )
        
        # Cross-jurisdictional analysis
        za_features = self._extract_za_features(case_facts)
        uk_features = self._extract_uk_features(case_facts)
        results["cross_jurisdictional"] = self.ggml_engine.cross_jurisdictional_analysis(
            za_features, uk_features
        )
        
        # Fraud pattern detection
        document_features = self._extract_document_features(shopify_data)
        fraud_patterns = self._get_known_fraud_patterns()
        results["fraud_detection"] = self.ggml_engine.detect_fraud_patterns(
            document_features, fraud_patterns
        )
        
        return results
    
    def _shopify_data_to_text(self, shopify_data: Dict[str, Any]) -> str:
        """Convert Shopify data to text for GGML analysis"""
        text_parts = []
        
        if shopify_data.get("uk_funding_sa_operations"):
            text_parts.append("UK company funding South African operations documented through payment records")
        
        if shopify_data.get("contradicts_debt_claims"):
            text_parts.append("Payment evidence contradicts sworn debt claims in legal proceedings")
        
        if shopify_data.get("total_funding_amount"):
            amount = shopify_data["total_funding_amount"]
            text_parts.append(f"Total financial amount involved: ${amount:,.2f}")
        
        text_parts.extend([
            "Documentary evidence from Shopify payment platform",
            "Multi-year payment history showing consistent pattern",
            "Cross-border commercial relationship established"
        ])
        
        return " ".join(text_parts)
    
    def _extract_za_features(self, case_facts: Dict[str, Any]) -> np.ndarray:
        """Extract ZA-relevant features for GGML analysis"""
        features = np.array([
            float(case_facts.get("fraudulent_activity", False)),
            float(case_facts.get("director_relationship", False)),
            min(1.0, case_facts.get("financial_amount", 0) / 1000000),  # Normalize to millions
            float(case_facts.get("cross_border", False)),
            float(case_facts.get("documentary_evidence", False)),
            0.8  # ZA jurisdiction applicability
        ], dtype=np.float32)
        
        return features
    
    def _extract_uk_features(self, case_facts: Dict[str, Any]) -> np.ndarray:
        """Extract UK-relevant features for GGML analysis"""
        features = np.array([
            float(case_facts.get("uk_company_involved", False)),
            float(case_facts.get("director_relationship", False)),
            min(1.0, case_facts.get("financial_amount", 0) / 1000000),  # Normalize to millions
            float(case_facts.get("cross_border", False)),
            float(case_facts.get("fraudulent_activity", False)),
            0.9  # UK jurisdiction applicability (stronger due to UK company involvement)
        ], dtype=np.float32)
        
        return features
    
    def _extract_document_features(self, shopify_data: Dict[str, Any]) -> np.ndarray:
        """Extract document features for fraud detection"""
        features = np.array([
            float(shopify_data.get("contradicts_debt_claims", False)),
            float(shopify_data.get("uk_funding_sa_operations", False)),
            min(1.0, shopify_data.get("funding_duration_years", 0) / 10),  # Normalize to decade
            float(shopify_data.get("invoice_count", 0) / 20),  # Normalize invoice count
            0.95,  # Documentary evidence strength
            0.8   # Pattern consistency
        ], dtype=np.float32)
        
        return features
    
    def _get_known_fraud_patterns(self) -> List[np.ndarray]:
        """Get known fraud patterns for detection"""
        # Pattern 1: False debt claims
        pattern1 = np.array([1.0, 0.8, 0.9, 0.7, 0.6, 0.8], dtype=np.float32)
        
        # Pattern 2: Cross-border financial manipulation
        pattern2 = np.array([0.9, 1.0, 0.8, 0.9, 0.7, 0.9], dtype=np.float32)
        
        # Pattern 3: Documentary evidence contradiction
        pattern3 = np.array([1.0, 0.7, 0.6, 0.5, 0.95, 0.9], dtype=np.float32)
        
        return [pattern1, pattern2, pattern3]
    
    def _calculate_overall_strength(self, za_analysis: ZALegalAnalysis, uk_analysis: UKLegalAnalysis,
                                  relevance_summary: ComprehensiveRelevanceSummary,
                                  ggml_results: Dict[str, Any]) -> float:
        """Calculate overall legal case strength"""
        weights = {
            "za_strength": 0.25,
            "uk_strength": 0.25, 
            "relevance_critical": 0.2,
            "ggml_document": 0.15,
            "ggml_fraud": 0.15
        }
        
        za_strength = za_analysis.strength_assessment
        uk_strength = uk_analysis.strength_assessment
        
        # Relevance strength based on critical items
        if relevance_summary:
            relevance_strength = min(1.0, len(relevance_summary.critical_items) * 0.3)
        else:
            relevance_strength = 0.5  # Default value if no relevance summary
        
        # GGML contributions
        ggml_doc_strength = ggml_results.get("document_analysis", {}).get("relevance_score", 0.0)
        ggml_fraud_strength = 1.0 if ggml_results.get("fraud_detection", {}).get("fraud_detected", False) else 0.5
        
        overall_strength = (
            za_strength * weights["za_strength"] +
            uk_strength * weights["uk_strength"] +
            relevance_strength * weights["relevance_critical"] +
            ggml_doc_strength * weights["ggml_document"] +
            ggml_fraud_strength * weights["ggml_fraud"]
        )
        
        return min(1.0, overall_strength)
    
    def _determine_recommended_jurisdiction(self, za_analysis: ZALegalAnalysis, uk_analysis: UKLegalAnalysis,
                                         case_facts: Dict[str, Any]) -> str:
        """Determine recommended primary jurisdiction"""
        za_strength = za_analysis.strength_assessment
        uk_strength = uk_analysis.strength_assessment
        
        # Factor in practical considerations
        if case_facts.get("uk_company_involved") and uk_strength > 0.7:
            if za_strength > 0.8:
                return "parallel_proceedings"  # Strong in both
            else:
                return "uk_primary"
        elif za_strength > uk_strength + 0.1:
            return "za_primary"
        elif uk_strength > za_strength + 0.1:
            return "uk_primary"
        else:
            return "parallel_proceedings"
    
    def _generate_priority_actions(self, za_analysis: ZALegalAnalysis, uk_analysis: UKLegalAnalysis,
                                 relevance_summary: ComprehensiveRelevanceSummary) -> List[str]:
        """Generate priority actions based on integrated analysis"""
        actions = []
        
        # Critical evidence preservation
        if relevance_summary.critical_items:
            actions.append("URGENT: Secure and preserve all critical documentary evidence")
        
        # High-impact jurisdictional actions
        if za_analysis.strength_assessment > 0.8:
            actions.extend(za_analysis.recommended_actions[:2])
        
        if uk_analysis.strength_assessment > 0.8:
            actions.extend(uk_analysis.recommended_actions[:2])
        
        # Cross-jurisdictional coordination
        actions.extend([
            "Engage experienced cross-border litigation counsel",
            "Coordinate legal strategy across ZA and UK jurisdictions",
            "Prepare comprehensive evidence bundles for both jurisdictions"
        ])
        
        return actions[:10]  # Top 10 priority actions
    
    def _assess_risks(self, za_analysis: ZALegalAnalysis, uk_analysis: UKLegalAnalysis,
                     ggml_results: Dict[str, Any]) -> Dict[str, float]:
        """Assess various legal and procedural risks"""
        return {
            "enforcement_risk": 1.0 - min(za_analysis.strength_assessment, uk_analysis.strength_assessment),
            "evidence_challenge_risk": 1.0 - ggml_results.get("document_analysis", {}).get("evidence_strength", 0.8),
            "jurisdictional_conflict_risk": abs(za_analysis.strength_assessment - uk_analysis.strength_assessment),
            "fraud_detection_confidence": ggml_results.get("fraud_detection", {}).get("confidence_score", 0.0),
            "overall_case_risk": 1.0 - self._calculate_overall_strength(za_analysis, uk_analysis, None, ggml_results)
        }
    
    def interpret_shopify_evidence_comprehensive(self, shopify_file_path: str) -> Dict[str, Any]:
        """Comprehensive interpretation of Shopify evidence file"""
        # This would read and parse the actual Shopify evidence file
        # For now, return structured interpretation based on the analysis document
        
        shopify_interpretation = {
            "za_jurisdiction": self.za_interpreter.interpret_shopify_evidence({
                "uk_funding_sa": True,
                "contradicts_sworn_statements": True
            }),
            "uk_jurisdiction": self.uk_interpreter.interpret_shopify_evidence({
                "uk_company_payments": True,
                "international_elements": True
            }),
            "unified_assessment": {
                "evidence_type": "documentary",
                "strength_rating": "critical",
                "cross_border_implications": True,
                "contradicts_opposing_claims": True,
                "quantifiable_amounts": True
            }
        }
        
        return shopify_interpretation


__all__ = [
    "UnifiedLegalAnalysisResult",
    "UnifiedLegalAnalysisFramework"
]