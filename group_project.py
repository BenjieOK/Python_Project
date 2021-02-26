from decouple import config
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import numpy as np
import csv
import pandas as pd

connection = psycopg2.connect(
    database='postgres',
    user='postgres',
    password=config("DBPASSWORD"),
    host='127.0.0.1',
    port='5432'
)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

cursor.execute('CREATE SCHEMA IF NOT EXISTS people')
cursor.execute('DROP TABLE IF EXISTS people.users')
cursor.execute(
    """
    CREATE TABLE people.users(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        address VARCHAR(50) NOT NULL,
        city VARCHAR(50) NOT NULL,
        county VARCHAR(50) NOT NULL,
        state VARCHAR(50) NOT NULL,
        zip VARCHAR(50) NOT NULL,
        phone1 VARCHAR(50) NOT NULL,
        phone2 VARCHAR(50) NOT NULL
        )

    """
)

with open('data/500-us-users.csv', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    data = np.empty((0, 9))
    for row in reader:
        hommie = np.array(
            [
                [
                    row['first_name'],
                    row['last_name'],
                    row['address'],
                    row['city'],
                    row['county'],
                    row['state'],
                    row['zip'],
                    row['phone1'],
                    row['phone2']
                ]
            ]
            )

        data = np.append(data, hommie, axis=0)

sql = """ INSERT INTO people.users
    (first_name, last_name, address, city, county, state, zip, phone1, phone2)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
values = data
cursor.executemany(sql, values)

cursor.execute(
    "SELECT state, count(first_name) FROM people.users group by state"
    )
pf = pd.DataFrame(cursor.fetchall(), columns=['state', 'count'])
print(pf)

cursor.execute(
    "SELECT first_name, zip FROM people.users order by zip"
)
pf = pd.DataFrame(cursor.fetchall(), columns=['first_name', 'zip'])
print(pf.head())

cursor.execute(
    """select zip, count(first_name) from people.users
    group by zip having count(first_name)>1"""
)
pf = pd.DataFrame(cursor.fetchall(), columns=['zip', 'count'])
print(pf)

cursor.execute(
    """select substr(last_name, 1,1) as last_name, count(first_name)
    from people.users
    group by substr(last_name, 1,1)"""
)
pf = pd.DataFrame(cursor.fetchall(), columns=['last_name', 'count'])
print(pf)
