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
PG_ISREADY="/opt/homebrew/opt/postgresql@15/bin/pg_isready"
if ! $PG_ISREADY -h localhost -p 5432 > /dev/null 2>&1; then
    echo "Starting PostgreSQL..."
    brew services start postgresql@15
    MAX_RETRIES=30
    RETRY_COUNT=0
    until $PG_ISREADY -h localhost -p 5432 > /dev/null 2>&1 || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
        echo "Waiting for PostgreSQL to be ready..."
        sleep 1
        RETRY_COUNT=$((RETRY_COUNT+1))
    done
    if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
        echo "Error: PostgreSQL failed to start after $MAX_RETRIES attempts"
        exit 1
    fi
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
