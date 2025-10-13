#!/usr/bin/env python3
"""
Automated Entity and Evidence Processing Script

This script supports the GitHub Action workflow for automated entity
and evidence processing. It provides a unified interface to all processing
functions with proper error handling and logging.
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from evidence_automation.evidence_pipeline import EvidenceProcessor
    from evidence_automation.processor import process_evidence_files
except ImportError as e:
    print(f"Warning: Could not import evidence automation modules: {e}")
    EvidenceProcessor = None
    process_evidence_files = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutoEntityProcessor:
    """Main class for automated entity and evidence processing."""
    
    def __init__(self, repository_root: str = "."):
        """
        Initialize the processor.
        
        Args:
            repository_root: Root directory of the repository
        """
        self.repo_root = Path(repository_root).resolve()
        self.entities_dir = self.repo_root / "entities"
        self.evidence_dir = self.repo_root / "evidence"
        self.timeline_dir = self.repo_root / "03_timeline"
        self.models_dir = self.repo_root / "04_models"
        
        # Create directories if they don't exist
        self.entities_dir.mkdir(exist_ok=True)
        self.timeline_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        
    def scan_for_changes(self, since_commit: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Scan repository for changes in relevant files.
        
        Args:
            since_commit: Git commit hash to compare against (optional)
            
        Returns:
            Dictionary of changed files by category
        """
        changed_files = {
            'evidence': [],
            'entities': [],
            'timeline': [],
            'models': [],
            'other': []
        }
        
        # Define patterns for different file types
        patterns = {
            'evidence': [r'evidence/', r'\.md$', r'\.json$', r'\.txt$', r'\.docx?$', r'\.pdf$'],
            'entities': [r'entities/', r'ENTITY', r'entity'],
            'timeline': [r'03_timeline/', r'timeline', r'TIMELINE'],
            'models': [r'04_models/', r'models/', r'MODEL']
        }
        
        if since_commit:
            # Use git to find changed files
            try:
                import subprocess
                result = subprocess.run(
                    ['git', 'diff', '--name-only', f'{since_commit}..HEAD'],
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    files_to_check = result.stdout.strip().split('\n')
                else:
                    logger.warning("Could not get git diff, scanning all files")
                    files_to_check = []
            except Exception as e:
                logger.warning(f"Could not run git command: {e}")
                files_to_check = []
        else:
            files_to_check = []
        
        if not files_to_check:
            # Scan all files if git diff not available
            files_to_check = []
            for pattern in ['**/*.md', '**/*.json', '**/*.txt']:
                files_to_check.extend(str(f.relative_to(self.repo_root)) 
                                    for f in self.repo_root.glob(pattern))
        
        # Categorize files
        for file_path in files_to_check:
            if not file_path.strip():
                continue
                
            categorized = False
            for category, category_patterns in patterns.items():
                if any(re.search(pattern, file_path) for pattern in category_patterns):
                    changed_files[category].append(file_path)
                    categorized = True
                    break
            
            if not categorized:
                changed_files['other'].append(file_path)
        
        logger.info(f"Detected changes: {sum(len(files) for files in changed_files.values())} files")
        for category, files in changed_files.items():
            if files:
                logger.info(f"  {category}: {len(files)} files")
        
        return changed_files
    
    def extract_entities_from_text(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from text using pattern matching.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of entities by type
        """
        entities = {
            'persons': set(),
            'organizations': set(),
            'dates': set(),
            'locations': set(),
            'financial': set(),
            'legal_entities': set(),
            'case_numbers': set()
        }
        
        # Person names (improved pattern)
        person_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b',  # First Last [Middle]
            r'\b(?:Mr|Ms|Mrs|Dr|Prof)\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b',  # Title + Name
        ]
        for pattern in person_patterns:
            matches = re.findall(pattern, text)
            entities['persons'].update(matches)
        
        # Organizations
        org_patterns = [
            r'\b[A-Z][a-zA-Z\s]+ (?:Ltd|Limited|Inc|Corporation|Corp|Company|Group|Holdings|Pty)\b',
            r'\b[A-Z][A-Z&\s]+ (?:Bank|Financial|Insurance|Trust|Fund)\b',
            r'\bRegim[A-Z]\s+[A-Za-z\s]+\b'  # RegimA related entities
        ]
        for pattern in org_patterns:
            matches = re.findall(pattern, text)
            entities['organizations'].update(matches)
        
        # Dates (multiple formats)
        date_patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',  # ISO format
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # US format
            r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # EU format
            r'\b[A-Z][a-z]+ \d{1,2}, \d{4}\b',  # Month Day, Year
            r'\b\d{1,2} [A-Z][a-z]+ \d{4}\b'  # Day Month Year
        ]
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            entities['dates'].update(matches)
        
        # Financial amounts
        financial_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',  # USD
            r'\£[\d,]+(?:\.\d{2})?',  # GBP
            r'R[\d,]+(?:\.\d{2})?',   # ZAR
            r'€[\d,]+(?:\.\d{2})?'    # EUR
        ]
        for pattern in financial_patterns:
            matches = re.findall(pattern, text)
            entities['financial'].update(matches)
        
        # Legal entities and case numbers
        legal_patterns = [
            r'\bCase\s+(?:No\.?)?\s*\d{4}[/_]\d+\b',
            r'\b[A-Z]{2,}\s*\d{4}[/_]\d+\b',
            r'\bCourt\s+Case\s+\d+\b'
        ]
        for pattern in legal_patterns:
            matches = re.findall(pattern, text)
            entities['legal_entities'].update(matches)
        
        # Convert sets back to lists for JSON serialization
        return {key: list(value) for key, value in entities.items()}
    
    def process_evidence_files(self, file_paths: List[str]) -> Dict:
        """
        Process evidence files and extract information.
        
        Args:
            file_paths: List of file paths to process
            
        Returns:
            Processing results
        """
        results = {
            'processed_files': [],
            'entities_extracted': {},
            'errors': []
        }
        
        for file_path in file_paths:
            try:
                file_path_obj = Path(self.repo_root / file_path)
                if not file_path_obj.exists():
                    continue
                
                logger.info(f"Processing evidence file: {file_path}")
                
                # Read file content
                content = ""
                if file_path_obj.suffix.lower() in ['.md', '.txt']:
                    with open(file_path_obj, 'r', encoding='utf-8') as f:
                        content = f.read()
                elif file_path_obj.suffix.lower() == '.json':
                    with open(file_path_obj, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        content = json.dumps(data, indent=2)
                
                if content:
                    # Extract entities from content
                    entities = self.extract_entities_from_text(content)
                    
                    # Filter out empty results
                    entities = {k: v for k, v in entities.items() if v}
                    
                    if entities:
                        results['entities_extracted'][file_path] = entities
                    
                    results['processed_files'].append(file_path)
                
            except Exception as e:
                error_msg = f"Error processing {file_path}: {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
        
        return results
    
    def create_entity_files(self, entities_data: Dict) -> int:
        """
        Create individual entity files from extracted data.
        
        Args:
            entities_data: Dictionary of extracted entities
            
        Returns:
            Number of entity files created
        """
        created_count = 0
        
        for source_file, file_entities in entities_data.items():
            for entity_type, entities in file_entities.items():
                for entity in entities:
                    if not entity.strip():
                        continue
                        
                    # Normalize entity name for filename
                    filename = entity.lower().strip()
                    filename = re.sub(r'[^\w\s-]', '', filename)  # Remove special chars
                    filename = re.sub(r'[-\s]+', '_', filename)   # Replace spaces/hyphens with underscore
                    filename = filename[:50]  # Limit length
                    
                    if not filename:
                        continue
                    
                    entity_file = self.entities_dir / f"{filename}.md"
                    
                    # Check if file already exists and has content
                    if entity_file.exists():
                        with open(entity_file, 'r') as f:
                            existing_content = f.read()
                        if len(existing_content) > 200:  # Skip if substantial content exists
                            continue
                    
                    # Create entity profile
                    entity_content = f"""# {entity}

## Entity Profile
- **Type**: {entity_type.title()}
- **Source**: {source_file}
- **Last Updated**: {datetime.now().isoformat()}
- **Status**: Automatically Extracted

## Occurrences
- Found in: {source_file}
- Entity Type: {entity_type}
- Extraction Method: Pattern Matching

## Analysis Notes
*This entity was automatically extracted. Manual review and enhancement recommended.*

## Related Files
- {source_file}

## Actions Required
- [ ] Verify entity accuracy
- [ ] Add detailed analysis
- [ ] Link to related entities
- [ ] Update timeline if applicable
"""
                    
                    # Write entity file
                    try:
                        with open(entity_file, 'w', encoding='utf-8') as f:
                            f.write(entity_content)
                        created_count += 1
                        logger.info(f"Created entity file: {entity_file}")
                    except Exception as e:
                        logger.error(f"Error creating entity file {entity_file}: {e}")
        
        return created_count
    
    def update_timeline(self, entities_data: Dict) -> int:
        """
        Update timeline with events extracted from entities.
        
        Args:
            entities_data: Dictionary of extracted entities
            
        Returns:
            Number of timeline events created
        """
        events_created = 0
        timeline_entries = []
        
        for source_file, file_entities in entities_data.items():
            dates = file_entities.get('dates', [])
            
            for date_str in dates:
                # Try to parse and normalize the date
                try:
                    # Basic date parsing (could be enhanced with dateutil)
                    event_entry = {
                        'date': date_str,
                        'source_file': source_file,
                        'event_type': 'document_reference',
                        'description': f'Date reference found in {source_file}',
                        'entities_involved': [],
                        'created_by': 'auto_entity_processor',
                        'created_at': datetime.now().isoformat()
                    }
                    
                    # Add related entities from the same file
                    for entity_type in ['persons', 'organizations']:
                        if entity_type in file_entities:
                            event_entry['entities_involved'].extend(file_entities[entity_type])
                    
                    timeline_entries.append(event_entry)
                    events_created += 1
                    
                except Exception as e:
                    logger.warning(f"Could not process date {date_str}: {e}")
        
        # Save timeline entries
        if timeline_entries:
            timeline_file = self.timeline_dir / "entries" / f"auto_extracted_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            timeline_file.parent.mkdir(exist_ok=True)
            
            try:
                with open(timeline_file, 'w', encoding='utf-8') as f:
                    json.dump(timeline_entries, f, indent=2)
                logger.info(f"Created timeline file: {timeline_file}")
            except Exception as e:
                logger.error(f"Error creating timeline file: {e}")
        
        return events_created
    
    def update_models(self, entities_data: Dict) -> Dict:
        """
        Update model files with new entity and relationship data.
        
        Args:
            entities_data: Dictionary of extracted entities
            
        Returns:
            Dictionary of model update results
        """
        results = {
            'hypergraph_updated': False,
            'entity_model_updated': False,
            'files_created': []
        }
        
        # Create consolidated entity model
        entity_model = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'created_by': 'auto_entity_processor',
                'source_files': list(entities_data.keys())
            },
            'entities_by_type': {},
            'entity_relationships': [],
            'statistics': {}
        }
        
        # Aggregate entities by type
        all_entities_by_type = {}
        for source_file, file_entities in entities_data.items():
            for entity_type, entities in file_entities.items():
                if entity_type not in all_entities_by_type:
                    all_entities_by_type[entity_type] = set()
                all_entities_by_type[entity_type].update(entities)
        
        # Convert to lists and add to model
        entity_model['entities_by_type'] = {
            k: list(v) for k, v in all_entities_by_type.items()
        }
        
        # Calculate statistics
        entity_model['statistics'] = {
            'total_entities': sum(len(entities) for entities in all_entities_by_type.values()),
            'entities_by_type': {k: len(v) for k, v in all_entities_by_type.items()},
            'source_files_processed': len(entities_data)
        }
        
        # Save entity model
        model_file = self.models_dir / "entity_models" / f"consolidated_entities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        model_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(model_file, 'w', encoding='utf-8') as f:
                json.dump(entity_model, f, indent=2)
            results['entity_model_updated'] = True
            results['files_created'].append(str(model_file))
            logger.info(f"Created entity model: {model_file}")
        except Exception as e:
            logger.error(f"Error creating entity model: {e}")
        
        # Update main case hypergraph if it exists
        main_hypergraph = self.repo_root / "case_hypergraph.json"
        if main_hypergraph.exists():
            try:
                with open(main_hypergraph, 'r') as f:
                    hypergraph_data = json.load(f)
                
                # Add extracted entities to hypergraph
                if 'entities' not in hypergraph_data:
                    hypergraph_data['entities'] = {}
                
                for entity_type, entities in all_entities_by_type.items():
                    if entity_type not in hypergraph_data['entities']:
                        hypergraph_data['entities'][entity_type] = []
                    
                    # Add new entities (avoid duplicates)
                    existing_entities = set(hypergraph_data['entities'][entity_type])
                    new_entities = entities - existing_entities
                    hypergraph_data['entities'][entity_type].extend(list(new_entities))
                
                # Update metadata
                if 'metadata' not in hypergraph_data:
                    hypergraph_data['metadata'] = {}
                hypergraph_data['metadata']['last_auto_update'] = datetime.now().isoformat()
                
                # Save updated hypergraph
                with open(main_hypergraph, 'w') as f:
                    json.dump(hypergraph_data, f, indent=2)
                
                results['hypergraph_updated'] = True
                logger.info("Updated main hypergraph file")
                
            except Exception as e:
                logger.error(f"Error updating hypergraph: {e}")
        
        return results


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description='Automated Entity and Evidence Processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full processing of all changes
  python auto_entity_processor.py --mode full

  # Process only evidence files
  python auto_entity_processor.py --mode evidence

  # Process specific files
  python auto_entity_processor.py --mode custom --files evidence/doc1.md entities/person1.md
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['full', 'evidence', 'entities', 'timeline', 'models', 'custom'],
        default='full',
        help='Processing mode (default: full)'
    )
    
    parser.add_argument(
        '--files',
        nargs='*',
        help='Specific files to process (for custom mode)'
    )
    
    parser.add_argument(
        '--since-commit',
        help='Git commit hash to compare against for change detection'
    )
    
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory (default: current directory)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize processor
    processor = AutoEntityProcessor(args.output_dir)
    
    # Determine files to process
    if args.mode == 'custom' and args.files:
        files_to_process = {
            'evidence': [f for f in args.files if 'evidence' in f or f.endswith(('.md', '.json', '.txt'))],
            'entities': [f for f in args.files if 'entit' in f.lower()],
            'timeline': [f for f in args.files if 'timeline' in f.lower()],
            'models': [f for f in args.files if 'model' in f.lower()]
        }
    else:
        # Scan for changes
        files_to_process = processor.scan_for_changes(args.since_commit)
    
    # Filter files based on mode
    if args.mode != 'full':
        filtered_files = {args.mode: files_to_process.get(args.mode, [])}
        files_to_process = filtered_files
    
    # Process files
    results = {
        'processing_run': {
            'timestamp': datetime.now().isoformat(),
            'mode': args.mode,
            'files_processed': 0,
            'entities_created': 0,
            'timeline_events': 0,
            'models_updated': 0
        },
        'errors': []
    }
    
    try:
        # Process evidence files
        evidence_files = files_to_process.get('evidence', [])
        if evidence_files and (args.mode in ['full', 'evidence']):
            logger.info(f"Processing {len(evidence_files)} evidence files")
            evidence_results = processor.process_evidence_files(evidence_files)
            results['processing_run']['files_processed'] += len(evidence_results['processed_files'])
            results['errors'].extend(evidence_results['errors'])
            
            # Create entity files from extracted data
            if evidence_results['entities_extracted']:
                entities_created = processor.create_entity_files(evidence_results['entities_extracted'])
                results['processing_run']['entities_created'] += entities_created
                
                # Update timeline
                if args.mode in ['full', 'timeline']:
                    timeline_events = processor.update_timeline(evidence_results['entities_extracted'])
                    results['processing_run']['timeline_events'] += timeline_events
                
                # Update models
                if args.mode in ['full', 'models']:
                    model_results = processor.update_models(evidence_results['entities_extracted'])
                    if model_results['entity_model_updated'] or model_results['hypergraph_updated']:
                        results['processing_run']['models_updated'] += len(model_results['files_created'])
        
        # Generate summary
        summary_file = Path(args.output_dir) / "PROCESSING_SUMMARY.md"
        with open(summary_file, 'w') as f:
            f.write(f"""# Automated Processing Summary

## Processing Run Details
- **Timestamp**: {results['processing_run']['timestamp']}
- **Mode**: {results['processing_run']['mode']}
- **Files Processed**: {results['processing_run']['files_processed']}
- **Entities Created**: {results['processing_run']['entities_created']}
- **Timeline Events**: {results['processing_run']['timeline_events']}
- **Models Updated**: {results['processing_run']['models_updated']}

## Errors Encountered
""")
            if results['errors']:
                for error in results['errors']:
                    f.write(f"- {error}\n")
            else:
                f.write("None\n")
            
            f.write(f"""
## Next Steps
1. Review generated entity files in `entities/` directory
2. Check timeline updates in `03_timeline/entries/`
3. Validate model updates in `04_models/`
4. Manual review recommended for accuracy
""")
        
        # Save JSON results
        results_file = Path(args.output_dir) / "processing_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Processing complete. Summary saved to {summary_file}")
        
        # Exit with error code if there were errors
        return 1 if results['errors'] else 0
        
    except Exception as e:
        logger.error(f"Fatal error during processing: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())