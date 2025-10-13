#!/usr/bin/env python3
"""
Manual Affidavit Enhancement Script

Run affidavit enhancement manually with various options.
"""

import argparse
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from affidavit_enhancement.affidavit_processor import AffidavitProcessor


def setup_logging(verbose: bool = False):
    """Set up logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('affidavit_enhancement.log')
        ]
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Enhance affidavits with evidence updates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Enhance all affidavits with recent evidence changes
  python scripts/enhance_affidavits.py --verbose
  
  # Enhance only with critical/high priority updates
  python scripts/enhance_affidavits.py --priority-filter critical,high
  
  # Enhance only changes since yesterday  
  python scripts/enhance_affidavits.py --since "2025-01-01T00:00:00"
  
  # Use custom configuration
  python scripts/enhance_affidavits.py --config config/affidavit_enhancement.json
  
  # Dry run (analyze only, don't modify files)
  python scripts/enhance_affidavits.py --dry-run --verbose
        """
    )
    
    parser.add_argument(
        "--config", 
        help="Path to configuration file",
        default="config/affidavit_enhancement.json"
    )
    
    parser.add_argument(
        "--since", 
        help="Only process changes since timestamp (ISO format)",
        type=str
    )
    
    parser.add_argument(
        "--priority-filter",
        help="Only process updates with specified priorities (comma-separated)",
        default="critical,high,medium"
    )
    
    parser.add_argument(
        "--affidavit-pattern",
        help="Override affidavit file pattern",
        action="append"
    )
    
    parser.add_argument(
        "--evidence-pattern", 
        help="Override evidence file pattern",
        action="append"
    )
    
    parser.add_argument(
        "--dry-run",
        help="Analyze evidence changes but don't modify affidavits",
        action="store_true"
    )
    
    parser.add_argument(
        "--backup-dir",
        help="Override backup directory",
        type=str
    )
    
    parser.add_argument(
        "--output-dir", 
        help="Override output directory",
        type=str
    )
    
    parser.add_argument(
        "--verbose", "-v",
        help="Enable verbose logging", 
        action="store_true"
    )
    
    parser.add_argument(
        "--report-only",
        help="Generate analysis report without processing",
        action="store_true"
    )
    
    parser.add_argument(
        "--since-hours",
        help="Process changes from N hours ago",
        type=int
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Handle since timestamp options
        since_timestamp = args.since
        if args.since_hours:
            since_dt = datetime.now() - timedelta(hours=args.since_hours)
            since_timestamp = since_dt.isoformat()
            
        # Initialize processor
        config_path = args.config if Path(args.config).exists() else None
        if config_path:
            logger.info(f"Using configuration: {config_path}")
        else:
            logger.info("Using default configuration")
            
        processor = AffidavitProcessor(config_path)
        
        # Override configuration from command line
        if args.affidavit_pattern:
            processor.config["affidavit_patterns"] = args.affidavit_pattern
            
        if args.evidence_pattern:
            processor.config["evidence_patterns"] = args.evidence_pattern
            
        if args.backup_dir:
            processor.backup_dir = Path(args.backup_dir)
            processor.backup_dir.mkdir(parents=True, exist_ok=True)
            
        if args.output_dir:
            processor.output_dir = Path(args.output_dir)
            processor.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Discover affidavits
        logger.info("🔍 Discovering affidavit files...")
        affidavits = processor.discover_affidavits()
        logger.info(f"Found {len(affidavits)} affidavit files")
        
        for affidavit in affidavits:
            logger.info(f"  - {affidavit.name}")
            
        # Analyze evidence changes
        logger.info("📊 Analyzing evidence changes...")
        updates = processor.analyze_evidence_changes(since_timestamp)
        logger.info(f"Found {len(updates)} evidence updates")
        
        # Filter by priority
        priority_filter = [p.strip() for p in args.priority_filter.split(',')]
        filtered_updates = [u for u in updates if u.priority in priority_filter]
        logger.info(f"After priority filtering ({', '.join(priority_filter)}): {len(filtered_updates)} updates")
        
        # Show update summary
        if filtered_updates:
            priority_counts = {}
            for update in filtered_updates:
                priority_counts[update.priority] = priority_counts.get(update.priority, 0) + 1
                
            logger.info("Evidence update summary:")
            for priority, count in sorted(priority_counts.items()):
                logger.info(f"  - {priority.title()}: {count}")
                
            # Show some example updates
            logger.info("Example updates:")
            for update in filtered_updates[:3]:
                logger.info(f"  - {Path(update.evidence_file).name} ({update.priority}): {update.update_type}")
        
        # Report-only mode
        if args.report_only:
            logger.info("📋 Report-only mode - generating analysis report")
            
            report_content = f"""# Affidavit Enhancement Analysis Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Configuration**: {args.config}
**Since Timestamp**: {since_timestamp or 'All time'}
**Priority Filter**: {args.priority_filter}

## Discovery Results

**Affidavit Files Found**: {len(affidavits)}
"""
            
            for affidavit in affidavits:
                report_content += f"- {affidavit.name}\n"
                
            report_content += f"""
## Evidence Analysis Results

**Total Evidence Updates**: {len(updates)}
**Filtered Updates**: {len(filtered_updates)}

### Priority Breakdown
"""
            
            if filtered_updates:
                priority_counts = {}
                for update in filtered_updates:
                    priority_counts[update.priority] = priority_counts.get(update.priority, 0) + 1
                    
                for priority, count in sorted(priority_counts.items()):
                    report_content += f"- **{priority.title()}**: {count}\n"
                    
                report_content += "\n### Detailed Updates\n\n"
                
                for i, update in enumerate(filtered_updates[:10], 1):
                    report_content += f"""#### {i}. {Path(update.evidence_file).name}

- **Priority**: {update.priority}
- **Type**: {update.update_type}  
- **Sections**: {', '.join(update.applicable_sections)}
- **Timestamp**: {update.timestamp}

"""
            
            report_path = Path("AFFIDAVIT_ANALYSIS_REPORT.md")
            report_path.write_text(report_content)
            logger.info(f"📄 Analysis report saved to: {report_path}")
            return
        
        # Dry run mode
        if args.dry_run:
            logger.info("🧪 Dry run mode - analyzing without modifications")
            
            # Show what would be enhanced
            logger.info("Affidavits that would be enhanced:")
            for affidavit_path in affidavits:
                relevant_updates = processor._filter_relevant_updates(affidavit_path, filtered_updates)
                if relevant_updates:
                    logger.info(f"  ✅ {affidavit_path.name} - {len(relevant_updates)} updates")
                    for update in relevant_updates[:3]:
                        logger.info(f"    - {Path(update.evidence_file).name} ({update.priority})")
                else:
                    logger.info(f"  ⏭️ {affidavit_path.name} - no relevant updates")
                    
            logger.info("🧪 Dry run complete - no files modified")
            return
        
        # Process affidavits
        if not filtered_updates:
            logger.info("ℹ️ No evidence updates found matching criteria")
            return
            
        logger.info("📝 Processing affidavits...")
        
        # Temporarily filter updates for processing
        original_method = processor._filter_relevant_updates
        def filtered_filter(affidavit_path, updates):
            relevant = original_method(affidavit_path, updates)
            return [u for u in relevant if u in filtered_updates]
        processor._filter_relevant_updates = filtered_filter
        
        # Process affidavits with progress tracking
        logger.info("🚀 Starting affidavit enhancement with progress tracking...")
        results = processor.process_all_affidavits(since_timestamp, max_workers=2)
        
        # Restore original method
        processor._filter_relevant_updates = original_method
        
        # Generate and display report
        report = processor.generate_enhancement_report(results)
        
        logger.info("📊 Enhancement Results:")
        logger.info(f"  - Total affidavits: {len(results)}")
        logger.info(f"  - Successfully enhanced: {sum(1 for success in results.values() if success)}")
        logger.info(f"  - Failed: {sum(1 for success in results.values() if not success)}")
        
        # Save detailed report
        report_path = Path("AFFIDAVIT_ENHANCEMENT_REPORT.md")
        report_path.write_text(report)
        logger.info(f"📄 Detailed report saved to: {report_path}")
        
        # Show enhanced files
        if processor.output_dir.exists():
            enhanced_files = list(processor.output_dir.glob("*"))
            if enhanced_files:
                logger.info(f"📁 Enhanced files saved to: {processor.output_dir}")
                for file in enhanced_files:
                    logger.info(f"  - {file.name}")
        
        # Show backup files  
        if processor.backup_dir.exists():
            backup_files = list(processor.backup_dir.glob("*"))
            if backup_files:
                logger.info(f"💾 Backup files saved to: {processor.backup_dir}")
                for file in backup_files:
                    logger.info(f"  - {file.name}")
                    
        logger.info("✅ Affidavit enhancement completed successfully")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Enhancement cancelled by user")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Enhancement failed: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()