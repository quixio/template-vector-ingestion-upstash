import psycopg2
from psycopg2.extras import execute_batch

# Define your PostgreSQL connection parameters
connection_params = {
    "dbname": "test_db",
    "user": "root",
    "password": "root",
    "host": "postgresdb",
    "port": "80",
    "connect_timeout": "10" 
}

# Sample documents data
documents = [
    { "name": "The Time Machine", "description": "A man travels through time and witnesses the evolution of humanity.", "author": "H.G. Wells", "year": 1895 },
    { "name": "Ender's Game", "description": "A young boy is trained to become a military leader in a war against an alien race.", "author": "Orson Scott Card", "year": 1985 },
    { "name": "Brave New World", "description": "A dystopian society where people are genetically engineered and conditioned to conform to a strict social hierarchy.", "author": "Aldous Huxley", "year": 1932 },
    {"name": "An Absolutely Remarkable Thing", "description": "A young woman becomes famous after discovering a mysterious alien artifact in New York City.", "author": "Hank Green", "year": 2018},
    { "name": "Dune", "description": "A desert planet is the site of political intrigue and power struggles.", "author": "Frank Herbert", "year": 1965 },
    { "name": "Foundation", "description": "A mathematician develops a science to predict the future of humanity and works to save civilization from collapse.", "author": "Isaac Asimov", "year": 1951 },
    { "name": "Snow Crash", "description": "A futuristic world where the internet has evolved into a virtual reality metaverse.", "author": "Neal Stephenson", "year": 1992 },
    { "name": "Neuromancer", "description": "A hacker is hired to pull off a near-impossible hack and gets pulled into a web of intrigue.", "author": "William Gibson", "year": 1984 },
    { "name": "The War of the Worlds", "description": "A Martian invasion of Earth throws humanity into chaos.", "author": "H.G. Wells", "year": 1898 },
    { "name": "The Hunger Games", "description": "A dystopian society where teenagers are forced to fight to the death in a televised spectacle.", "author": "Suzanne Collins", "year": 2008 },
    { "name": "The Andromeda Strain", "description": "A deadly virus from outer space threatens to wipe out humanity.", "author": "Michael Crichton", "year": 1969 },
    { "name": "The Left Hand of Darkness", "description": "A human ambassador is sent to a planet where the inhabitants are genderless and can change gender at will.", "author": "Ursula K. Le Guin", "year": 1969 },
    { "name": "The Time Traveler's Wife", "description": "A love story between a man who involuntarily time travels and the woman he loves.", "author": "Audrey Niffenegger", "year": 2003 }
]

def main():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Prepare data for insertion
    data = [(doc['name'], doc['description'], doc['author'], doc['year']) for doc in documents]

    # Create a table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            name TEXT,
            description TEXT,
            author TEXT,
            year INTEGER
        )
    ''')
    conn.commit()

    # Insert data using execute_batch for efficient bulk inserts
    query = "INSERT INTO books (name, description, author, year) VALUES (%s, %s, %s, %s)"
    execute_batch(cursor, query, data)
    print("Inserted records.")
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
