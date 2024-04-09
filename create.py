import psycopg2
from psycopg2 import sql

DATABASE_URL = "postgres://pdtyayje:LwPTxm21oU5kSA7WU1Z_IxHsz3hhohMz@bubble.db.elephantsql.com/pdtyayje"

# BikeSerialCode will just be really long UUIDs where we'd do id searching
# We'd also join them together a lot with long text everywhere to make it slow for 5s
# BikeSerialCodeHash contains encryted serial codes

create_table_command = sql.SQL("""
CREATE TABLE IF NOT EXISTS BikeList (
    BikeListID SERIAL PRIMARY KEY,
    BikeSerialCodeHash TEXT NOT NULL,
    BikeName TEXT NOT NULL,
    BikeType TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS BikeCost (
    BikeCostID SERIAL PRIMARY KEY,
    BikeSerialCodeHash TEXT NOT NULL,
    BikeCost DECIMAL(10, 2)
);
""")

clean_database = sql.SQL("""
DROP TABLE BikeList;
DROP TABLE BikeCost;
""")

def create_table_in_database(db_url):
    try:
        # Connect to the database using the database URL
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Execute the create table command
        cur.execute(clean_database)
        cur.execute(create_table_command)
        
        # Commit the changes
        conn.commit()
        
        print("Table 'BikeList' created successfully in database:", db_url)
        
    except psycopg2.DatabaseError as e:
        print(f"An error occurred in database {db_url}: {e}")
    finally:
        # Close communication with the database
        if cur: cur.close()
        if conn: conn.close()

create_table_in_database(DATABASE_URL)
