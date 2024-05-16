import psycopg2
from psycopg2 import sql


class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS data (
                id SERIAL PRIMARY KEY,
                date DATE,
                coordinate_x FLOAT,
                coordinate_y FLOAT,
                coordinate_z FLOAT,
                x_probe FLOAT,
                y_probe FLOAT,
                z_probe FLOAT,
                sample_time TIMESTAMP,
                sample_distance FLOAT
            )
        '''
        self.cur.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, date, coordinate_x, coordinate_y, coordinate_z, x_probe, y_probe, z_probe, sample_time,
                    sample_distance):
        insert_query = '''
            INSERT INTO data (date, coordinate_x, coordinate_y, coordinate_z, x_probe, y_probe, z_probe, sample_time, sample_distance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.cur.execute(insert_query, (
        date, coordinate_x, coordinate_y, coordinate_z, x_probe, y_probe, z_probe, sample_time, sample_distance))
        self.conn.commit()

    def select_all_data(self):
        select_query = '''
            SELECT * FROM data
        '''
        self.cur.execute(select_query)
        return self.cur.fetchall()

    def delete_data(self, data_id):
        delete_query = '''
            DELETE FROM data WHERE id = %s
        '''
        self.cur.execute(delete_query, (data_id,))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
