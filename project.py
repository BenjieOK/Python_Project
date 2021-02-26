from decouple import config
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv
import numpy as np
import pandas as pd


# Create a connection object
def getconnection(database):
    connection = psycopg2.connect(
        database=database,
        user="postgres",
        password=config("DBPASSWORD"),
        host="127.0.0.1", port="5432"
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    return cursor


# Query via the cursor
def createSchema():
    cursor = getconnection("users")
    cursor.execute("CREATE SCHEMA IF NOT EXISTS people")
    cursor.execute("DROP TABLE IF EXISTS people.users")
    cursor.execute(
        """
    CREATE TABLE people.users
    (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(20),
    county VARCHAR(20),
    state VARCHAR(3),
    zip VARCHAR(10),
    phone1 VARCHAR(20),
    phone2 VARCHAR(20))
        """
    )


with open('data/500-us-users.csv', newline='') as user_file:
    data = csv.DictReader(user_file, delimiter=',')
    users = np.empty((0, 9))

    for row in data:
        hommie = np.array([
            [row['first_name'], row['last_name'], row['address'],
             row['city'], row['county'], row['state'],
             row['zip'], row['phone1'], row['phone2']]
        ])
        users = np.append(users, hommie, axis=0)


def insertData():
    cursor = getconnection("users")
    sql = """INSERT INTO people.users
    (first_name, last_name, address, city, county, state, zip, phone1, phone2)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.executemany(sql, users)


# getconnection("users")
# createSchema()
# insertData()
cursor = getconnection("users")
cursor.execute(
    "SELECT COUNT(first_name), state FROM people.users GROUP BY state"
    )
pf = pd.DataFrame(cursor.fetchall(), columns=['count', 'state'])
print(pf)

cursor.execute(
    """SELECT COUNT(first_name), zip
        FROM people.users GROUP BY zip HAVING COUNT(first_name)>1
    """
)
pf = pd.DataFrame(cursor.fetchall(), columns=['count', 'zip'])
print(pf)

cursor.execute(
    """SELECT COUNT(first_name), last_name
        FROM people.users GROUP BY last_name HAVING COUNT(first_name)>1
    """
)
pf = pd.DataFrame(cursor.fetchall(), columns=['count', 'last_name'])
print(pf)
