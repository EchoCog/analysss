#!/usr/bin/env python3
"""
OpenCog HyperGraphQL ORGGML Evidence Refinery
============================================

A comprehensive evidence processing system that combines:
1. OpenCog-style knowledge representation (AtomSpace)
2. HyperGraphQL schema and API integration
3. GGML-optimized inference engine for evidence analysis
4. Evidence quality assessment and refinement algorithms

This module provides a unified interface for evidence management,
quality assessment, and intelligent refinement using multiple AI frameworks.
"""

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np

# Import framework components
from frameworks.opencog_hgnnql import (
    Atom,
    AtomSpace,
    AtomType,
    HGNNQLQueryEngine,
    TruthValue,
)
from frameworks.ggml_legal_engine import (
    GGMLLegalEngine,
    GGMLTensor,
    GGMLTensorType,
)
from src.api.hypergraphql_schema import (
    HyperGraphQLEdge,
    HyperGraphQLNode,
    HyperGraphQLSchema,
    EntityTypeQL,
    RelationTypeQL,
    OrgLevel,
)
from src.api.hypergraphql_resolvers import HyperGraphQLResolver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EvidenceQualityScore(Enum):
    """Evidence quality classification levels"""
    CRITICAL = "critical"        # High-confidence, verifiable evidence
    HIGH = "high"               # Strong evidence with good verification
    MEDIUM = "medium"           # Moderate quality, some verification issues
    LOW = "low"                 # Weak evidence, limited verification
    SPECULATIVE = "speculative" # Unverified or questionable evidence
    INVALID = "invalid"         # Evidence determined to be false/unreliable


class EvidenceProcessingStatus(Enum):
    """Evidence processing pipeline status"""
    PENDING = "pending"
    PROCESSING = "processing"
    ANALYZED = "analyzed"
    REFINED = "refined"
    VALIDATED = "validated"
    REJECTED = "rejected"


@dataclass
class RefinedEvidence:
    """Refined evidence with quality metrics and processing metadata"""
    evidence_id: str
    original_content: str
    refined_content: Optional[str] = None
    quality_score: EvidenceQualityScore = EvidenceQualityScore.MEDIUM
    confidence: float = 0.5
    verification_status: str = "unverified"
    source_reliability: float = 0.5
    corroboration_count: int = 0
    processing_status: EvidenceProcessingStatus = EvidenceProcessingStatus.PENDING
    
    # OpenCog integration
    atom_id: Optional[str] = None
    truth_value: Optional[TruthValue] = None
    
    # HyperGraphQL integration
    graphql_node_id: Optional[str] = None
    related_entities: List[str] = field(default_factory=list)
    
    # GGML analysis results
    ggml_analysis: Optional[Dict[str, Any]] = None
    
    # Processing metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    processing_log: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        result = asdict(self)
        result["quality_score"] = self.quality_score.value
        result["processing_status"] = self.processing_status.value
        result["created_at"] = self.created_at.isoformat()
        result["last_updated"] = self.last_updated.isoformat()
        if self.truth_value:
            result["truth_value"] = self.truth_value.to_dict()
        return result


class OpenCogHyperGraphQLORGGMLEvidenceRefinery:
    """
    Main evidence refinery system integrating multiple AI frameworks.
    
    This class orchestrates evidence processing through:
    1. OpenCog AtomSpace for knowledge representation
    2. HyperGraphQL for API and schema management
    3. GGML for optimized neural inference
    4. Evidence quality assessment algorithms
    """
    
    def __init__(self, case_id: str, output_dir: str = "./evidence_refinery_output"):
        """
        Initialize the evidence refinery system.
        
        Args:
            case_id: Unique identifier for the case
            output_dir: Directory for refined evidence outputs
        """
        self.case_id = case_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize framework components
        self.atomspace = AtomSpace(case_id)
        self.query_engine = HGNNQLQueryEngine(self.atomspace)
        self.ggml_engine = GGMLLegalEngine(quantization_enabled=True)
        self.hypergraphql_schema = HyperGraphQLSchema()
        self.hypergraphql_resolver = HyperGraphQLResolver(self.hypergraphql_schema)
        
        # Evidence storage
        self.refined_evidence: Dict[str, RefinedEvidence] = {}
        self.evidence_relationships: Dict[str, List[str]] = {}
        
        # Processing configuration
        self.quality_thresholds = {
            EvidenceQualityScore.CRITICAL: 0.9,
            EvidenceQualityScore.HIGH: 0.75,
            EvidenceQualityScore.MEDIUM: 0.5,
            EvidenceQualityScore.LOW: 0.25,
            EvidenceQualityScore.SPECULATIVE: 0.1,
        }
        
        logger.info(f"Initialized Evidence Refinery for case: {case_id}")
    
    def add_raw_evidence(self, evidence_id: str, content: str, 
                        source: str = "unknown", 
                        metadata: Optional[Dict[str, Any]] = None) -> RefinedEvidence:
        """
        Add raw evidence to the refinery for processing.
        
        Args:
            evidence_id: Unique identifier for the evidence
            content: Raw evidence content/description
            source: Source of the evidence
            metadata: Additional metadata
        
        Returns:
            RefinedEvidence object for tracking
        """
        logger.info(f"Adding raw evidence: {evidence_id}")
        
        # Create refined evidence object
        refined_evidence = RefinedEvidence(
            evidence_id=evidence_id,
            original_content=content,
            processing_status=EvidenceProcessingStatus.PENDING
        )
        
        # Add processing log entry
        refined_evidence.processing_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": "evidence_added",
            "source": source,
            "metadata": metadata or {}
        })
        
        # Store evidence
        self.refined_evidence[evidence_id] = refined_evidence
        
        # Create OpenCog atom for the evidence
        evidence_atom = Atom(
            atom_id=f"evidence_{evidence_id}",
            atom_type=AtomType.EVIDENCE,
            name=f"Evidence: {content[:100]}...",
            truth_value=TruthValue(strength=0.5, confidence=0.3),  # Initial low confidence
            metadata={
                "evidence_id": evidence_id,
                "source": source,
                "original_content": content,
                "added_timestamp": datetime.now().isoformat()
            }
        )
        
        atom_id = self.atomspace.add_atom(evidence_atom)
        refined_evidence.atom_id = atom_id
        
        # Create HyperGraphQL node
        hypergraphql_node = HyperGraphQLNode(
            id=f"evidence_node_{evidence_id}",
            node_type=EntityTypeQL.EVIDENCE,
            name=f"Evidence {evidence_id}",
            properties={"content": content, "source": source},
            metadata=metadata or {}
        )
        
        self.hypergraphql_schema.add_node(hypergraphql_node)
        refined_evidence.graphql_node_id = hypergraphql_node.id
        
        return refined_evidence
    
    def process_evidence(self, evidence_id: str) -> RefinedEvidence:
        """
        Process raw evidence through the complete refinery pipeline.
        
        Args:
            evidence_id: ID of evidence to process
        
        Returns:
            Processed RefinedEvidence object
        """
        if evidence_id not in self.refined_evidence:
            raise ValueError(f"Evidence not found: {evidence_id}")
        
        evidence = self.refined_evidence[evidence_id]
        logger.info(f"Processing evidence: {evidence_id}")
        
        # Update processing status
        evidence.processing_status = EvidenceProcessingStatus.PROCESSING
        evidence.last_updated = datetime.now()
        
        # Step 1: GGML-based content analysis
        logger.debug(f"Running GGML analysis for evidence: {evidence_id}")
        ggml_results = self._run_ggml_analysis(evidence.original_content)
        evidence.ggml_analysis = ggml_results
        
        # Step 2: Quality assessment
        logger.debug(f"Assessing quality for evidence: {evidence_id}")
        quality_metrics = self._assess_evidence_quality(evidence)
        evidence.quality_score = quality_metrics["score"]
        evidence.confidence = quality_metrics["confidence"]
        evidence.source_reliability = quality_metrics["source_reliability"]
        
        # Step 3: Content refinement
        logger.debug(f"Refining content for evidence: {evidence_id}")
        refined_content = self._refine_evidence_content(evidence)
        evidence.refined_content = refined_content
        
        # Step 4: Update OpenCog atom with refined information
        if evidence.atom_id:
            atom = self.atomspace.get_atom(evidence.atom_id)
            if atom:
                # Update truth value based on quality assessment
                atom.truth_value = TruthValue(
                    strength=evidence.confidence,
                    confidence=min(0.9, evidence.confidence + 0.2)
                )
                evidence.truth_value = atom.truth_value
                
                # Update metadata
                atom.metadata.update({
                    "quality_score": evidence.quality_score.value,
                    "confidence": evidence.confidence,
                    "refined_content": evidence.refined_content,
                    "processed_timestamp": datetime.now().isoformat()
                })
        
        # Step 5: Update HyperGraphQL node
        if evidence.graphql_node_id:
            node = self.hypergraphql_schema.get_node(evidence.graphql_node_id)
            if node:
                node.properties.update({
                    "quality_score": evidence.quality_score.value,
                    "confidence": evidence.confidence,
                    "refined_content": evidence.refined_content
                })
        
        # Update processing status
        evidence.processing_status = EvidenceProcessingStatus.ANALYZED
        evidence.processing_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": "evidence_processed",
            "quality_score": evidence.quality_score.value,
            "confidence": evidence.confidence
        })
        
        logger.info(f"Evidence processing completed: {evidence_id} "
                   f"(Quality: {evidence.quality_score.value}, "
                   f"Confidence: {evidence.confidence:.3f})")
        
        return evidence
    
    def _run_ggml_analysis(self, content: str) -> Dict[str, Any]:
        """Run GGML-based analysis on evidence content"""
        try:
            # Analyze document using GGML legal engine
            analysis = self.ggml_engine.analyze_legal_document(content, "evidence")
            
            # Create evidence tensor for pattern detection
            content_embedding = self.ggml_engine._text_to_embedding(content)
            evidence_tensor = self.ggml_engine.create_tensor(
                name="evidence_content",
                tensor_type=GGMLTensorType.LEGAL_DOCUMENT,
                shape=content_embedding.shape,
                data=content_embedding
            )
            
            # Apply evidence weighting
            weighted_tensor = self.ggml_engine.execute_operator(
                "evidence_weighting", 
                ["evidence_content"]
            )
            
            # Store the weighted tensor for next operation
            self.ggml_engine.tensors[weighted_tensor.name] = weighted_tensor
            
            # Compute relevance scores using stored weighted tensor
            relevance_tensor = self.ggml_engine.execute_operator(
                "relevance_scoring", 
                [weighted_tensor.name]
            )
            
            # Extract results
            relevance_data = (relevance_tensor.dequantize().data 
                            if relevance_tensor.quantized 
                            else relevance_tensor.data)
            
            return {
                "document_analysis": analysis,
                "relevance_score": float(np.mean(relevance_data)),
                "legal_significance": float(np.max(relevance_data)),
                "ggml_optimized": True,
                "processing_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"GGML analysis failed: {str(e)}")
            return {
                "error": str(e),
                "relevance_score": 0.5,
                "legal_significance": 0.5,
                "ggml_optimized": False
            }
    
    def _assess_evidence_quality(self, evidence: RefinedEvidence) -> Dict[str, Any]:
        """Assess evidence quality using multiple criteria"""
        quality_factors = []
        
        # Factor 1: Content analysis from GGML
        ggml_score = 0.5
        if evidence.ggml_analysis:
            ggml_score = evidence.ggml_analysis.get("relevance_score", 0.5)
            quality_factors.append(("ggml_analysis", ggml_score, 0.3))
        
        # Factor 2: Content length and detail
        content_length = len(evidence.original_content)
        length_score = min(1.0, content_length / 500)  # Normalize to 500 chars
        quality_factors.append(("content_detail", length_score, 0.2))
        
        # Factor 3: Presence of specific keywords (legal, financial terms)
        keyword_score = self._calculate_keyword_score(evidence.original_content)
        quality_factors.append(("keyword_relevance", keyword_score, 0.2))
        
        # Factor 4: Source reliability (simplified assessment)
        source_score = 0.7  # Default moderate reliability
        quality_factors.append(("source_reliability", source_score, 0.3))
        
        # Calculate weighted average
        total_weight = sum(weight for _, _, weight in quality_factors)
        weighted_score = sum(score * weight for _, score, weight in quality_factors) / total_weight
        
        # Determine quality classification
        quality_score = EvidenceQualityScore.MEDIUM
        for level, threshold in sorted(self.quality_thresholds.items(), 
                                     key=lambda x: x[1], reverse=True):
            if weighted_score >= threshold:
                quality_score = level
                break
        
        return {
            "score": quality_score,
            "confidence": weighted_score,
            "source_reliability": source_score,
            "quality_factors": quality_factors,
            "assessment_timestamp": datetime.now().isoformat()
        }
    
    def _calculate_keyword_score(self, content: str) -> float:
        """Calculate relevance score based on legal/evidence keywords"""
        evidence_keywords = {
            # Legal terms
            "evidence", "proof", "documentation", "witness", "testimony",
            "contract", "agreement", "legal", "court", "judge",
            # Financial terms  
            "payment", "transaction", "invoice", "bank", "financial",
            "funds", "money", "transfer", "account", "debt",
            # Investigation terms
            "investigation", "fraud", "breach", "fiduciary", "duty",
            "violation", "misconduct", "unauthorized", "control", "access"
        }
        
        content_lower = content.lower()
        words = content_lower.split()
        
        keyword_count = sum(1 for word in words if any(kw in word for kw in evidence_keywords))
        
        if not words:
            return 0.0
        
        keyword_density = keyword_count / len(words)
        return min(1.0, keyword_density * 10)  # Scale up and cap at 1.0
    
    def _refine_evidence_content(self, evidence: RefinedEvidence) -> str:
        """Refine evidence content based on quality assessment"""
        content = evidence.original_content
        
        # Basic content refinement (in practice, would use NLP/LLM)
        refinements = []
        
        # Add quality assessment summary
        refinements.append(f"[Quality: {evidence.quality_score.value.upper()}]")
        refinements.append(f"[Confidence: {evidence.confidence:.2f}]")
        
        # Add GGML insights if available
        if evidence.ggml_analysis:
            legal_sig = evidence.ggml_analysis.get("legal_significance", 0)
            if legal_sig > 0.7:
                refinements.append("[HIGH LEGAL SIGNIFICANCE]")
            
            relevance = evidence.ggml_analysis.get("relevance_score", 0)
            refinements.append(f"[Relevance: {relevance:.2f}]")
        
        # Combine original content with refinements
        refined = " ".join(refinements) + "\n\n" + content
        
        return refined
    
    def find_related_evidence(self, evidence_id: str, 
                            similarity_threshold: float = 0.7) -> List[str]:
        """Find evidence related to the given evidence using OpenCog queries"""
        if evidence_id not in self.refined_evidence:
            return []
        
        evidence = self.refined_evidence[evidence_id]
        if not evidence.atom_id:
            return []
        
        # Use HGNNQL to find connected evidence
        query = f"QUERY CONNECTED TO {evidence.atom_id}"
        result = self.query_engine.execute_hgnnql(query)
        
        related_ids = []
        if result.get("status") == "success":
            for connected_atom in result.get("connected_atoms", []):
                if connected_atom.get("atom_type") == "evidence":
                    # Extract evidence ID from metadata
                    metadata = connected_atom.get("metadata", {})
                    related_evidence_id = metadata.get("evidence_id")
                    if related_evidence_id and related_evidence_id != evidence_id:
                        related_ids.append(related_evidence_id)
        
        return related_ids
    
    def create_evidence_relationship(self, source_id: str, target_id: str,
                                   relationship_type: str = "related_to",
                                   strength: float = 0.8) -> bool:
        """Create relationship between two evidence items"""
        if source_id not in self.refined_evidence or target_id not in self.refined_evidence:
            return False
        
        source_evidence = self.refined_evidence[source_id]
        target_evidence = self.refined_evidence[target_id]
        
        # Create OpenCog relationship
        if source_evidence.atom_id and target_evidence.atom_id:
            link_id = self.atomspace.add_link(
                link_type=AtomType.RELATIONSHIP,
                name=f"{relationship_type}: {source_id} -> {target_id}",
                targets=[source_evidence.atom_id, target_evidence.atom_id],
                truth_value=TruthValue(strength=strength, confidence=0.8)
            )
        
        # Create HyperGraphQL edge
        if source_evidence.graphql_node_id and target_evidence.graphql_node_id:
            edge = HyperGraphQLEdge(
                id=f"evidence_relation_{source_id}_{target_id}",
                edge_type=RelationTypeQL.RELATED_TO,
                source_id=source_evidence.graphql_node_id,
                target_ids=[target_evidence.graphql_node_id],
                strength=strength,
                properties={"relationship_type": relationship_type},
                metadata={"created_timestamp": datetime.now().isoformat()}
            )
            self.hypergraphql_schema.add_edge(edge)
        
        # Update local relationship tracking
        if source_id not in self.evidence_relationships:
            self.evidence_relationships[source_id] = []
        self.evidence_relationships[source_id].append(target_id)
        
        logger.info(f"Created evidence relationship: {source_id} -> {target_id} ({relationship_type})")
        return True
    
    def get_evidence_summary(self, evidence_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of processed evidence"""
        if evidence_id not in self.refined_evidence:
            return {"error": "Evidence not found"}
        
        evidence = self.refined_evidence[evidence_id]
        related_evidence = self.find_related_evidence(evidence_id)
        
        return {
            "evidence_id": evidence_id,
            "quality_score": evidence.quality_score.value,
            "confidence": evidence.confidence,
            "processing_status": evidence.processing_status.value,
            "verification_status": evidence.verification_status,
            "source_reliability": evidence.source_reliability,
            "original_content_length": len(evidence.original_content),
            "refined_content_available": evidence.refined_content is not None,
            "related_evidence_count": len(related_evidence),
            "related_evidence": related_evidence,
            "opencog_atom_id": evidence.atom_id,
            "hypergraphql_node_id": evidence.graphql_node_id,
            "ggml_analysis_available": evidence.ggml_analysis is not None,
            "created_at": evidence.created_at.isoformat(),
            "last_updated": evidence.last_updated.isoformat(),
            "processing_steps": len(evidence.processing_log)
        }
    
    def get_evidence_summary_graphql(self, evidence_id: str) -> Dict[str, Any]:
        """Get evidence summary formatted for GraphQL (camelCase keys)"""
        if evidence_id not in self.refined_evidence:
            return {"error": "Evidence not found"}
        
        evidence = self.refined_evidence[evidence_id]
        related_evidence = self.find_related_evidence(evidence_id)
        
        return {
            "evidenceId": evidence_id,
            "qualityScore": evidence.quality_score.value,
            "confidence": evidence.confidence,
            "processingStatus": evidence.processing_status.value,
            "verificationStatus": evidence.verification_status,
            "sourceReliability": evidence.source_reliability,
            "originalContentLength": len(evidence.original_content),
            "refinedContentAvailable": evidence.refined_content is not None,
            "relatedEvidenceCount": len(related_evidence),
            "relatedEvidence": related_evidence,
            "openCogAtomId": evidence.atom_id,
            "hyperGraphQLNodeId": evidence.graphql_node_id,
            "ggmlAnalysisAvailable": evidence.ggml_analysis is not None,
            "createdAt": evidence.created_at.isoformat(),
            "lastUpdated": evidence.last_updated.isoformat(),
            "processingSteps": len(evidence.processing_log)
        }
    
    def export_refined_evidence(self, output_format: str = "json") -> str:
        """Export all refined evidence to specified format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format.lower() == "json":
            filename = f"refined_evidence_{self.case_id}_{timestamp}.json"
            filepath = self.output_dir / filename
            
            export_data = {
                "case_id": self.case_id,
                "export_timestamp": datetime.now().isoformat(),
                "total_evidence_count": len(self.refined_evidence),
                "evidence": {eid: evidence.to_dict() 
                           for eid, evidence in self.refined_evidence.items()},
                "relationships": self.evidence_relationships,
                "processing_summary": self.get_processing_summary()
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
                
            logger.info(f"Exported refined evidence to: {filepath}")
            return str(filepath)
        
        else:
            raise ValueError(f"Unsupported export format: {output_format}")
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of evidence processing statistics"""
        if not self.refined_evidence:
            return {"total_evidence": 0}
        
        quality_distribution = {}
        status_distribution = {}
        total_confidence = 0
        
        for evidence in self.refined_evidence.values():
            # Quality distribution
            quality = evidence.quality_score.value
            quality_distribution[quality] = quality_distribution.get(quality, 0) + 1
            
            # Status distribution
            status = evidence.processing_status.value
            status_distribution[status] = status_distribution.get(status, 0) + 1
            
            # Confidence tracking
            total_confidence += evidence.confidence
        
        avg_confidence = total_confidence / len(self.refined_evidence)
        
        # Count relationships
        total_relationships = sum(len(rels) for rels in self.evidence_relationships.values())
        
        return {
            "total_evidence": len(self.refined_evidence),
            "quality_distribution": quality_distribution,
            "status_distribution": status_distribution,
            "average_confidence": avg_confidence,
            "total_relationships": total_relationships,
            "atomspace_size": len(self.atomspace.atoms),
            "hypergraphql_nodes": len(self.hypergraphql_schema.nodes),
            "hypergraphql_edges": len(self.hypergraphql_schema.edges),
            "ggml_performance": self.ggml_engine.get_performance_stats()
        }


# Export main class for use in other modules
__all__ = [
    "OpenCogHyperGraphQLORGGMLEvidenceRefinery",
    "RefinedEvidence",
    "EvidenceQualityScore", 
    "EvidenceProcessingStatus"
]