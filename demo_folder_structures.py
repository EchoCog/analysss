#!/usr/bin/env python3
"""
Evidence Management System - Folder Structure Demonstration
===========================================================

This script demonstrates the comprehensive folder structure generation
capabilities of the Evidence Management System.
"""

import json
import os
from datetime import datetime

from frameworks.evidence_management import (
    ClassificationLevel,
    EvidenceItem,
    EvidenceManagementSystem,
    EvidenceType,
    VerificationStatus,
)
from tools.folder_structure_generator import FolderStructureGenerator


def demo_comprehensive_structure():
    """Demonstrate comprehensive folder structure creation"""
    print("=" * 80)
    print("EVIDENCE MANAGEMENT SYSTEM - FOLDER STRUCTURE DEMONSTRATION")
    print("=" * 80)

    # Initialize system
    base_dir = "/tmp/evidence_demo"
    ems = EvidenceManagementSystem(base_dir)

    print(f"\n🏗️  Initializing Evidence Management System at: {base_dir}")
    print(
        f"📁 Total folders created: {len(ems._generate_comprehensive_folder_structure())}"
    )

    # Show folder structure visualization
    print("\n📊 FOLDER STRUCTURE VISUALIZATION:")
    print("-" * 50)
    print(ems.visualize_folder_structure())

    # Create sample case with various evidence types
    print("\n🔍 CREATING SAMPLE INVESTIGATION CASE:")
    print("-" * 50)

    case = ems.create_case_file(
        "INV_2025_001",
        "Complex Financial Fraud Investigation",
        "Multi-jurisdictional investigation involving financial fraud, communication interception, and digital forensics",
    )

    # Add investigators and keywords
    case.investigators.update(
        ["Det. Sarah Johnson", "Agent Mike Chen", "Analyst Emma Davis"]
    )
    case.keywords.update(
        [
            "financial fraud",
            "money laundering",
            "digital forensics",
            "communication analysis",
        ]
    )
    ems._save_case_file_metadata(case)

    print(f"✅ Case created: {case.case_id}")
    print(f"   Title: {case.title}")
    print(f"   Investigators: {', '.join(case.investigators)}")

    # Create diverse evidence items
    evidence_samples = [
        {
            "id": "DOC_001",
            "title": "Suspicious Bank Contract",
            "type": EvidenceType.DOCUMENT,
            "classification": ClassificationLevel.CONFIDENTIAL,
            "description": "Banking contract with unusual clauses",
            "content": b"CONFIDENTIAL BANKING CONTRACT\nParties: XYZ Corp, ABC Bank\nSuspicious Clause 15...",
        },
        {
            "id": "EMAIL_001",
            "title": "Incriminating Email Thread",
            "type": EvidenceType.COMMUNICATION,
            "classification": ClassificationLevel.RESTRICTED,
            "description": "Email thread discussing questionable transactions",
            "content": b"From: john@example.com\nTo: jane@corp.com\nSubject: Re: Special Account\nThe transfers need to be...",
        },
        {
            "id": "TRANS_001",
            "title": "Large Transaction Record",
            "type": EvidenceType.FINANCIAL,
            "classification": ClassificationLevel.PRIVILEGED,
            "description": "Suspicious large transaction between accounts",
            "content": b"TRANSACTION RECORD\nAmount: $2,500,000\nFrom: Account 1234567\nTo: Offshore Account...",
        },
        {
            "id": "LOG_001",
            "title": "Server Access Logs",
            "type": EvidenceType.TECHNICAL,
            "classification": ClassificationLevel.CONFIDENTIAL,
            "description": "Server logs showing unauthorized access attempts",
            "content": b"2025-01-15 02:30:15 UNAUTHORIZED LOGIN ATTEMPT\n2025-01-15 02:31:22 ROOT ACCESS GRANTED...",
        },
        {
            "id": "PHOTO_001",
            "title": "Evidence Scene Photography",
            "type": EvidenceType.PHOTOGRAPHIC,
            "classification": ClassificationLevel.PUBLIC,
            "description": "Photographs of physical evidence at crime scene",
            "content": b"JPEG binary data representing crime scene photos...",
        },
    ]

    print("\n📋 ADDING EVIDENCE ITEMS:")
    print("-" * 50)

    for item in evidence_samples:
        evidence = EvidenceItem(
            evidence_id=item["id"],
            title=item["title"],
            evidence_type=item["type"],
            classification=item["classification"],
            verification_status=VerificationStatus.VERIFIED,
            description=item["description"],
            source="Investigation Team Alpha",
            collection_date=datetime(2025, 1, 15, 14, 30),
        )

        # Add relevant tags
        evidence.tags.update(["investigation", "financial", "verified"])

        # Add evidence to system
        ems.add_evidence_item(evidence, item["content"])
        ems.add_evidence_to_case("INV_2025_001", item["id"])

        print(f"   ✅ {item['id']}: {item['title']}")
        print(f"      📁 Stored at: {evidence.file_path}")

    # Create case-specific folder structure
    print("\n🗂️  CREATING CASE-SPECIFIC FOLDER STRUCTURE:")
    print("-" * 50)

    case_structure = ems.create_case_folder_structure("INV_2025_001")
    print(f"✅ Case folders created: {case_structure['folders_created']}")
    print(f"📁 Base path: {case_structure['base_path']}")
    print(f"📄 README created: {case_structure['readme_path']}")

    # Generate comprehensive reports
    print("\n📊 GENERATING SYSTEM REPORTS:")
    print("-" * 50)

    # Folder structure report
    structure_report = ems.generate_folder_structure_report()
    print(f"📁 Main categories: {len(structure_report['main_categories'])}")
    print(
        f"🔒 Classification folders: {len(structure_report['classification_folders'])}"
    )
    print(
        f"📅 Date-based organization: {'Yes' if structure_report['date_based_organization'] else 'No'}"
    )

    # Case report
    case_report = ems.generate_case_report("INV_2025_001")
    print(f"📋 Evidence items in case: {case_report['total_evidence_items']}")
    print(f"✅ Verification status: {json.dumps(case_report['verification_summary'])}")

    # System analysis
    system_analysis = ems.export_professional_analysis()
    print(
        f"🔍 Total evidence items: {system_analysis['system_overview']['total_evidence_items']}"
    )
    print(f"📁 Active cases: {len(system_analysis['active_cases'])}")

    return ems, case_structure, structure_report


def demo_template_generation():
    """Demonstrate template generation capabilities"""
    print("\n" + "=" * 80)
    print("TEMPLATE GENERATION DEMONSTRATION")
    print("=" * 80)

    template_dir = "/tmp/evidence_template_demo"
    generator = FolderStructureGenerator(template_dir)

    print(f"\n🏗️  Creating template structure at: {template_dir}")

    # Create template with full documentation
    result = generator.create_template_structure()

    print(f"✅ Template created successfully!")
    print(f"📁 Folders created: {result['folders_created']}")
    print(f"📄 Documentation files: {len(result['documentation_files'])}")

    # Export to JSON
    json_file = f"{template_dir}/structure_export.json"
    generator.export_structure_to_json(json_file)
    print(f"💾 Structure exported to: {json_file}")

    # Show some created documentation
    readme_path = f"{template_dir}/README.md"
    if os.path.exists(readme_path):
        print(f"\n📄 Template README.md created:")
        with open(readme_path, "r") as f:
            lines = f.readlines()[:10]  # Show first 10 lines
            for line in lines:
                print(f"   {line.rstrip()}")
        print("   ...")

    return template_dir


def show_final_summary(ems, structure_report):
    """Show final summary of capabilities"""
    print("\n" + "=" * 80)
    print("FOLDER STRUCTURE GENERATION SUMMARY")
    print("=" * 80)

    print("\n🎯 KEY FEATURES IMPLEMENTED:")
    features = [
        f"📁 {structure_report['total_folders']} total organized folders",
        "📅 Date-based organization (YYYY/MM format)",
        "🔒 Security classification support (4 levels)",
        "🗂️  Case-specific folder structures",
        "🤖 Intelligent file placement based on content",
        "📊 ASCII tree visualization",
        "📚 Comprehensive documentation generation",
        "💾 JSON export capabilities",
        "🔧 Template generation with .gitkeep files",
        "⚡ Professional evidence management standards",
    ]

    for feature in features:
        print(f"   ✅ {feature}")

    print("\n📋 FOLDER CATEGORIES:")
    for category in structure_report["main_categories"][:8]:  # Show first 8
        print(f"   📁 {category['name'].ljust(15)} - {category['description']}")
    print("   ...")

    print(f"\n🔍 EVIDENCE TYPES SUPPORTED:")
    evidence_types = [
        "Documents",
        "Communications",
        "Financial Records",
        "Technical Evidence",
        "Media (Photos/Audio/Video)",
        "Witness Statements",
        "Digital Forensics",
    ]
    for ev_type in evidence_types:
        print(f"   📄 {ev_type}")

    print(f"\n🔒 SECURITY CLASSIFICATIONS:")
    classifications = ["Public", "Confidential", "Restricted", "Privileged"]
    for classification in classifications:
        print(f"   🛡️  {classification}")

    print(f"\n📊 SYSTEM STATISTICS:")
    print(f"   📁 Base directory: {ems.base_directory}")
    print(f"   📋 Evidence items: {len(ems.evidence_items)}")
    print(f"   🗂️  Case files: {len(ems.case_files)}")
    print(f"   📅 Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Main demonstration function"""
    print("🚀 Starting Evidence Management System Folder Structure Demonstration...")

    # Demo comprehensive structure
    ems, case_structure, structure_report = demo_comprehensive_structure()

    # Demo template generation
    template_dir = demo_template_generation()

    # Show final summary
    show_final_summary(ems, structure_report)

    print("\n" + "=" * 80)
    print("✅ DEMONSTRATION COMPLETE!")
    print("=" * 80)
    print(f"🔍 Explore the created structures at:")
    print(f"   📁 Main system: {ems.base_directory}")
    print(f"   📁 Template: {template_dir}")
    print(f"   📁 Case folder: {case_structure['base_path']}")
    print(
        "\n💡 Use the folder_structure_generator.py utility for production deployment."
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
