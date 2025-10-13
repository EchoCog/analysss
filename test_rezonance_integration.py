#!/usr/bin/env python3
"""
Test script for the ReZonance case integration.
"""

import os
import json
from src.cases.rezonance_case import ReZonanceCaseAnalyzer
from src.fraud_analysis import create_rezonance_fraud_analyzer

def test_case_analyzer():
    """Test the ReZonance case analyzer."""
    print("Testing ReZonance case analyzer...")
    
    analyzer = ReZonanceCaseAnalyzer()
    analyzer.load_entities()
    analyzer.load_timeline_events()
    analyzer.analyze_financial_patterns()
    
    print(f"Loaded {len(analyzer.entities)} entities")
    print(f"Loaded {len(analyzer.timeline_events)} timeline events")
    
    # Export to JSON
    output_file = "test_rezonance_case.json"
    analyzer.export_to_json(output_file)
    print(f"Exported case data to {output_file}")
    
    # Verify the file exists
    assert os.path.exists(output_file), f"Output file {output_file} not found"
    
    # Load and verify the data
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    assert data["case_id"] == "rezonance_2017_2025", "Incorrect case ID"
    assert len(data["entities"]) > 0, "No entities found"
    assert len(data["timeline_events"]) > 0, "No timeline events found"
    
    print("ReZonance case analyzer test passed!")
    
def test_fraud_analyzer():
    """Test the ReZonance fraud analyzer."""
    print("\nTesting ReZonance fraud analyzer...")
    
    analyzer = create_rezonance_fraud_analyzer()
    
    # Generate criminal profile
    profile = analyzer.generate_criminal_profile("Rynette Farrar")
    print(f"Generated criminal profile for {profile['primary_suspect']}")
    
    # Calculate damages
    damages = analyzer.calculate_damages()
    print(f"Total damages: R{damages['total_damages_claim']:,.2f}")
    
    # Export to JSON
    output_file = "test_rezonance_fraud.json"
    analyzer.export_fraud_analysis(output_file)
    print(f"Exported fraud analysis to {output_file}")
    
    # Verify the file exists
    assert os.path.exists(output_file), f"Output file {output_file} not found"
    
    # Load and verify the data
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    assert data["case_id"] == "rezonance_2017_2025", "Incorrect case ID"
    assert "fraud_pattern_analysis" in data, "No fraud pattern analysis found"
    assert "criminal_profiles" in data, "No criminal profiles found"
    
    print("ReZonance fraud analyzer test passed!")

if __name__ == "__main__":
    test_case_analyzer()
    test_fraud_analyzer()
    print("\nAll tests passed!")
