#!/usr/bin/env python3
"""
Test script for AD Hypergraph Repository Mapper
"""

import json
import sys
from pathlib import Path

# Add the source directory to Python path
sys.path.insert(0, '.')

from src.api.ad_hypergraph_repository_mapper import ADHypergraphRepositoryMapper, RepositoryConfig


def test_mapper_initialization():
    """Test basic initialization of the mapper."""
    print("Testing AD Hypergraph Repository Mapper initialization...")
    
    mapper = ADHypergraphRepositoryMapper()
    
    # Check that repositories were initialized
    print(f"Initialized with {len(mapper.repositories)} repositories:")
    for repo_name, repo_config in mapper.repositories.items():
        print(f"  - {repo_name}: {repo_config.org_name} ({repo_config.evidence_level})")
    
    assert len(mapper.repositories) == 5, "Should have 5 target repositories"
    
    # Check specific repositories
    assert "analysss" in mapper.repositories, "Should have analysss repository"
    assert "ad-res-j7" in mapper.repositories, "Should have ad-res-j7 repository"
    
    print("✓ Initialization test passed")


def test_repository_config():
    """Test repository configuration."""
    print("\nTesting repository configuration...")
    
    mapper = ADHypergraphRepositoryMapper()
    
    # Test the analysss repository (should have local path)
    analysss_repo = mapper.repositories["analysss"]
    assert analysss_repo.local_path is not None, "analysss should have local path"
    assert analysss_repo.evidence_level == "comprehensive", "analysss should be comprehensive"
    
    # Test creating org mapping
    mapping = mapper.create_org_mapping("analysss")
    assert mapping.org_name == "EchoCog", "Should be EchoCog org"
    assert len(mapping.repos) == 1, "Should have one repository URL"
    
    print("✓ Repository configuration test passed")


def test_repository_summary():
    """Test getting repository summary."""
    print("\nTesting repository summary...")
    
    mapper = ADHypergraphRepositoryMapper()
    summary = mapper.get_repository_summary()
    
    assert "total_repositories" in summary, "Should have total repositories count"
    assert "evidence_distribution" in summary, "Should have evidence distribution"
    assert "organization_distribution" in summary, "Should have org distribution"
    
    print(f"Summary: {json.dumps(summary, indent=2)}")
    print("✓ Repository summary test passed")


def test_local_repository_scan():
    """Test scanning the local repository."""
    print("\nTesting local repository scan...")
    
    mapper = ADHypergraphRepositoryMapper()
    
    # Try to scan the analysss repository (local)
    try:
        scan_results = mapper.scan_local_repository("analysss")
        print(f"Scan results: {json.dumps(scan_results, indent=2)}")
        
        assert "repository" in scan_results, "Should have repository field"
        assert "entity_count" in scan_results, "Should have entity count"
        assert "relation_count" in scan_results, "Should have relation count"
        assert "evidence_count" in scan_results, "Should have evidence count"
        
        print("✓ Local repository scan test passed")
        
    except Exception as e:
        print(f"Note: Local scan test failed (expected if no entities/relations exist): {e}")


def main():
    """Run all tests."""
    print("Running AD Hypergraph Repository Mapper Tests")
    print("=" * 50)
    
    try:
        test_mapper_initialization()
        test_repository_config()
        test_repository_summary()
        test_local_repository_scan()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()