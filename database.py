from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import psycopg
from psycopg.rows import dict_row
import pytz
import urllib.parse as urlparse
from keep_alive import get_ipv4
import logging

OWNER_ID = 594617002736222219

# SHOULD add database checks for integrity and stuff  

# ALSO might want to think about a better/cleaner database setup if expanding
    # Don't want to have a lot of db methods cluttering
        # could have DB just run a command given and then return

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
            INSERT INTO daily_status (id, last_reset)
            VALUES (1, NOW())
            ON CONFLICT (id)
            DO UPDATE SET
            last_reset = NOW();
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
        with self.connection.cursor(row_factory=dict_row) as cur:

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
        with self.connection.cursor(row_factory=dict_row) as cur:
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
                WHERE user_id = %s
                RETURNING roll_count;
                """, (user_info['user_id'],))

                roll_count = cur.fetchone()
                if roll_count is None:
                    raise ValueError("Roll count: Should not be possible")

                self.set_user_last_status(user_info)

                self.connection.commit()
                return roll_count[0]
            else:
                cur.execute("""
                SELECT roll_count FROM users
                WHERE user_id = %s;
                """, (user_info['user_id'],))

                roll_count = cur.fetchone()
                if roll_count is None:
                    raise ValueError("Roll count: Should not be possible")

                self.set_user_last_status(user_info)

                self.connection.commit()
                return roll_count[0]

    def subtract_roll(self, user_info):
        with self.connection.cursor() as cur:

            cur.execute("""
            UPDATE users
            SET roll_count = roll_count - 1
            WHERE user_id = %s
            RETURNING roll_count;
            """, (user_info['user_id'],))

            roll_count = cur.fetchone()
            if roll_count is None:
                raise ValueError("Roll count: Should not be possible")
            self.connection.commit()

            return roll_count[0]

    def get_rand_gif_with_tier(self, tier):
        with self.connection.cursor(row_factory=dict_row) as cur:

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

    def reset_pities(self, user_info, tier):
        with self.connection.cursor() as cur:

            which_counter = None
            if tier == "S":
                which_counter = "s_pity"
            elif tier == "A":
                which_counter = 'a_pity'
            else:
                return

            cur.execute(f"""
            UPDATE users
            SET {which_counter} = 0
            WHERE user_id = %s
            """, (user_info['user_id'],))


    def get_gif_from_gif_id(self, gif_id):
        with self.connection.cursor(row_factory=dict_row) as cur:
            
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
        with self.connection.cursor(row_factory=dict_row) as cur:

            cur.execute("""
            SELECT * FROM users
            WHERE user_id = %s;
            """, (user_id,))

            user_info = cur.fetchone()
            if user_info is None:
                raise ValueError("User info not found")
            return user_info
    
    def set_user_last_status(self, user_info):
        with self.connection.cursor() as cur:

            cur.execute("""
            UPDATE users
            SET last_status = %s
            WHERE user_id = %s;
            """, (datetime.now(), user_info['user_id'],))
            # Add database check here

            self.connection.commit()

    def add_user_gif(self, user_info, gif):
        with self.connection.cursor() as cur:
            
            cur.execute("""
            INSERT INTO user_gifs (user_id, gif_id, obtain_date)
            VALUES (%s, %s, %s)
            """,(user_info['user_id'], gif['id'], datetime.now(),))

            self.connection.commit()
            print(f"{user_info['user_id']} got gif id: {gif['id']}")

    def make_connection(self):
        load_dotenv()

        db_url = os.environ.get('DATABASE_URL')

        if db_url:

            connection = psycopg.connect(db_url)
            print("USING PRODUCTION")

        else:
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

            connection = psycopg.connect(
                f"dbname={envs['db_name']} "
                f"user={envs['db_user']} "
                f"password={envs['db_password']} "
                f"host={envs['db_host']} "
                f"port={envs['db_port']} "
            )
            print("USING LOCAL TEST")

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




