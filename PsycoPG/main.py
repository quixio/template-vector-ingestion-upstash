import psycopg2

# SQL commands to create table and insert initial data
create_table_query = '''
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL NOT NULL
);
'''

insert_data_query = '''
INSERT INTO products (name, price) VALUES (%s, %s)
RETURNING id;
'''

# Sample data to insert
sample_data = ('Sample Product', 19.99)

try:
    # Connect to your postgres DB
    conn = psycopg2.connect(
            host="postgresdb",  # Docker service name or IP address
            database="test_db",          # Default database
            user="root",              # Default user
            password="root",     # Password for the PostgreSQL user
            port=80,
            connect_timeout=10       
        )
    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    # Create table if not exists
    cur.execute(create_table_query)
    
    # Insert data into table
    cur.execute(insert_data_query, sample_data)
    product_id = cur.fetchone()[0]
    print(f"Inserted product with ID: {product_id}")

    # Commit the changes to the database
    conn.commit()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Clean up connection
    if conn:
        cur.close()
        conn.close()
