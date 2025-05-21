from dotenv import load_dotenv
from datetime import datetime
import os
import psycopg2

class Database:
    def __init__(self) -> None:
        self.connection = self.make_connection()    


    def get_last_status(self):
        cur = self.connection.cursor()

        cur.execute("""
        SELECT last_reset FROM daily_status;
        """)
        
        last_status = cur.fetchone()
        if last_status is None:
            raise ValueError("Did not get last status...")
        return last_status[0]

    def set_last_status(self):
        cur = self.connection.cursor()

        cur.execute("""
        UPDATE daily_status SET last_reset = %s WHERE id = 1;
        """, (datetime.now(),))

    def get_num_gifs(self):
        cur = self.connection.cursor()
        
        cur.execute("""
        SELECT COUNT(*) FROM user_gifs;
        """)
        # add loggin here

        num_gifs = cur.fetchone()
        if num_gifs is None:
            raise ValueError("Did not get last status...")
        return num_gifs[0]



    def make_connection(self):
        load_dotenv()
        envs = {
            'db_name' : os.environ.get('DB_NAME'),
            'db_user' : os.environ.get('DB_USER'),
            'db_password' : os.environ.get('DB_PASSWORD'),
            'db_host' : os.environ.get('DB_HOST'),
            'db_port' : os.environ.get('DB_PORT'),
        }

        missing = [key for key, val in envs.items() if val is None]
        if missing:
            raise ValueError(f"Connection failed: {', '.join(missing)}")

        connection = psycopg2.connect(
            dbname=envs['db_name'],
            user=envs['db_user'],
            password=envs['db_password'],
            host=envs['db_host'],
            port=envs['db_port']
        )
        # add logging here

        return connection

    def __del__(self):
      if self.connection:
        self.connection.close()





