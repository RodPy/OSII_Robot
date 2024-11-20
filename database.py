"""
October 2024
Version: 1.0
Author: Rodney Rojas
Sustainable MRI Lab

database.py

Description:
This class provides functions to interact with a PostgreSQL database.
It allows the creation of a table to store data with coordinates and associated information,
insertion of new records, selection of all data, and deletion of records by ID.
It handles basic database operations to store 3D coordinates and related data.

Functions:
- create_table(): Creates a table named 'data' if it doesn't already exist.
- insert_data(): Inserts a new record into the 'data' table.
- select_all_data(): Selects all data from the 'data' table.
- delete_data(): Deletes a record by its ID.
- close(): Closes the database connection and cursor.
"""
import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        # Establish connection to the PostgreSQL database
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        # Create a cursor object to interact with the database
        self.cur = self.conn.cursor()

    def create_table(self):
        # Create a table if it does not already exist
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS data (
                id SERIAL PRIMARY KEY,  -- Primary key with auto-increment
                date DATE,  -- Date field
                coordinate_x FLOAT,  -- X coordinate for data points
                coordinate_y FLOAT,  -- Y coordinate for data points
                coordinate_z FLOAT,  -- Z coordinate for data points
                y_probe FLOAT,          --  probe data 
                sample_time TIMESTAMP,  -- Time when the sample was taken
                sample_distance FLOAT  -- Distance related to the sample
            )
        '''
        # Execute the query to create the table
        self.cur.execute(create_table_query)
        # Commit the transaction to save changes
        self.conn.commit()

    def insert_data(self, date, coordinate_x, coordinate_y, coordinate_z, y_probe, sample_time, sample_distance):
        # Insert data into the 'data' table
        insert_query = '''
            INSERT INTO data (date, coordinate_x, coordinate_y, coordinate_z, y_probe, sample_time, sample_distance)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        # Execute the query with the provided data
        self.cur.execute(insert_query, (
            date, coordinate_x, coordinate_y, coordinate_z, y_probe, sample_time, sample_distance))
        #
