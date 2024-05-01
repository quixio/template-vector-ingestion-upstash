import psycopg2

def connect_to_db():
    """ Connects to the PostgreSQL database server """
    conn = None
    try:
        # Connection parameters - adjust as needed
        conn = psycopg2.connect(
            host="postgres_service_name",  # Docker service name or IP address
            database="postgres",          # Default database
            user="postgres",              # Default user
            password="your_password"      # Password for the PostgreSQL user
        )

        # Create a cursor object
        cur = conn.cursor()
        
        # SQL for creating a table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT
        );
        '''
        cur.execute(create_table_query)
        conn.commit()  # Commit the changes
        print("Table created successfully.")

        # Close the cursor and the connection
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not limited to:
            conn.close()
            print("Database connection closed.")

# Main execution
if __name__ == '__main__':
    connect_to_db()