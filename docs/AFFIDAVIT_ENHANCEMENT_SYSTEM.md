# Affidavit Enhancement System

## Overview

The Affidavit Enhancement System is a comprehensive solution for automatically updating and refining legal affidavits based on the present state of the evidence base. It continuously monitors evidence files and applies relevant updates to affidavits while preserving document integrity and legal formatting.

## Features

### 🤖 Automatic Enhancement
- **Evidence Monitoring**: Continuously scans evidence directories for changes
- **Smart Analysis**: Identifies relevant evidence updates for specific affidavits
- **Priority-Based Processing**: Processes critical updates first
- **Backup Creation**: Automatically creates backups before modifications

### 📝 Document Processing
- **Multiple Formats**: Supports Markdown (.md) and Word (.docx) affidavits
- **Format Preservation**: Maintains original document formatting and structure
- **Section-Aware**: Intelligently places updates in appropriate affidavit sections
- **Metadata Tracking**: Adds comprehensive enhancement metadata

### 🔧 GitHub Actions Integration
- **Automated Workflows**: Triggers on evidence changes via GitHub Actions
- **Pull Request Support**: Provides enhancement previews for PR reviews
- **Issue Creation**: Automatically creates issues for critical evidence updates
- **Validation**: Includes comprehensive validation and quality checks

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Evidence Repository                       │
├─────────────────┬───────────────────┬────────────────────────┤
│   Evidence      │   Case Files      │   Analysis Reports     │
│   Documents     │   & Affidavits    │   & Summaries         │
└─────────────────┴───────────────────┴────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Evidence Change Detection                    │
│  • File modification monitoring                             │
│  • Content analysis for relevance                          │
│  • Priority assessment based on keywords                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Affidavit Enhancement Engine                │
│  • Discovery of affidavit files                           │
│  • Update extraction and processing                       │
│  • Section-aware content insertion                        │
│  • Format-specific enhancement logic                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Generation                        │
│  • Enhanced affidavit creation                             │
│  • Backup file management                                  │
│  • Enhancement reporting                                   │
│  • Quality validation                                      │
└─────────────────────────────────────────────────────────────┘
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- Required packages: `python-docx`, `PyPDF2`, `Pillow`
- Git repository with evidence and affidavit files

### Installation

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd analysis
   ```

2. **Install Dependencies**
   ```bash
   pip install python-docx PyPDF2 Pillow
   ```

3. **Configure System**
   ```bash
   # Copy and customize configuration
   cp config/affidavit_enhancement.json.example config/affidavit_enhancement.json
   ```

4. **Test Installation**
   ```bash
   python -m pytest tests/test_affidavit_enhancement.py -v
   ```

## Configuration

### Configuration File Structure

```json
{
  "affidavit_patterns": [
    "*AFFIDAVIT*.md",
    "*affidavit*.md", 
    "*AFFIDAVIT*.docx",
    "*affidavit*.docx"
  ],
  "evidence_patterns": [
    "evidence/**/*.md",
    "case_*/analysis/*.md",
    "*EVIDENCE*.md"
  ],
  "critical_keywords": [
    "fraud", "perjury", "murder", "criminal", 
    "evidence", "witness intimidation"
  ],
  "priority_indicators": {
    "critical": ["murder", "perjury", "smoking gun"],
    "high": ["fraud", "new evidence", "witness intimidation"],
    "medium": ["analysis reveals", "documents show"]
  },
  "backup_settings": {
    "backup_on_change": true,
    "retention_days": 90
  },
  "output_settings": {
    "backup_dir": "backups/affidavits",
    "output_dir": "enhanced_affidavits"
  }
}
```

### Key Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `affidavit_patterns` | File patterns to identify affidavits | `["*AFFIDAVIT*.md", "*affidavit*.md"]` |
| `evidence_patterns` | File patterns for evidence sources | `["evidence/**/*.md"]` |
| `critical_keywords` | Keywords indicating critical updates | `["fraud", "murder", "criminal"]` |
| `backup_on_change` | Create backups before modification | `true` |
| `preserve_formatting` | Maintain document formatting | `true` |

## Usage

### Manual Enhancement

```bash
# Basic enhancement of all affidavits
python scripts/enhance_affidavits.py --verbose

# Process only critical/high priority updates
python scripts/enhance_affidavits.py --priority-filter critical,high

# Analyze changes since specific date
python scripts/enhance_affidavits.py --since "2025-01-01T00:00:00"

# Dry run (analyze without modifying files)
python scripts/enhance_affidavits.py --dry-run --verbose

# Generate analysis report only
python scripts/enhance_affidavits.py --report-only
```

### Programmatic Usage

```python
from src.affidavit_enhancement.affidavit_processor import AffidavitProcessor

# Initialize processor
processor = AffidavitProcessor("config/affidavit_enhancement.json")

# Process all affidavits
results = processor.process_all_affidavits()

# Generate report
report = processor.generate_enhancement_report(results)
print(report)
```

### GitHub Actions Integration

The system automatically triggers via GitHub Actions when:

- Evidence files are modified (`evidence/**`)
- Case analysis files are updated (`case_*/analysis/**`)
- Affidavit files are changed
- Manual workflow dispatch is triggered

#### Workflow Features

1. **Change Detection**: Identifies which files have been modified
2. **Evidence Analysis**: Analyzes evidence changes for relevance and priority
3. **Enhancement Processing**: Applies updates to relevant affidavits
4. **Validation**: Verifies enhancement quality and integrity
5. **Issue Creation**: Creates GitHub issues for critical updates
6. **Artifact Management**: Uploads enhanced files as artifacts

## Enhancement Process

### 1. Evidence Discovery

The system scans for evidence files matching configured patterns:

```python
evidence_patterns = [
    "evidence/**/*.md",
    "case_*/analysis/*.md", 
    "*EVIDENCE*.md"
]
```

### 2. Relevance Assessment

Evidence files are evaluated for relevance using:
- **Critical Keywords**: Fraud, murder, criminal, etc.
- **Pattern Matching**: Regular expressions for legal terms
- **Context Analysis**: Section and content analysis

### 3. Priority Determination

Updates are prioritized based on content analysis:

| Priority | Indicators | Processing |
|----------|------------|------------|
| **Critical** | Murder, perjury, smoking gun evidence | Immediate processing, issue creation |
| **High** | Fraud, new evidence, witness intimidation | High-priority processing |
| **Medium** | General analysis, document updates | Standard processing |
| **Low** | Minor corrections, formatting | Background processing |

### 4. Section Mapping

Updates are intelligently placed in appropriate affidavit sections:

| Evidence Type | Target Section |
|---------------|----------------|
| Background/History | Introduction/Background |
| New Evidence | Evidence Analysis |
| Timeline Events | Chronology/Timeline |
| Financial Data | Financial Evidence |
| Regulatory Issues | Compliance/Regulatory |
| Criminal Charges | Criminal Evidence |

### 5. Enhancement Application

Different enhancement types are handled specifically:

#### New Evidence
```markdown
## ENHANCED EVIDENCE ANALYSIS (Added 2025-01-15)

### New Evidence from critical_fraud_evidence.md

- Evidence shows systematic embezzlement over 5 years
- Documents confirm R10 million fraudulent transfers
- Analysis reveals coordinated criminal conspiracy

**Source**: evidence/critical_fraud_evidence.md
**Priority**: CRITICAL
**Date Added**: 2025-01-15
```

#### Corrections
```markdown
## CORRECTION NOTICE (Applied 2025-01-15)

**Source**: correction_evidence.md
**Priority**: HIGH

**Correction Details**:
- Previous statement regarding dates corrected
- Updated timeline based on new documentation
- Clarified regulatory compliance violations
```

#### Enhancements
Existing sections are enhanced with additional supporting information while preserving original content.

## File Management

### Directory Structure

```
project/
├── enhanced_affidavits/          # Enhanced affidavit outputs
│   ├── affidavit_enhanced.md
│   └── comprehensive_affidavit_enhanced.docx
├── backups/affidavits/          # Original file backups
│   ├── affidavit_backup_20250115_143022.md
│   └── comprehensive_backup_20250115_143045.docx
├── evidence/                    # Evidence source files
├── case_*/analysis/            # Case-specific analysis
└── reports/                    # Enhancement reports
    └── AFFIDAVIT_ENHANCEMENT_REPORT.md
```

### Backup Strategy

- **Automatic Backups**: Created before any modification
- **Timestamp Naming**: `{filename}_backup_{timestamp}{extension}`
- **Retention Policy**: Configurable retention period (default: 90 days)
- **Integrity Checks**: Backup verification before processing

## Quality Assurance

### Validation Checks

1. **Document Integrity**: Structure and formatting preservation
2. **Content Validation**: Enhancement accuracy and relevance  
3. **Backup Verification**: Successful backup creation
4. **Output Quality**: Enhanced file generation and accessibility

### Error Handling

- **Graceful Degradation**: Continue processing other files on individual failures
- **Detailed Logging**: Comprehensive error logging and reporting
- **Recovery Mechanisms**: Automatic backup restoration on critical failures
- **Validation Reporting**: Clear success/failure reporting

## Security Considerations

### Data Protection

- **No External Transmission**: All processing occurs locally
- **Backup Security**: Secure backup file handling
- **Access Controls**: Respect existing file permissions
- **Audit Trail**: Comprehensive change logging

### Legal Compliance

- **Document Integrity**: Maintains legal document structure
- **Change Tracking**: Clear attribution of all modifications
- **Version Control**: Integration with Git for change history
- **Professional Standards**: Adherence to legal document standards

## Monitoring & Reporting

### Enhancement Reports

Generated reports include:
- **Processing Summary**: Files processed and results
- **Evidence Analysis**: Source evidence and priority assessment
- **Enhancement Details**: Specific changes made to each affidavit
- **Quality Metrics**: Validation results and statistics
- **Recommendations**: Suggested next steps and manual review requirements

### GitHub Integration

- **Workflow Status**: Clear success/failure indication
- **Artifact Uploads**: Enhanced files available for download
- **Issue Management**: Automatic issue creation for critical updates
- **PR Comments**: Enhancement summaries on pull requests

## Troubleshooting

### Common Issues

1. **No Affidavits Found**
   - Check `affidavit_patterns` configuration
   - Verify file naming conventions
   - Ensure files are in the correct directory

2. **No Evidence Updates Detected**
   - Review `evidence_patterns` configuration
   - Check file modification timestamps
   - Verify content contains relevant keywords

3. **Enhancement Failures**
   - Check file permissions
   - Verify document format compatibility
   - Review error logs for specific issues

4. **Backup Creation Failures**
   - Ensure backup directory exists and is writable
   - Check available disk space
   - Verify file access permissions

### Debugging

Enable verbose logging for detailed troubleshooting:

```bash
python scripts/enhance_affidavits.py --verbose --dry-run
```

Review log files:
```bash
tail -f affidavit_enhancement.log
```

### Support

- **Documentation**: Comprehensive guides in `/docs`
- **Test Suite**: Validation via `tests/test_affidavit_enhancement.py`
- **Configuration Examples**: Sample configs in `/config`
- **Issue Tracking**: GitHub Issues for bug reports and feature requests

## Future Enhancements

### Planned Features

- **AI-Powered Analysis**: Machine learning for evidence relevance assessment
- **Cross-Reference Validation**: Automatic fact-checking across documents
- **Template Management**: Standardized affidavit templates
- **Multi-Language Support**: International legal document support
- **Advanced Formatting**: Enhanced Word document formatting capabilities
- **Collaboration Features**: Multi-user review and approval workflows

### Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` for guidelines on:
- Code standards and testing requirements
- Documentation expectations  
- Pull request process
- Issue reporting procedures

---

## Quick Start Example

```bash
# 1. Setup
git clone <repository-url>
cd analysis
pip install python-docx PyPDF2 Pillow

# 2. Configure (optional - uses defaults if not configured)
cp config/affidavit_enhancement.json.example config/affidavit_enhancement.json

# 3. Test the system
python scripts/enhance_affidavits.py --dry-run --verbose

# 4. Run enhancement
python scripts/enhance_affidavits.py --verbose

# 5. Review results
ls enhanced_affidavits/
cat AFFIDAVIT_ENHANCEMENT_REPORT.md
```

The system is now ready to automatically enhance your affidavits based on evidence updates!