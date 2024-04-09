import psycopg2
from psycopg2 import sql

DATABASE_URL = "postgres://pdtyayje:LwPTxm21oU5kSA7WU1Z_IxHsz3hhohMz@bubble.db.elephantsql.com/pdtyayje"

slow_query = sql.SQL("""
SELECT *
FROM
(
BikeList JOIN BikeCost
ON pgp_sym_decrypt(BikeList.BikeSerialCodeHash::bytea, 'key') = BikeCost.BikeSerialCodeHash
)
WHERE BikeList.BikeName LIKE 'Name%';
""")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(slow_query)
    conn.commit()

except psycopg2.DatabaseError as e:
    print(f"An error occurred with database {DATABASE_URL}: {e}")
finally:
    # Ensure that the database connection is closed
    if 'cur' in locals(): cur.close()
    if 'conn' in locals(): conn.close()
