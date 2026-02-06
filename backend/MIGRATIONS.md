# Database Migrations Guide

This document explains how to manage database migrations using Alembic.

## Initial Setup (Already Completed)

The database schema has been initialized with the following tables:
- **users**: Stores user accounts with UUID primary keys
- **tasks**: Stores tasks with foreign key relationships to users

Current migration version: **001** (Initial schema)

## Migration Commands

### Check Current Migration Version
```bash
cd backend
venv/Scripts/alembic.exe current
```

### View Migration History
```bash
cd backend
venv/Scripts/alembic.exe history
```

### Apply All Pending Migrations
```bash
cd backend
venv/Scripts/alembic.exe upgrade head
```

### Rollback One Migration
```bash
cd backend
venv/Scripts/alembic.exe downgrade -1
```

### Rollback to Specific Version
```bash
cd backend
venv/Scripts/alembic.exe downgrade <revision_id>
```

## Creating New Migrations

### Auto-generate Migration from Model Changes

1. **Modify your SQLModel models** in `src/models/`

2. **Generate migration**:
   ```bash
   cd backend
   venv/Scripts/alembic.exe revision --autogenerate -m "Description of changes"
   ```

3. **Review the generated migration** in `alembic/versions/`
   - Check that the upgrade() and downgrade() functions are correct
   - Add any custom logic if needed

4. **Apply the migration**:
   ```bash
   venv/Scripts/alembic.exe upgrade head
   ```

### Create Empty Migration (Manual)

For complex changes that can't be auto-generated:

```bash
cd backend
venv/Scripts/alembic.exe revision -m "Description of changes"
```

Then edit the generated file to add your custom migration logic.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(500) NOT NULL,
    description VARCHAR(5000),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes
- `ix_users_id` on users(id)
- `ix_users_email` on users(email) - UNIQUE
- `ix_tasks_user_id` on tasks(user_id)

## Configuration

### Environment Variables

Alembic reads the database URL from the `.env` file:

```env
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
```

### Alembic Configuration Files

- **alembic.ini**: Main configuration file
- **alembic/env.py**: Environment setup and model imports
- **alembic/versions/**: Migration scripts directory

## Troubleshooting

### Migration Fails with "relation already exists"

If tables already exist in the database:
1. Check current migration state: `alembic current`
2. If no migrations are applied, the database may have been created manually
3. Option 1: Drop all tables and rerun migrations
4. Option 2: Mark the current migration as applied without running it:
   ```bash
   alembic stamp head
   ```

### Type Mismatch Errors

If you get foreign key type mismatch errors:
- Ensure all foreign key columns match the type of their referenced columns
- UUID columns must reference UUID columns
- Integer columns must reference Integer columns

### Import Errors in env.py

If Alembic can't import your models:
- Check that `sys.path` is correctly set in `alembic/env.py`
- Ensure all model files are imported in `env.py`
- Verify that the virtual environment is activated

## Best Practices

1. **Always review auto-generated migrations** before applying them
2. **Test migrations on a development database** before production
3. **Create a database backup** before running migrations in production
4. **Keep migrations small and focused** - one logical change per migration
5. **Never edit applied migrations** - create a new migration to fix issues
6. **Document complex migrations** with comments in the migration file

## Production Deployment

When deploying to production:

1. **Backup the database**:
   ```bash
   # Use your database provider's backup tools
   ```

2. **Apply migrations**:
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   alembic upgrade head
   ```

3. **Verify migration success**:
   ```bash
   alembic current
   ```

4. **If migration fails**, rollback:
   ```bash
   alembic downgrade -1
   ```

5. **Restore from backup if needed**

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
