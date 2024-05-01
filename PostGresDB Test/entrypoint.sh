#!/bin/bash
set -e

# Automatically initialize and configure the database if not already set up
if [ ! -s "/var/lib/postgresql/data/PG_VERSION" ]; then
    echo "Initializing database..."
    pg_ctl initdb -D /var/lib/postgresql/data

    # Modify the configuration to listen on all interfaces
    echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf
    echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf

    # Start the PostgreSQL service
    pg_ctl start -D /var/lib/postgresql/data -l logfile

    # Create a new user and database
    while ! pg_isready -d postgres; do
        echo "Waiting for PostgreSQL to start..."
        sleep 1
    done

    createdb -O $POSTGRES_USER $POSTGRES_DB
    psql -c "CREATE USER $POSTGRES_USER WITH SUPERUSER PASSWORD '$POSTGRES_PASSWORD';"
fi

# Run PostgreSQL in the foreground
exec postgres -D /var/lib/postgresql/data
