"""
Evidence Automation Module

This module provides automated evidence processing capabilities for the
rzonedevops/analysis repository, including entity extraction, timeline
integration, and evidence folder management.
"""

from .analyzers import EntityAnalyzer, LegalAnalyzer, TimelineAnalyzer
from .extractors import DocumentExtractor, EmailExtractor, HTMLExtractor
from .processor import EvidenceProcessor

__all__ = [
    "EvidenceProcessor",
    "DocumentExtractor",
    "HTMLExtractor",
    "EmailExtractor",
    "EntityAnalyzer",
    "TimelineAnalyzer",
    "LegalAnalyzer",
]

__version__ = "1.0.0"
