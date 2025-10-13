# Auto Entity and Evidence Scan GitHub Action

## Overview

The **Auto Entity and Evidence Scan** GitHub Action automatically processes new and updated entities, relations, events, timelines, stocks, flows, and other data elements in the analysis repository. It provides intelligent automation for evidence processing, entity extraction, and model updates.

## Features

### 🔍 Automatic Change Detection
- Monitors changes to evidence files (`evidence/**`)
- Tracks entity updates (`entities/**`)
- Watches timeline modifications (`03_timeline/**`)
- Observes model changes (`04_models/**`)
- Detects case-specific updates (`case_*/**`)

### 📊 Processing Capabilities
- **Evidence Processing**: Extracts entities and relationships from documents
- **Entity Management**: Creates and updates individual entity files
- **Timeline Integration**: Consolidates timeline events and updates
- **Model Synchronization**: Updates hypergraph and other analytical models
- **Cross-validation**: Ensures consistency across all data sources

### ⚙️ Flexible Triggering
- **Push Events**: Automatic processing on main/develop branch pushes
- **Pull Requests**: Validation and processing for PR reviews
- **Manual Dispatch**: On-demand processing with customizable options

## Workflow Jobs

### 1. **detect-changes**
Analyzes git diff to identify which types of files have changed:
- Evidence files (`.md`, `.json`, `.txt`, `.pdf`, etc.)
- Entity definitions and profiles
- Timeline entries and events
- Model files and configurations

### 2. **process-evidence**
Processes evidence files using the evidence automation pipeline:
- Extracts text content from various file formats
- Runs entity recognition and extraction
- Integrates with existing evidence management system
- Produces structured output for downstream processing

### 3. **process-entities**
Manages entity creation and updates:
- Creates individual entity profile files
- Extracts entities from document text using pattern matching
- Updates entity relationships and cross-references
- Maintains entity database consistency

### 4. **process-timeline**
Handles timeline processing and integration:
- Consolidates timeline entries from multiple sources
- Updates timeline database with new events
- Cross-references timeline data with entity information
- Generates timeline correlation analysis

### 5. **update-models**
Updates analytical models and hypergraph structures:
- Integrates processed data into hypergraph models
- Updates entity and relationship models
- Generates consolidated analysis reports
- Maintains model version history

## Usage

### Automatic Triggering

The action automatically runs when:
```yaml
# On pushes to main branches
push:
  branches: [ main, develop ]
  paths:
    - 'evidence/**'
    - 'entities/**'
    - '03_timeline/**'
    - '04_models/**'
    - 'case_*/**'
    - '*.md'
    - '*.json'

# On pull requests
pull_request:
  branches: [ main ]
```

### Manual Triggering

You can manually trigger the workflow with custom options:

1. Go to **Actions** tab in your GitHub repository
2. Select **Auto Entity and Evidence Scan**
3. Click **Run workflow**
4. Choose your options:
   - **Scan Mode**: `incremental`, `full_scan`, `evidence_only`, `entities_only`
   - **Force Rebuild**: Whether to rebuild all models regardless of changes

### Scan Modes

- **`incremental`** (default): Process only changed files
- **`full_scan`**: Process all files in the repository
- **`evidence_only`**: Process only evidence files
- **`entities_only`**: Process only entity-related files

## Configuration

### Environment Variables

The action automatically uses repository secrets and environment variables:
- GitHub token for API access (automatically provided)
- Repository context for change detection

### Dependencies

The action automatically installs required dependencies:
```bash
pip install -e .[dev]
pip install python-docx PyPDF2 eml-parser  # Additional evidence processing
```

## Outputs and Artifacts

### Artifacts Created

1. **Evidence Processing Results** (30-day retention)
   - Extracted entity data
   - Processing logs and reports
   - Evidence metadata

2. **Entity Processing Results** (30-day retention)
   - Generated entity files
   - Entity extraction summaries
   - Cross-reference data

3. **Timeline Processing Results** (30-day retention)
   - Consolidated timeline files
   - Event correlation data
   - Timeline visualization data

4. **Complete Processing Results** (90-day retention)
   - Final integrated results
   - Processing summary report
   - Updated model files

### Generated Files

- **`entities/*.md`**: Individual entity profile files
- **`03_timeline/entries/*.json`**: Timeline event files
- **`04_models/*.json`**: Updated analytical models
- **`PROCESSING_SUMMARY.md`**: Human-readable processing report
- **`processing_summary.json`**: Machine-readable results

## Integration with Pull Requests

When run on pull requests, the action:
- Posts a comment with processing results
- Shows detected changes and their impact
- Provides validation feedback
- Includes processing summary

## Error Handling

The action includes comprehensive error handling:
- Individual job failures don't stop the entire workflow
- Processing errors are logged and reported
- Partial results are preserved even if some processing fails
- Detailed error messages help with troubleshooting

## Performance Considerations

### Optimization Features
- **Incremental Processing**: Only processes changed files by default
- **Parallel Job Execution**: Multiple processing jobs run simultaneously
- **Efficient Change Detection**: Uses git diff for precise change identification
- **Smart Caching**: Leverages GitHub Actions caching for dependencies

### Resource Usage
- **Processing Time**: 2-15 minutes depending on changes
- **Storage**: Artifacts retained for 30-90 days
- **Compute**: Moderate CPU usage for text processing and analysis

## Troubleshooting

### Common Issues

1. **Processing Timeout**
   - Increase timeout values in workflow file
   - Use `evidence_only` mode for large repositories
   - Check for malformed files causing processing delays

2. **Memory Issues**
   - Process files in smaller batches
   - Use incremental mode instead of full scan
   - Check for very large files in evidence directory

3. **Permission Errors**
   - Ensure workflow has proper repository permissions
   - Check if files are properly accessible
   - Verify GitHub token has required scopes

### Debug Mode

Enable verbose logging by using manual dispatch with debug options or by modifying the workflow to include:
```bash
python scripts/auto_entity_processor.py --mode full --verbose
```

## Monitoring

### Success Indicators
- All jobs complete without errors
- Processing summary generated successfully
- Artifact uploads complete
- Entity files created/updated as expected

### Failure Indicators
- Job failures in workflow run
- Missing expected artifacts
- Processing summary shows errors
- Entity extraction yields no results

## Security Considerations

- Action runs in isolated GitHub Actions environment
- No external API calls or data transmission
- All processing happens within the repository context
- Generated files follow repository access controls

## Future Enhancements

Planned improvements include:
- Integration with external evidence management systems
- Advanced entity relationship detection
- Machine learning-based entity classification
- Real-time processing notifications
- Enhanced visualization of processing results

## Support

For issues or questions:
1. Check the workflow run logs in GitHub Actions
2. Review the processing summary for detailed error information
3. Examine artifact contents for partial results
4. Create an issue in the repository for persistent problems

## Related Documentation

- [Entity Management Guide](./entity-management.md)
- [Evidence Processing Pipeline](./evidence-processing.md)
- [Timeline Processing Workflow](./timeline-processing.md)
- [Model Integration Guidelines](./model-integration.md)