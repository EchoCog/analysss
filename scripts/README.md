# Scripts Directory

This directory contains utility scripts for maintaining code quality, processing data, and automating workflows in the rzonedevops/analysis repository.

## Code Quality Scripts

### validate_emoji_syntax.py

Validates that all emoji characters in Python files are properly quoted as strings to prevent syntax errors.

**Usage:**
```bash
python3 scripts/validate_emoji_syntax.py
```

**What it checks:**
- Syntax errors caused by bare emoji characters (e.g., `print(🚀)` without quotes)
- Potential emoji usage issues in print statements
- Proper string quoting for all emoji characters

**Example output:**
```
🔍 Emoji Syntax Validator
============================================================
📁 Scanning: /home/runner/work/analysis/analysis

✅ Files checked: 211
✅ Files with issues: 0

============================================================
✅ SUCCESS: No emoji syntax issues found!
============================================================
```

**Integration:**
- Automatically runs via pre-commit hook
- Runs on every push via GitHub Actions
- Part of the continuous integration pipeline

**Why this matters:**
Python does not allow unescaped Unicode emoji literals. Using `print(🚀)` causes:
```
SyntaxError: invalid character '🚀' (U+1F680)
```

The correct usage is: `print("🚀")` or `print('🚀')`

See [Emoji Usage Guide](../docs/EMOJI_USAGE_GUIDE.md) for complete documentation.

### validate_codebase.py

Validates the overall codebase for common issues and best practices.

**Usage:**
```bash
python3 scripts/validate_codebase.py
```

## Data Processing Scripts

### auto_entity_processor.py

Automatically processes entities from evidence files and updates the entity database.

**Usage:**
```bash
python3 scripts/auto_entity_processor.py --mode [entities|evidence|timeline|models|full] --verbose
```

### auto_sync_on_commit.py

Synchronizes data across different components when commits are made.

**Usage:**
```bash
python3 scripts/auto_sync_on_commit.py
```

## Simulation Scripts

### run_agent_based_simulation.py

Runs agent-based model simulations using HyperGNN.

**Usage:**
```bash
python3 scripts/run_agent_based_simulation.py --case-id CASE_ID --output-dir sims
```

### run_discrete_event_simulation.py

Runs discrete event model simulations for case analysis.

**Usage:**
```bash
python3 scripts/run_discrete_event_simulation.py --case-id CASE_ID --output-dir sims
```

### run_system_dynamics_simulation.py

Runs system dynamics model simulations.

**Usage:**
```bash
python3 scripts/run_system_dynamics_simulation.py --case-id CASE_ID --output-dir sims
```

### run_integrated_simulation.py

Runs integrated multi-model simulations combining HyperGNN and Case-LLM.

**Usage:**
```bash
python3 scripts/run_integrated_simulation.py --case-id CASE_ID --output-dir sims
```

### generate_simulation_report.py

Generates comprehensive simulation reports from multiple simulation runs.

**Usage:**
```bash
python3 scripts/generate_simulation_report.py --results-dir RESULTS_DIR --case-id CASE_ID --output-dir sims
```

## Enhancement Scripts

### enhance_affidavits.py

Enhances affidavits with additional analysis and formatting.

**Usage:**
```bash
python3 scripts/enhance_affidavits.py
```

### integrate_refinements.py

Integrates refinements and updates across the codebase.

**Usage:**
```bash
python3 scripts/integrate_refinements.py
```

## Database Scripts

### run_migrations.py

Runs database migrations for schema updates.

**Usage:**
```bash
python3 scripts/run_migrations.py
```

## Best Practices

1. **Make scripts executable**: `chmod +x script_name.py`
2. **Use shebang**: Start scripts with `#!/usr/bin/env python3`
3. **Add docstrings**: Document what the script does
4. **Handle errors**: Use try/except blocks appropriately
5. **Validate input**: Check arguments and file existence
6. **Provide help**: Use argparse for command-line arguments
7. **Follow PEP 8**: Maintain consistent code style
8. **Test locally**: Run scripts locally before committing

## Running Scripts in CI/CD

Most scripts are integrated into GitHub Actions workflows:

- **validate-emoji-syntax.yml**: Runs emoji validation on every push
- **auto-entity-scan.yml**: Processes entities automatically
- **run-simulations.yml**: Executes simulations on demand

## Contributing

When adding new scripts:

1. Place them in this directory
2. Make them executable: `chmod +x script_name.py`
3. Add documentation to this README
4. Include usage examples
5. Add appropriate error handling
6. Follow existing script patterns
7. Test thoroughly before committing

## Troubleshooting

### Permission Denied

```bash
chmod +x scripts/script_name.py
```

### Module Not Found

```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Python Version Issues

All scripts require Python 3.11+:

```bash
python3 --version  # Should be 3.11 or higher
```

## Support

For issues or questions about scripts:
1. Check script documentation (docstrings)
2. Review this README
3. Check GitHub Actions logs
4. Open an issue on GitHub

## Related Documentation

- [Emoji Usage Guide](../docs/EMOJI_USAGE_GUIDE.md)
- [Testing Documentation](../TESTING.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Repository Structure](../REPOSITORY_STRUCTURE.md)
