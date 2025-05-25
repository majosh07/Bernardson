from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pytz
import logging

OWNER_ID = 594617002736222219



class Database:
    def __init__(self) -> None:
        self.connection = self.make_connection()    


    def get_last_status(self):
        with self.connection.cursor() as cur:

            cur.execute("""
            SELECT last_reset FROM daily_status;
            """)
            
            last_status = cur.fetchone()
            if last_status is None:
                raise ValueError("Did not get last status...")
            return last_status[0]

    def set_last_status(self):
        with self.connection.cursor() as cur:

            cur.execute("""
            UPDATE daily_status SET last_reset = %s WHERE id = 1;
            """, (datetime.now(),))
            self.connection.commit()

    def get_num_gifs(self):
        with self.connection.cursor() as cur:
        
            cur.execute("""
            SELECT COUNT(*) FROM user_gifs;
            """)
            # add loggin here

            num_gifs = cur.fetchone()
            if num_gifs is None:
                raise ValueError("Did not get last status...")
            return num_gifs[0]

    def add_daily_gif(self, user):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute("""
            INSERT INTO daily_gifs (gif_id, url, user_id, author)
            SELECT gifs.id, gifs.url, %s, %s
            FROM gifs
            ORDER BY RANDOM()
            LIMIT 1
            RETURNING gif_id, url, user_id, author, created_at;
            """,(user.id, user.name,))

            latest_gif = cur.fetchone()
            if latest_gif is None:
                raise ValueError("Did not get gif")
            self.connection.commit()
            return latest_gif

    def get_daily_gif(self, user):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
            SELECT gif_id, user_id, author, created_at, url FROM daily_gifs 
            ORDER BY created_at DESC
            LIMIT 1;
            """)

            recent_gif = cur.fetchone()
            is_new = False
            if recent_gif is None or self.is_next_day(recent_gif['created_at']):
                recent_gif = self.add_daily_gif(user)
                is_new = True

            return dict(recent_gif), is_new

    def check_add_roll(self, user, admin=False):
        with self.connection.cursor() as cur:

            user_info = self.get_user_info(user.id)

            if self.is_next_day_and_admin(user_info, admin):
                cur.execute("""
                UPDATE users
                SET roll_count = roll_count + 1
                RETURNING roll_count;
                """)

                roll_count = cur.fetchone()
                if roll_count is None:
                    raise ValueError("Roll count: Should not be possible")

                self.connection.commit()
                return roll_count[0]
            else:
                cur.execute("""
                SELECT roll_count FROM users;
                """)

                roll_count = cur.fetchone()
                if roll_count is None:
                    raise ValueError("Roll count: Should not be possible")

                self.connection.commit()
                return roll_count[0]

    def get_rand_gif_with_tier(self, tier):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute("""
            SELECT *
            FROM gifs
            WHERE tier = %s
            ORDER BY RANDOM()
            LIMIT 1
            """, (tier,))

            gif = cur.fetchone()
            if gif is None:
                raise ValueError("There are now gifs")
            return dict(gif)

    def get_gif_from_gif_id(self, gif_id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            
            cur.execute("""
            SELECT * FROM gifs
            WHERE id = %s;
            """, (gif_id,))

            gif_info = cur.fetchone()
            if gif_info is None:
                raise ValueError("Could not find gif")
            return gif_info
    
    def check_add_user(self, user_info):
        with self.connection.cursor() as cur:

            cur.execute("""
            INSERT INTO users (user_id, username)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
            """, (user_info.id, user_info.name))

            self.connection.commit()

    def get_user_info(self, user_id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute("""
            SELECT * FROM users
            WHERE user_id = %s;
            """, (user_id,))

            user_info = cur.fetchone()
            if user_info is None:
                raise ValueError("User info not found")
            return user_info


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

    def is_next_day(self, last_status):
        est = pytz.timezone("US/Eastern")
        effective_time = datetime.now(est) - timedelta(hours=4)
        local_status = est.localize(last_status)

        return local_status < effective_time
    
    def is_next_day_and_admin(self, user_info, admin_flag):
        if user_info['user_id'] == OWNER_ID and admin_flag:
            return True
        return self.is_next_day(user_info['last_status'])



    def __del__(self):
      if self.connection:
        self.connection.close()





