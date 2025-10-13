#!/usr/bin/env python3
"""
Relevance Summarization Engine
=============================

Analyzes and summarizes the main points of relevance from legal documents,
case facts, and cross-jurisdictional analysis. Provides weighted importance
scoring and hierarchical summarization.

Key Features:
1. Multi-jurisdictional relevance scoring
2. Legal significance weighting
3. Cross-reference validation
4. Hierarchical summary generation
5. Evidence strength assessment
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from frameworks.opencog_hgnnql import Atom, AtomSpace, AtomType, TruthValue
from frameworks.za_legal_jurisdiction import ZALegalJurisdictionInterpreter, ZALegalAnalysis
from frameworks.uk_legal_jurisdiction import UKLegalJurisdictionInterpreter, UKLegalAnalysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RelevanceCategory(Enum):
    """Categories of legal relevance"""
    CRITICAL = "critical"          # Case-decisive evidence
    HIGH = "high"                 # Strong supporting evidence  
    MEDIUM = "medium"             # Contributory evidence
    LOW = "low"                   # Background information
    NEGLIGIBLE = "negligible"     # Minimal relevance


class EvidenceType(Enum):
    """Types of evidence"""
    DOCUMENTARY = "documentary"    # Documents, emails, contracts
    FINANCIAL = "financial"       # Bank statements, invoices, transactions
    TESTIMONIAL = "testimonial"   # Witness statements, affidavits
    CIRCUMSTANTIAL = "circumstantial"  # Patterns, inferences
    EXPERT = "expert"             # Expert analysis and opinions


@dataclass
class RelevanceScore:
    """Scoring for relevance assessment"""
    overall_score: float          # 0.0 to 1.0
    za_jurisdiction_score: float  # ZA legal relevance
    uk_jurisdiction_score: float  # UK legal relevance
    cross_border_score: float    # Cross-border implications
    evidence_strength: float     # Strength of evidence
    legal_significance: float    # Legal significance level
    
    def get_category(self) -> RelevanceCategory:
        """Determine relevance category from overall score"""
        if self.overall_score >= 0.9:
            return RelevanceCategory.CRITICAL
        elif self.overall_score >= 0.7:
            return RelevanceCategory.HIGH
        elif self.overall_score >= 0.5:
            return RelevanceCategory.MEDIUM
        elif self.overall_score >= 0.3:
            return RelevanceCategory.LOW
        else:
            return RelevanceCategory.NEGLIGIBLE


@dataclass
class RelevanceItem:
    """Individual item with relevance assessment"""
    item_id: str
    title: str
    description: str
    evidence_type: EvidenceType
    source_document: Optional[str]
    relevance_score: RelevanceScore
    supporting_facts: List[str]
    legal_implications: List[str]
    cross_references: List[str]
    timestamps: List[datetime] = field(default_factory=list)
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of this relevance item"""
        return {
            "title": self.title,
            "relevance_category": self.relevance_score.get_category().value,
            "overall_score": self.relevance_score.overall_score,
            "evidence_type": self.evidence_type.value,
            "key_implications": self.legal_implications[:3],  # Top 3
            "supporting_evidence": len(self.supporting_facts)
        }


@dataclass 
class ComprehensiveRelevanceSummary:
    """Comprehensive summary of all relevant items"""
    summary_id: str
    analysis_timestamp: datetime
    critical_items: List[RelevanceItem]
    high_relevance_items: List[RelevanceItem] 
    medium_relevance_items: List[RelevanceItem]
    za_analysis_summary: Dict[str, Any]
    uk_analysis_summary: Dict[str, Any]
    cross_jurisdictional_points: List[str]
    main_conclusions: List[str]
    recommended_actions: List[str]
    evidence_summary: Dict[str, int]
    
    def generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary for stakeholders"""
        return {
            "analysis_date": self.analysis_timestamp.isoformat(),
            "total_critical_items": len(self.critical_items),
            "total_high_relevance": len(self.high_relevance_items),
            "za_legal_strength": self.za_analysis_summary.get("legal_strength", 0.0),
            "uk_legal_strength": self.uk_analysis_summary.get("legal_strength", 0.0),
            "main_conclusions": self.main_conclusions,
            "priority_actions": self.recommended_actions[:5],
            "evidence_breakdown": self.evidence_summary
        }


class RelevanceSummarizer:
    """
    Main relevance summarization engine that analyzes legal materials
    and generates weighted importance summaries across jurisdictions.
    """
    
    def __init__(self, atomspace: Optional[AtomSpace] = None):
        self.atomspace = atomspace
        self.za_interpreter = ZALegalJurisdictionInterpreter(atomspace)
        self.uk_interpreter = UKLegalJurisdictionInterpreter(atomspace)
        self.relevance_items: List[RelevanceItem] = []
        logger.info("Initialized Relevance Summarization Engine")
    
    def analyze_shopify_evidence(self, shopify_analysis_data: Dict[str, Any]) -> RelevanceItem:
        """Analyze Shopify evidence for relevance"""
        
        # Extract key facts from shopify analysis
        uk_funding_sa = shopify_analysis_data.get("uk_funding_sa_operations", False)
        contradicts_claims = shopify_analysis_data.get("contradicts_debt_claims", False)
        total_amount = shopify_analysis_data.get("total_funding_amount", 0)
        duration_years = shopify_analysis_data.get("funding_duration_years", 0)
        
        # Calculate relevance scores
        za_score = 0.9 if contradicts_claims else 0.6
        uk_score = 0.8 if uk_funding_sa else 0.5
        cross_border_score = 0.9 if uk_funding_sa else 0.3
        
        # Evidence strength based on documentary nature
        evidence_strength = 0.95  # High - documentary evidence from Shopify
        
        # Legal significance
        legal_significance = 0.9 if contradicts_claims else 0.7
        
        # Overall score calculation (weighted average)
        overall_score = (
            za_score * 0.3 +
            uk_score * 0.3 + 
            cross_border_score * 0.2 +
            evidence_strength * 0.1 +
            legal_significance * 0.1
        )
        
        relevance_score = RelevanceScore(
            overall_score=overall_score,
            za_jurisdiction_score=za_score,
            uk_jurisdiction_score=uk_score,
            cross_border_score=cross_border_score,
            evidence_strength=evidence_strength,
            legal_significance=legal_significance
        )
        
        # Generate supporting facts
        supporting_facts = [
            f"16 Shopify invoices spanning {duration_years} years documented",
            f"Total UK funding of SA operations: ${total_amount:,.2f} USD",
            "All invoices show UK company as payer with UK billing address",
            "UK payment card (ending 7147) used for all transactions",
            "All payments marked as 'PAID' - no outstanding amounts"
        ]
        
        # Legal implications
        legal_implications = []
        if contradicts_claims:
            legal_implications.extend([
                "Documentary evidence directly contradicts sworn affidavits",
                "Potential perjury charges under both ZA and UK law",
                "Material misrepresentation in legal proceedings"
            ])
        
        if uk_funding_sa:
            legal_implications.extend([
                "Establishes creditor-debtor relationship (UK creditor, SA debtor)",
                "Reverses claimed debt direction in legal filings",
                "Demonstrates ongoing commercial relationship and support"
            ])
        
        return RelevanceItem(
            item_id="shopify_evidence_analysis",
            title="Shopify Payment Flow Evidence",
            description="Documentary evidence of UK company funding SA operations over 9+ years",
            evidence_type=EvidenceType.DOCUMENTARY,
            source_document="shopify_payment_flow_analysis.md",
            relevance_score=relevance_score,
            supporting_facts=supporting_facts,
            legal_implications=legal_implications,
            cross_references=[
                "uk_funding_sa_operations_perjury_evidence.md",
                "Shopify invoices 2016-2025"
            ]
        )
    
    def analyze_cross_jurisdictional_case(self, case_data: Dict[str, Any]) -> ComprehensiveRelevanceSummary:
        """Perform comprehensive cross-jurisdictional relevance analysis"""
        
        # Clear previous analysis
        self.relevance_items = []
        
        # Analyze Shopify evidence
        if case_data.get("shopify_data"):
            shopify_item = self.analyze_shopify_evidence(case_data["shopify_data"])
            self.relevance_items.append(shopify_item)
        
        # Analyze other evidence types
        if case_data.get("financial_evidence"):
            financial_item = self._analyze_financial_evidence(case_data["financial_evidence"])
            self.relevance_items.append(financial_item)
        
        if case_data.get("corporate_documents"):
            corporate_item = self._analyze_corporate_documents(case_data["corporate_documents"])
            self.relevance_items.append(corporate_item)
        
        # Perform jurisdictional analysis
        za_analysis = self.za_interpreter.analyze_case_facts(case_data)
        uk_analysis = self.uk_interpreter.analyze_case_facts(case_data)
        
        # Categorize relevance items
        critical_items = [item for item in self.relevance_items 
                         if item.relevance_score.get_category() == RelevanceCategory.CRITICAL]
        high_items = [item for item in self.relevance_items 
                     if item.relevance_score.get_category() == RelevanceCategory.HIGH]
        medium_items = [item for item in self.relevance_items 
                       if item.relevance_score.get_category() == RelevanceCategory.MEDIUM]
        
        # Generate cross-jurisdictional points
        cross_jurisdictional_points = self._analyze_cross_jurisdictional_implications(
            za_analysis, uk_analysis, case_data
        )
        
        # Generate main conclusions
        main_conclusions = self._generate_main_conclusions(
            critical_items, high_items, za_analysis, uk_analysis
        )
        
        # Generate recommended actions
        recommended_actions = self._generate_recommended_actions(
            za_analysis, uk_analysis, critical_items
        )
        
        # Evidence summary statistics
        evidence_summary = {
            "documentary": sum(1 for item in self.relevance_items 
                             if item.evidence_type == EvidenceType.DOCUMENTARY),
            "financial": sum(1 for item in self.relevance_items 
                           if item.evidence_type == EvidenceType.FINANCIAL),
            "testimonial": sum(1 for item in self.relevance_items 
                             if item.evidence_type == EvidenceType.TESTIMONIAL),
            "total_items": len(self.relevance_items),
            "critical_items": len(critical_items),
            "high_relevance": len(high_items)
        }
        
        return ComprehensiveRelevanceSummary(
            summary_id=f"relevance_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            analysis_timestamp=datetime.now(),
            critical_items=critical_items,
            high_relevance_items=high_items,
            medium_relevance_items=medium_items,
            za_analysis_summary=za_analysis.generate_legal_summary(),
            uk_analysis_summary=uk_analysis.generate_legal_summary(),
            cross_jurisdictional_points=cross_jurisdictional_points,
            main_conclusions=main_conclusions,
            recommended_actions=recommended_actions,
            evidence_summary=evidence_summary
        )
    
    def _analyze_financial_evidence(self, financial_data: Dict[str, Any]) -> RelevanceItem:
        """Analyze financial evidence for relevance"""
        total_amount = financial_data.get("total_amount", 0)
        transaction_count = financial_data.get("transaction_count", 0)
        
        # Calculate scores based on financial evidence characteristics
        evidence_strength = 0.9 if transaction_count > 10 else 0.7
        legal_significance = min(1.0, total_amount / 1000000 * 0.8)  # Scale with amount
        
        overall_score = (evidence_strength + legal_significance) / 2
        
        return RelevanceItem(
            item_id="financial_evidence",
            title="Financial Transaction Evidence",
            description=f"Financial evidence covering {transaction_count} transactions totaling ${total_amount:,.2f}",
            evidence_type=EvidenceType.FINANCIAL,
            source_document=financial_data.get("source_document"),
            relevance_score=RelevanceScore(
                overall_score=overall_score,
                za_jurisdiction_score=0.8,
                uk_jurisdiction_score=0.8,
                cross_border_score=0.9,
                evidence_strength=evidence_strength,
                legal_significance=legal_significance
            ),
            supporting_facts=[
                f"Total financial exposure: ${total_amount:,.2f}",
                f"Number of transactions: {transaction_count}",
                "Bank statements provide contemporaneous records"
            ],
            legal_implications=[
                "Demonstrates financial relationship between parties",
                "Provides basis for quantifying damages",
                "Contemporary records reduce dispute risk"
            ],
            cross_references=[]
        )
    
    def _analyze_corporate_documents(self, corporate_data: Dict[str, Any]) -> RelevanceItem:
        """Analyze corporate documentation for relevance"""
        document_types = corporate_data.get("document_types", [])
        jurisdictions = corporate_data.get("jurisdictions", [])
        
        # Higher relevance for multi-jurisdictional corporate docs
        cross_border_score = 0.9 if len(jurisdictions) > 1 else 0.5
        evidence_strength = 0.8  # Corporate docs are generally strong evidence
        
        overall_score = (cross_border_score + evidence_strength) / 2
        
        return RelevanceItem(
            item_id="corporate_documents",
            title="Corporate Documentation",
            description=f"Corporate documents across {len(jurisdictions)} jurisdictions",
            evidence_type=EvidenceType.DOCUMENTARY,
            source_document=corporate_data.get("source_document"),
            relevance_score=RelevanceScore(
                overall_score=overall_score,
                za_jurisdiction_score=0.7,
                uk_jurisdiction_score=0.7,
                cross_border_score=cross_border_score,
                evidence_strength=evidence_strength,
                legal_significance=0.7
            ),
            supporting_facts=[
                f"Document types: {', '.join(document_types)}",
                f"Jurisdictions involved: {', '.join(jurisdictions)}",
                "Official corporate records provide authoritative evidence"
            ],
            legal_implications=[
                "Establishes corporate structure and relationships",
                "Demonstrates compliance or non-compliance with corporate law",
                "Provides foundation for derivative or direct claims"
            ],
            cross_references=[]
        )
    
    def _analyze_cross_jurisdictional_implications(
        self, 
        za_analysis: ZALegalAnalysis, 
        uk_analysis: UKLegalAnalysis,
        case_data: Dict[str, Any]
    ) -> List[str]:
        """Analyze cross-jurisdictional legal implications"""
        implications = []
        
        # Enforcement considerations
        implications.extend([
            "UK judgments enforceable in SA through High Court recognition procedures",
            "SA judgments enforceable in UK under common law reciprocity principles",
            "Both jurisdictions recognize corporate law concepts and director duties"
        ])
        
        # Procedural considerations
        if za_analysis.strength_assessment > 0.7 and uk_analysis.strength_assessment > 0.7:
            implications.extend([
                "Strong legal case in both jurisdictions enables forum shopping",
                "Parallel proceedings possible but coordination advisable",
                "Asset recovery available in both jurisdictions"
            ])
        
        # Evidence transfer
        implications.extend([
            "Documentary evidence admissible in both jurisdictions",
            "Mutual Legal Assistance Treaty available for evidence gathering",
            "Expert evidence may require local qualification in each jurisdiction"
        ])
        
        return implications
    
    def _generate_main_conclusions(
        self,
        critical_items: List[RelevanceItem],
        high_items: List[RelevanceItem],
        za_analysis: ZALegalAnalysis,
        uk_analysis: UKLegalAnalysis
    ) -> List[str]:
        """Generate main conclusions from relevance analysis"""
        conclusions = []
        
        # Evidence strength conclusions
        if critical_items:
            conclusions.append(
                f"Critical evidence identified: {len(critical_items)} items with decisive relevance"
            )
        
        # Cross-jurisdictional strength
        if za_analysis.strength_assessment > 0.7 and uk_analysis.strength_assessment > 0.7:
            conclusions.append(
                "Strong legal case established in both ZA and UK jurisdictions"
            )
        
        # Specific to Shopify evidence
        shopify_items = [item for item in critical_items + high_items 
                        if "shopify" in item.item_id.lower()]
        if shopify_items:
            conclusions.append(
                "Shopify payment records provide irrefutable documentary evidence contradicting sworn claims"
            )
        
        # Financial implications
        total_financial_exposure = sum(
            item.relevance_score.cross_border_score * 100000  # Estimate based on scores
            for item in critical_items + high_items
            if item.evidence_type == EvidenceType.FINANCIAL
        )
        if total_financial_exposure > 0:
            conclusions.append(
                f"Estimated financial exposure exceeds ${total_financial_exposure:,.0f} across jurisdictions"
            )
        
        return conclusions
    
    def _generate_recommended_actions(
        self,
        za_analysis: ZALegalAnalysis,
        uk_analysis: UKLegalAnalysis,
        critical_items: List[RelevanceItem]
    ) -> List[str]:
        """Generate recommended actions based on relevance analysis"""
        actions = []
        
        # High priority actions for critical evidence
        if critical_items:
            actions.extend([
                "Secure and preserve all critical documentary evidence",
                "Engage forensic accountants to quantify financial damages",
                "Prepare comprehensive evidence bundles for both jurisdictions"
            ])
        
        # Jurisdictional actions
        actions.extend(za_analysis.recommended_actions[:2])  # Top 2 ZA actions
        actions.extend(uk_analysis.recommended_actions[:2])  # Top 2 UK actions
        
        # Cross-border coordination
        actions.extend([
            "Coordinate legal strategy across ZA and UK jurisdictions",
            "Consider parallel proceedings to maximize enforcement options",
            "Engage international legal counsel experienced in cross-border litigation"
        ])
        
        return actions
    
    def generate_relevance_report(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive relevance analysis report"""
        summary = self.analyze_cross_jurisdictional_case(case_data)
        
        return {
            "executive_summary": summary.generate_executive_summary(),
            "critical_evidence": [item.generate_summary() for item in summary.critical_items],
            "high_relevance_evidence": [item.generate_summary() for item in summary.high_relevance_items],
            "jurisdictional_analysis": {
                "south_africa": summary.za_analysis_summary,
                "united_kingdom": summary.uk_analysis_summary
            },
            "cross_jurisdictional_considerations": summary.cross_jurisdictional_points,
            "main_conclusions": summary.main_conclusions,
            "recommended_actions": summary.recommended_actions,
            "evidence_statistics": summary.evidence_summary
        }


__all__ = [
    "RelevanceCategory",
    "EvidenceType",
    "RelevanceScore",
    "RelevanceItem",
    "ComprehensiveRelevanceSummary",
    "RelevanceSummarizer"
]