#!/bin/bash
set -e

# Initialize the database if it does not exist
if [ ! -s "/var/lib/postgresql/data/PG_VERSION" ]; then
    echo "Database not found, initializing..."
    pg_ctl init -D /var/lib/postgresql/data
fi

# Modify PostgreSQL configurations to allow local connections
echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf

# Start PostgreSQL server
postgres -D /var/lib/postgresql/data &

# Create the user and database based on environment variables
while ! pg_isready -q -d postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost/$POSTGRES_DB; do
    echo "Waiting for PostgreSQL to start..."
    sleep 1
done

if [ -z "$(psql -Atqc "\\list $POSTGRES_DB")" ]; then
    echo "Database $POSTGRES_DB does not exist. Creating..."
    psql -c "CREATE DATABASE $POSTGRES_DB"
    psql -c "CREATE USER $POSTGRES_USER WITH SUPERUSER PASSWORD '$POSTGRES_PASSWORD'"
fi

# Keep the process running
wait
