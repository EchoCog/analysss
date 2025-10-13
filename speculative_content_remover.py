#!/usr/bin/env python3
"""
Speculative Content Remover
Removes or flags speculative claims and replaces with fact-based statements
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple
import json


class SpeculativeContentRemover:
    """Tool to identify and remove/replace speculative content with facts"""
    
    def __init__(self):
        self.workspace_path = Path(".")
        
        # Patterns for content that needs revision or removal
        self.problematic_patterns = [
            # Damage claims without documented basis
            (r'- Damages exceeding R ([0-9,]+(?:,000)?)', 'REMOVE_UNFOUNDED_DAMAGES'),
            (r'R ([0-9,]+)\+ in damages', 'REMOVE_UNFOUNDED_DAMAGES'),
            (r'civil damages: R ([0-9,]+)', 'REMOVE_UNFOUNDED_DAMAGES'),
            (r'punitive damages.*R ([0-9,]+)', 'REMOVE_UNFOUNDED_DAMAGES'),
            
            # Speculative language to replace
            (r'\bmight\b', 'FLAG_SPECULATION'),
            (r'\bcould\b', 'FLAG_SPECULATION'),
            (r'\bpossibly\b', 'FLAG_SPECULATION'),
            (r'\bperhaps\b', 'FLAG_SPECULATION'),
            (r'\bmaybe\b', 'FLAG_SPECULATION'),
            (r'\bestimated?\b', 'FLAG_SPECULATION'),
            (r'\bapproximately\b', 'FLAG_SPECULATION'),
            (r'\bprojected?\b', 'FLAG_SPECULATION'),
            (r'\bguesstimates?\b', 'FLAG_SPECULATION'),
            
            # Weak evidence language
            (r'\bit appears that\b', 'WEAK_EVIDENCE'),
            (r'\bit seems\b', 'WEAK_EVIDENCE'),
            (r'\blikely that\b', 'WEAK_EVIDENCE'),
            (r'\bprobably\b', 'WEAK_EVIDENCE'),
            (r'\bpresumed?\b', 'WEAK_EVIDENCE'),
            (r'\barguably\b', 'WEAK_EVIDENCE'),
        ]
        
        # Replacement patterns for fact-based language
        self.fact_based_replacements = {
            'might': 'can (subject to documented evidence)',
            'could': 'can (per documented records)',
            'possibly': 'per available documentation',
            'perhaps': 'according to recorded evidence',
            'maybe': 'per documented sources',
            'estimated': 'documented as',
            'approximately': 'recorded as',
            'projected': 'documented',
            'guesstimates': 'documented figures',
            'it appears that': 'documented evidence shows',
            'it seems': 'records indicate',
            'likely that': 'documented evidence supports that',
            'probably': 'per documented evidence',
            'presumed': 'documented',
            'arguably': 'based on documented evidence',
        }
    
    def analyze_file_for_speculation(self, file_path: str) -> Dict:
        """Analyze a file for speculative content"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e)}
        
        issues = {
            'file': file_path,
            'total_issues': 0,
            'damage_claims': [],
            'speculative_language': [],
            'weak_evidence': [],
            'suggested_removals': [],
            'suggested_replacements': []
        }
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern, issue_type in self.problematic_patterns:
                matches = list(re.finditer(pattern, line, re.IGNORECASE))
                for match in matches:
                    issues['total_issues'] += 1
                    
                    issue_data = {
                        'line_number': i,
                        'line_content': line.strip(),
                        'match': match.group(),
                        'pattern': pattern,
                        'start': match.start(),
                        'end': match.end()
                    }
                    
                    if issue_type == 'REMOVE_UNFOUNDED_DAMAGES':
                        issues['damage_claims'].append(issue_data)
                        issues['suggested_removals'].append({
                            'line': i,
                            'reason': 'Unfounded damage claim without documented basis',
                            'content': line.strip()
                        })
                    elif issue_type == 'FLAG_SPECULATION':
                        issues['speculative_language'].append(issue_data)
                        # Suggest replacement
                        word = match.group().lower()
                        if word in self.fact_based_replacements:
                            issues['suggested_replacements'].append({
                                'line': i,
                                'original': match.group(),
                                'suggested': self.fact_based_replacements[word],
                                'reason': 'Replace speculative language with fact-based statement'
                            })
                    elif issue_type == 'WEAK_EVIDENCE':
                        issues['weak_evidence'].append(issue_data)
        
        return issues
    
    def create_fact_based_version(self, file_path: str, output_path: str = None) -> str:
        """Create a fact-based version of a file with speculative content removed/replaced"""
        
        if not output_path:
            path_obj = Path(file_path)
            output_path = str(path_obj.parent / f"{path_obj.stem}_FACT_BASED{path_obj.suffix}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return f"Error reading file: {e}"
        
        # Track changes made
        changes_made = []
        
        # First, remove lines with unfounded damage claims
        lines = content.split('\n')
        filtered_lines = []
        
        for i, line in enumerate(lines):
            should_remove = False
            
            # Check for unfounded damage claims
            damage_patterns = [
                r'- Damages exceeding R [0-9,]+',
                r'R [0-9,]+\+ in damages',
                r'Payment of R [0-9,]+\+ in damages',
                r'businesses worth R [0-9,]+\+',
                r'systematic criminal enterprise.*R [0-9,]+\+',
            ]
            
            for pattern in damage_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    should_remove = True
                    changes_made.append(f"REMOVED Line {i+1}: Unfounded damage claim - {line.strip()}")
                    break
            
            if not should_remove:
                # Replace speculative language
                modified_line = line
                for word, replacement in self.fact_based_replacements.items():
                    if re.search(r'\b' + word + r'\b', modified_line, re.IGNORECASE):
                        old_line = modified_line
                        modified_line = re.sub(r'\b' + word + r'\b', replacement, modified_line, flags=re.IGNORECASE)
                        if old_line != modified_line:
                            changes_made.append(f"REPLACED Line {i+1}: '{word}' -> '{replacement}'")
                
                filtered_lines.append(modified_line)
        
        # Join the filtered content
        revised_content = '\n'.join(filtered_lines)
        
        # Add header explaining the revision
        revision_header = f"""<!-- FACT-BASED REVISION NOTICE -->
<!-- This document has been revised to remove speculative claims and unfounded projections -->
<!-- Changes made: {len(changes_made)} modifications -->
<!-- Standard: Only documented facts and exact recorded figures included -->
<!-- Generated: {Path(file_path).name} -> {Path(output_path).name} -->

"""
        
        final_content = revision_header + revised_content
        
        # Write the fact-based version
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        # Create change log
        change_log = f"""# Fact-Based Revision Log - {Path(file_path).name}

## Changes Made: {len(changes_made)}

"""
        for change in changes_made:
            change_log += f"- {change}\n"
        
        change_log += f"""
## Revision Standards Applied:
1. Removed unfounded damage claims without documented basis
2. Replaced speculative language with fact-based statements
3. Eliminated estimates and projections without source evidence
4. Focused on documented facts and exact recorded figures only

Original file: {file_path}
Revised file: {output_path}
"""
        
        log_path = str(Path(output_path).parent / f"{Path(file_path).stem}_REVISION_LOG.md")
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(change_log)
        
        return output_path
    
    def generate_speculation_report(self) -> Dict:
        """Generate comprehensive report on speculative content across repository"""
        
        results = {
            'total_files_analyzed': 0,
            'files_with_issues': 0,
            'total_issues': 0,
            'worst_offenders': [],
            'file_analyses': {}
        }
        
        # Analyze key markdown files
        md_files = list(self.workspace_path.glob('*.md'))
        
        for md_file in md_files:
            if md_file.name.startswith('.'):
                continue
                
            analysis = self.analyze_file_for_speculation(str(md_file))
            
            if 'error' in analysis:
                continue
                
            results['total_files_analyzed'] += 1
            
            if analysis['total_issues'] > 0:
                results['files_with_issues'] += 1
                results['total_issues'] += analysis['total_issues']
                results['file_analyses'][md_file.name] = analysis
                
                # Track worst offenders
                if analysis['total_issues'] >= 5:
                    results['worst_offenders'].append({
                        'file': md_file.name,
                        'issues': analysis['total_issues'],
                        'damage_claims': len(analysis['damage_claims']),
                        'speculative_language': len(analysis['speculative_language'])
                    })
        
        # Sort worst offenders by issue count
        results['worst_offenders'].sort(key=lambda x: x['issues'], reverse=True)
        
        return results


def main():
    """Main execution function"""
    remover = SpeculativeContentRemover()
    
    print("=== SPECULATIVE CONTENT REMOVER ===")
    print("Analyzing repository for speculative claims and unfounded projections...")
    
    # Generate comprehensive report
    report = remover.generate_speculation_report()
    
    print(f"\n=== ANALYSIS RESULTS ===")
    print(f"Files analyzed: {report['total_files_analyzed']}")
    print(f"Files with speculative content: {report['files_with_issues']}")
    print(f"Total speculative issues: {report['total_issues']}")
    
    # Show worst offenders
    if report['worst_offenders']:
        print(f"\n=== WORST OFFENDERS (5+ issues) ===")
        for offender in report['worst_offenders'][:10]:  # Top 10
            print(f"- {offender['file']}: {offender['issues']} issues ({offender['damage_claims']} damage claims)")
    
    # Create fact-based versions of worst offenders
    print(f"\n=== CREATING FACT-BASED VERSIONS ===")
    for offender in report['worst_offenders'][:5]:  # Top 5 only
        original_path = offender['file']
        print(f"Processing {original_path}...")
        
        try:
            fact_based_path = remover.create_fact_based_version(original_path)
            print(f"✅ Created fact-based version: {fact_based_path}")
        except Exception as e:
            print(f"❌ Error processing {original_path}: {e}")
    
    # Save detailed report
    report_file = "speculative_content_analysis.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n✅ Detailed analysis saved to: {report_file}")
    
    return report


if __name__ == "__main__":
    main()