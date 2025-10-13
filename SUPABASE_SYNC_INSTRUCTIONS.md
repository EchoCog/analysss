# Supabase Database Synchronization Instructions

## Overview

The Neon database has been successfully updated with new schema improvements. To maintain synchronization, the same schema changes need to be applied to Supabase.

## New Tables Added

The following tables have been added to track repository improvements and automation:

1. **sync_operations** - Tracks all database synchronization operations
2. **database_migrations** - Records migration history and status
3. **repository_changes** - Logs git changes requiring database sync
4. **workflow_runs** - Tracks CI/CD workflow execution
5. **code_quality_metrics** - Stores test coverage and quality metrics

## Method 1: Using Supabase Dashboard (Recommended)

1. **Login to Supabase Dashboard**
   - Navigate to: https://app.supabase.com
   - Select your project

2. **Open SQL Editor**
   - Click on "SQL Editor" in the left sidebar
   - Click "New Query"

3. **Execute Schema Migration**
   - Copy the contents of `database_improvements_simple.sql`
   - Paste into the SQL Editor
   - Click "Run" to execute

4. **Verify Tables**
   - Go to "Table Editor"
   - Confirm the 5 new tables are present

## Method 2: Using Supabase CLI

### Prerequisites
```bash
# Install Supabase CLI
npm install -g supabase

# Login to Supabase
supabase login
```

### Link Project
```bash
# Link to your Supabase project
supabase link --project-ref YOUR_PROJECT_REF
```

### Apply Migration
```bash
# Create migration file
supabase migration new add_sync_tracking_tables

# Copy SQL content to the migration file
cp database_improvements_simple.sql supabase/migrations/TIMESTAMP_add_sync_tracking_tables.sql

# Push to Supabase
supabase db push
```

## Method 3: Using API (Automated)

The repository includes automated sync scripts that will handle this when properly configured:

```bash
# Configure environment
export SUPABASE_URL="your-project-url"
export SUPABASE_KEY="your-anon-key"

# Run sync script
python scripts/run_migrations.py --file database_improvements_simple.sql
```

## Verification

After applying the migration, verify the tables exist:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN (
    'sync_operations',
    'database_migrations',
    'repository_changes',
    'workflow_runs',
    'code_quality_metrics'
  )
ORDER BY table_name;
```

Expected result: 5 rows

## CI/CD Automation

The GitHub workflow `.github/workflows/database-sync.yml` will automatically handle future synchronization when:

1. Database schema files are modified
2. Evidence or entity files are added
3. Manual workflow dispatch is triggered

### Setup CI/CD Sync

Add these secrets to your GitHub repository:

1. Go to: Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase service role key
   - `NEON_CONNECTION_STRING` - Your Neon connection string

## Troubleshooting

### Issue: Permission Denied

**Solution**: Ensure you're using the service role key, not the anon key.

### Issue: Table Already Exists

**Solution**: The SQL uses `CREATE TABLE IF NOT EXISTS`, so this is safe. If you see this, the tables already exist.

### Issue: Foreign Key Constraint Errors

**Solution**: Ensure all referenced tables exist before creating tables with foreign keys.

## Next Steps

After synchronizing Supabase:

1. ✅ Both databases (Neon and Supabase) will have identical schemas
2. ✅ Automated sync workflows will keep them synchronized
3. ✅ Repository changes will automatically trigger database updates
4. ✅ CI/CD pipelines will track and log all operations

## Support

If you encounter issues:

1. Check the Supabase logs in the Dashboard
2. Review the migration SQL for syntax errors
3. Ensure your Supabase project has sufficient permissions
4. Contact support via GitHub Issues

---

**Status**: Neon database updated ✅ | Supabase pending manual sync ⏳

