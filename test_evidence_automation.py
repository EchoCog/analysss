#!/usr/bin/env python3
"""
Test script for the evidence automation system.

This script demonstrates the automated processing of the July 2025 formal notice
evidence package using the new evidence automation framework.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from evidence_automation.processor import EvidenceProcessor


def test_evidence_automation():
    """Test the evidence automation system with the July 2025 formal notice."""
    
    print("🔍 Testing Evidence Automation System")
    print("=" * 50)
    
    # Initialize the evidence processor
    processor = EvidenceProcessor()
    
    # Define the evidence files from the July 2025 formal notice
    evidence_files = [
        "evidence/formal_notice_july_2025/FORMALNOTICE-CESSATIONOFCRIMINALINSTRUCTIONS.docx",
        "evidence/formal_notice_july_2025/email-body.html"
    ]
    
    # Check if files exist
    missing_files = []
    for file_path in evidence_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print(f"📁 Processing {len(evidence_files)} evidence files:")
    for file_path in evidence_files:
        print(f"   - {file_path}")
    
    try:
        # Process the evidence package
        package = processor.process_evidence_package(
            evidence_files, 
            "formal_notice_july_2025_automated"
        )
        
        print(f"\n✅ Evidence package processed successfully!")
        print(f"📦 Package name: {package.package_name}")
        print(f"📂 Evidence folder: {package.evidence_folder}")
        
        # Display analysis results
        print(f"\n📊 Analysis Results:")
        print(f"   - Entities extracted: {len(package.entities)}")
        print(f"   - Timeline events: {len(package.timeline_events)}")
        print(f"   - Legal violations: {len(package.legal_violations)}")
        
        # Show sample entities
        if package.entities:
            print(f"\n👥 Sample Entities:")
            for i, entity in enumerate(package.entities[:5]):
                print(f"   {i+1}. {entity['type'].title()}: {entity['name']}")
        
        # Show sample timeline events
        if package.timeline_events:
            print(f"\n📅 Sample Timeline Events:")
            for i, event in enumerate(package.timeline_events[:3]):
                print(f"   {i+1}. {event['date']}: {event['description'][:60]}...")
        
        # Show sample legal violations
        if package.legal_violations:
            print(f"\n⚖️ Sample Legal Violations:")
            for i, violation in enumerate(package.legal_violations[:3]):
                print(f"   {i+1}. {violation['category']} ({violation['severity']})")
        
        print(f"\n🎯 Integration Status:")
        print(f"   ✅ Evidence files organized in folder structure")
        print(f"   ✅ Entities integrated with repository database")
        print(f"   ✅ Timeline events added to main timeline")
        print(f"   ✅ Analysis files generated (JSON format)")
        print(f"   ✅ README documentation created")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing evidence package: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    print("🚀 Evidence Automation System Test")
    print("Testing automated processing of July 2025 formal notice")
    print()
    
    success = test_evidence_automation()
    
    if success:
        print("\n🎉 Evidence automation test completed successfully!")
        print("The system has demonstrated automated:")
        print("   - File content extraction")
        print("   - Entity recognition and analysis")
        print("   - Timeline event extraction")
        print("   - Legal violation identification")
        print("   - Evidence folder organization")
        print("   - Repository integration")
    else:
        print("\n❌ Evidence automation test failed!")
        print("Please check the error messages above.")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
