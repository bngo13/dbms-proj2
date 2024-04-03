import uuid
import psycopg2
from psycopg2 import sql

iterations = 100
DATABASE_URL = "postgres://pdtyayje:LwPTxm21oU5kSA7WU1Z_IxHsz3hhohMz@bubble.db.elephantsql.com/pdtyayje"

insert_bikelist = sql.SQL("""
INSERT INTO BikeList (BikeSerialCodeHash, BikeName, BikeType) VALUES (pgp_sym_encrypt(%s, 'key'), %s, %s)
""")

insert_bikecost = sql.SQL("""
INSERT INTO BikeCost (BikeSerialCodeHash, BikeCost) VALUES (%s, %s)
""")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    for i in range(0, iterations):
        # Generate a serial code for a long string
        serialCode = str(uuid.uuid4()).replace('-', '')
        cur.execute(insert_bikelist, (serialCode, "Name" + str(i), "Type" + str(i)))
        cur.execute(insert_bikecost, (serialCode, i * 100))
    conn.commit()

except psycopg2.DatabaseError as e:
    print(f"An error occurred with database {DATABASE_URL}: {e}")
finally:
    # Ensure that the database connection is closed
    if 'cur' in locals(): cur.close()
    if 'conn' in locals(): conn.close()