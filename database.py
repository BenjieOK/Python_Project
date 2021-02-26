from decouple import config
import psycopg2

# Create a connection object
connection = psycopg2.connect(
                                database="postgres",
                                user="postgres",
                                password=config("DBPASSWORD"),
                                host="127.0.0.1", port="5432"
                            )

# Create a cursor via the connection
cursor = connection.cursor()

# Query via the cursor
cursor.execute("select * from pubs2.authors")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Alternatively, set the 'search_path' to set the schema search path (prefix)
cursor.execute("SET search_path TO pubs2")
cursor.execute("select * from authors")
rows = cursor.fetchall()
for row in rows:
    print(row)
