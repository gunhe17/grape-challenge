#!/bin/bash

set -e

# Load .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Use environment variables with defaults
POSTGRES_USER=${POSTGRES_USER:-dev_user}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-dev_password}
POSTGRES_DB=${POSTGRES_DB:-grape_dev}

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "Starting PostgreSQL..."
    brew services start postgresql@15
    sleep 2
fi

# Create user if not exists
psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_USER'" | grep -q 1 || \
    psql postgres -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"

# Create database if not exists
psql postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'" | grep -q 1 || \
    psql postgres -c "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"

# Grant privileges
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;" > /dev/null 2>&1

echo "✓ Dev database setup complete"
