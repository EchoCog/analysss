#!/usr/bin/env python3
"""
Evidence Search Report
Checks if any of the required evidence files are available in specified repositories.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

# Evidence requirements from jax-response README
CRITICAL_EVIDENCE_REQUIREMENTS = [
    # JF-RP (Responsible Person Documentation)
    "JF-RP1",  # Responsible Person documentation (37 jurisdictions)
    "JF-RP2",  # Regulatory risk analysis
    
    # JF-DLA (Director Loan Accounts)
    "JF-DLA1", "JF-DLA2", "JF-DLA3",  # Director loan account statements (all 3 directors)
    
    # JF-PA (Peter's Activities)
    "JF-PA1", "JF-PA2", "JF-PA3", "JF-PA4",  # Peter's own withdrawals (minimum 4 examples)
    
    # JF-BS (Bank Statements)
    "JF-BS1",  # R500K payment bank statement (16 July 2025)
    
    # JF5 Agreement Documents
    "JF5_draft_agreement",  # JF5 draft agreement (initial version reviewed)
    "JF5_final_agreement",  # JF5 final agreement (signed version with changes)
    "JF5_comparison_document",  # Comparison document highlighting all changes
    
    # Witness Statements
    "daniel_witness_statement",  # Daniel's witness statement re: "Has anything changed?" exchange
    
    # Tax Documentation
    "uk_tax_residency",  # UK tax residency documentation
    
    # Chesno Fraud Documentation
    "JF-CHESNO1", "JF-CHESNO2", "JF-CHESNO3", "JF-CHESNO4",  # Chesno fraud documentation
    
    # Restoration Evidence
    "JF-RESTORE1", "JF-RESTORE2", "JF-RESTORE3", "JF-RESTORE4",  # Daniel's 8-year restoration evidence
]

# Revenue Theft Evidence Categories
REVENUE_THEFT_EVIDENCE = [
    "14_apr_bank_letter",     # Bank account change fraud (April 14, 2025)
    "22_may_shopify_audit",   # Shopify audit trail destruction (May 22, 2025)
    "29_may_domain_registration",  # Domain registration by son for identity fraud
    "20_june_gee_gayane_email",    # Administrative instruction coordination evidence
    "08_july_warehouse_popi",      # Business sabotage and POPI violations
]

# Nuclear Evidence (from murder-theft analysis)
NUCLEAR_EVIDENCE = [
    "kayla_murder_evidence",
    "bantjies_letters_june_6",
    "bantjies_letters_june_10", 
    "rezonance_missing_funds_2023",
    "rezonance_missing_funds_2024",
    "rezonance_missing_funds_2025",
    "witness_statement_murder",
    "financial_flows_evidence",
    "trust_conspiracy_evidence",
]

def search_directory_for_evidence(directory_path, evidence_list):
    """Search a directory for evidence files matching the requirements."""
    found_evidence = {}
    missing_evidence = set(evidence_list)
    
    if not os.path.exists(directory_path):
        return found_evidence, missing_evidence
    
    # Walk through all files and directories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()
            
            # Check each evidence requirement
            for evidence in evidence_list:
                evidence_lower = evidence.lower().replace("-", "_")
                
                # Various matching strategies
                if (evidence_lower in file_lower or 
                    evidence.lower() in file_lower or
                    any(part in file_lower for part in evidence_lower.split("_")) or
                    re.search(rf'\b{re.escape(evidence_lower)}\b', file_lower)):
                    
                    if evidence not in found_evidence:
                        found_evidence[evidence] = []
                    found_evidence[evidence].append(file_path)
                    missing_evidence.discard(evidence)
    
    return found_evidence, missing_evidence

def generate_repository_report():
    """Generate comprehensive evidence report for all repositories."""
    
    base_path = "/home/runner/work/analysss/analysss"
    
    # Repository paths to check
    repo_paths = {
        "analysss_main": base_path,
        "jax_response": os.path.join(base_path, "jax-response"),
        "murder_theft": os.path.join(base_path, "murder-theft"),
        "case_2025_137857": os.path.join(base_path, "case_2025_137857"),
        "evidence": os.path.join(base_path, "evidence"),
    }
    
    # External repositories mentioned (would need API access)
    external_repos = [
        "https://github.com/cogpy/ad-res-j7",
        "https://github.com/EchoCog/analysss",  # This repo
        "https://github.com/rzonedevops/analysis",
        "https://github.com/rzonedevops/avtomaatoctory", 
        "https://github.com/rzonedevops/analyticase",
    ]
    
    # External repositories findings (manually discovered)
    external_findings = {
        "cogpy/ad-res-j7": {
            "bank_records": [
                "D_FAUCITT_PERSONAL_BANK_RECORDS_20250604.pdf",
                "D_FAUCITT_PERSONAL_BANK_RECORDS_20250704.pdf", 
                "D_FAUCITT_PERSONAL_BANK_RECORDS_20250804.pdf",
                "D_FAUCITT_PERSONAL_BANK_RECORDS_20250904.pdf",
                "D_FAUCITT_PERSONAL_BANK_RECORDS_20251004.pdf"
            ],
            "director_loan_accounts": [
                "ACCOUNTING_RECORDS_DIRECTOR_LOAN_ALLOCATION.md",
                "COMPLETION_NOTES.md"
            ],
            "jax_response_structure": [
                "AD/", "analysis-output/", "evidence-attachments/", 
                "family-trust/", "financial-flows/", "peter-interdict/",
                "revenue-theft/", "source-documents/"
            ],
            "forensic_evidence": [
                "FORENSIC_EVIDENCE_INDEX.json",
                "FORENSIC_EVIDENCE_INDEX.md"
            ]
        }
    }
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "repositories_checked": repo_paths,
        "external_repositories": external_repos,
        "evidence_categories": {
            "critical_jax_evidence": {},
            "revenue_theft_evidence": {},
            "nuclear_evidence": {}
        },
        "summary": {
            "total_critical_required": len(CRITICAL_EVIDENCE_REQUIREMENTS),
            "total_revenue_theft_required": len(REVENUE_THEFT_EVIDENCE),
            "total_nuclear_required": len(NUCLEAR_EVIDENCE),
            "found_critical": 0,
            "found_revenue_theft": 0,
            "found_nuclear": 0
        }
    }
    
    # Search each repository
    for repo_name, repo_path in repo_paths.items():
        if os.path.exists(repo_path):
            print(f"Searching {repo_name}: {repo_path}")
            
            # Search for critical evidence
            found_critical, missing_critical = search_directory_for_evidence(
                repo_path, CRITICAL_EVIDENCE_REQUIREMENTS
            )
            
            # Search for revenue theft evidence
            found_revenue, missing_revenue = search_directory_for_evidence(
                repo_path, REVENUE_THEFT_EVIDENCE
            )
            
            # Search for nuclear evidence
            found_nuclear, missing_nuclear = search_directory_for_evidence(
                repo_path, NUCLEAR_EVIDENCE
            )
            
            # Store results
            report["evidence_categories"]["critical_jax_evidence"][repo_name] = {
                "found": found_critical,
                "missing": list(missing_critical),
                "found_count": len(found_critical)
            }
            
            report["evidence_categories"]["revenue_theft_evidence"][repo_name] = {
                "found": found_revenue,
                "missing": list(missing_revenue),
                "found_count": len(found_revenue)
            }
            
            report["evidence_categories"]["nuclear_evidence"][repo_name] = {
                "found": found_nuclear,
                "missing": list(missing_nuclear),
                "found_count": len(found_nuclear)
            }
            
            # Update summary
            report["summary"]["found_critical"] += len(found_critical)
            report["summary"]["found_revenue_theft"] += len(found_revenue)
            report["summary"]["found_nuclear"] += len(found_nuclear)
    
    return report

def generate_markdown_report(report):
    """Generate markdown report from the evidence search results."""
    
    md_lines = [
        "# Evidence Files Search Report",
        f"**Generated:** {report['timestamp']}",
        "",
        "## Executive Summary",
        "",
        f"- **Critical JAX Evidence**: {report['summary']['found_critical']}/{report['summary']['total_critical_required']} found",
        f"- **Revenue Theft Evidence**: {report['summary']['found_revenue_theft']}/{report['summary']['total_revenue_theft_required']} found", 
        f"- **Nuclear Evidence**: {report['summary']['found_nuclear']}/{report['summary']['total_nuclear_required']} found",
        "",
        "## Repositories Checked",
        "",
    ]
    
    # Add repositories checked
    for repo_name, repo_path in report["repositories_checked"].items():
        exists = "✅" if os.path.exists(repo_path) else "❌"
        md_lines.append(f"- **{repo_name}**: {repo_path} {exists}")
    
    md_lines.extend([
        "",
        "## External Repositories Mentioned",
        "",
    ])
    
    for repo in report["external_repositories"]:
        md_lines.append(f"- {repo}")
    
    # Critical Evidence Section
    md_lines.extend([
        "",
        "## Critical JAX Evidence Results",
        "",
    ])
    
    for repo_name, results in report["evidence_categories"]["critical_jax_evidence"].items():
        if results["found_count"] > 0:
            md_lines.append(f"### {repo_name} - Found {results['found_count']} items")
            for evidence, files in results["found"].items():
                md_lines.append(f"- **{evidence}**:")
                for file_path in files:
                    md_lines.append(f"  - `{file_path}`")
            md_lines.append("")
    
    # Revenue Theft Evidence Section
    md_lines.extend([
        "",
        "## Revenue Theft Evidence Results", 
        "",
    ])
    
    for repo_name, results in report["evidence_categories"]["revenue_theft_evidence"].items():
        if results["found_count"] > 0:
            md_lines.append(f"### {repo_name} - Found {results['found_count']} items")
            for evidence, files in results["found"].items():
                md_lines.append(f"- **{evidence}**:")
                for file_path in files:
                    md_lines.append(f"  - `{file_path}`")
            md_lines.append("")
    
    # Nuclear Evidence Section
    md_lines.extend([
        "",
        "## Nuclear Evidence Results",
        "",
    ])
    
    for repo_name, results in report["evidence_categories"]["nuclear_evidence"].items():
        if results["found_count"] > 0:
            md_lines.append(f"### {repo_name} - Found {results['found_count']} items")
            for evidence, files in results["found"].items():
                md_lines.append(f"- **{evidence}**:")
                for file_path in files:
                    md_lines.append(f"  - `{file_path}`")
            md_lines.append("")
    
    # Missing Evidence Summary
    md_lines.extend([
        "",
        "## Missing Evidence Summary",
        "",
        "### Critical JAX Evidence Still Missing",
        "",
    ])
    
    all_missing_critical = set(CRITICAL_EVIDENCE_REQUIREMENTS)
    for repo_name, results in report["evidence_categories"]["critical_jax_evidence"].items():
        all_missing_critical -= set(results["found"].keys())
    
    for missing in sorted(all_missing_critical):
        md_lines.append(f"- ❌ {missing}")
    
    md_lines.extend([
        "",
        "### Revenue Theft Evidence Still Missing",
        "",
    ])
    
    all_missing_revenue = set(REVENUE_THEFT_EVIDENCE)
    for repo_name, results in report["evidence_categories"]["revenue_theft_evidence"].items():
        all_missing_revenue -= set(results["found"].keys())
    
    for missing in sorted(all_missing_revenue):
        md_lines.append(f"- ❌ {missing}")
    
    md_lines.extend([
        "",
        "### Nuclear Evidence Still Missing",
        "",
    ])
    
    all_missing_nuclear = set(NUCLEAR_EVIDENCE)
    for repo_name, results in report["evidence_categories"]["nuclear_evidence"].items():
        all_missing_nuclear -= set(results["found"].keys())
    
    for missing in sorted(all_missing_nuclear):
        md_lines.append(f"- ❌ {missing}")
    
    return "\n".join(md_lines)

if __name__ == "__main__":
    print("Generating evidence search report...")
    
    # Generate the report
    report = generate_repository_report()
    
    # Save JSON report
    json_path = "/home/runner/work/analysss/analysss/evidence_search_report.json"
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)
    
    # Generate and save markdown report
    markdown_report = generate_markdown_report(report)
    md_path = "/home/runner/work/analysss/analysss/EVIDENCE_SEARCH_REPORT.md"
    with open(md_path, "w") as f:
        f.write(markdown_report)
    
    print(f"Reports generated:")
    print(f"- JSON: {json_path}")
    print(f"- Markdown: {md_path}")
    
    # Print summary
    print(f"\nSUMMARY:")
    print(f"Critical JAX Evidence: {report['summary']['found_critical']}/{report['summary']['total_critical_required']}")
    print(f"Revenue Theft Evidence: {report['summary']['found_revenue_theft']}/{report['summary']['total_revenue_theft_required']}")
    print(f"Nuclear Evidence: {report['summary']['found_nuclear']}/{report['summary']['total_nuclear_required']}")