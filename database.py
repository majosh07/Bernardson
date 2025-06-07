from typing import Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import psycopg 
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
import pytz
import traceback
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
        load_dotenv()

        db_url = os.environ.get('DATABASE_URL')

        if db_url:
            connection = AsyncConnectionPool(conninfo=db_url, max_size=1, open=False, max_lifetime=300,)

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

            conn_info = (
                f"dbname={envs['db_name']} "
                f"user={envs['db_user']} "
                f"password={envs['db_password']} "
                f"host={envs['db_host']} "
                f"port={envs['db_port']} "
            )
            connection = AsyncConnectionPool(conninfo=conn_info, open=False, max_lifetime=300)

            # add logging here

        self.pool = connection


    async def get_last_status(self):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:

                await cur.execute("""
                SELECT last_reset FROM daily_status;
                """)
                
                last_status = await cur.fetchone()
                if last_status is None:
                    raise ValueError("Did not get last status...")
                return last_status[0]

    async def set_last_status(self):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:

                await cur.execute("""
                INSERT INTO daily_status (id, last_reset)
                VALUES (1, NOW())
                ON CONFLICT (id)
                DO UPDATE SET last_reset = NOW();
                """, )
                print(f"New status: {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
                await conn.commit()

    async def get_num_gifs(self):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
        
                await cur.execute("""
                SELECT COUNT(*) FROM user_gifs;
                """)
                # add loggin here

                num_gifs = await cur.fetchone()
                if num_gifs is None:
                    raise ValueError("Did not get last status...")
                return num_gifs[0]

    async def add_daily_gif(self, user):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:

                await cur.execute("""
                INSERT INTO daily_gifs (gif_id, url, user_id, author)
                SELECT gifs.id, gifs.url, %s, %s
                FROM gifs
                ORDER BY RANDOM()
                LIMIT 1
                RETURNING gif_id, url, user_id, author, created_at;
                """,(user.id, user.name,))

                latest_gif = await cur.fetchone()
                if latest_gif is None:
                    raise ValueError("Did not get gif")
                await conn.commit()
                print(f"New daily_gif at: {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
                return latest_gif

    async def get_daily_gif(self, user):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                SELECT gif_id, user_id, author, created_at, url FROM daily_gifs 
                ORDER BY created_at DESC
                LIMIT 1;
                """)

                recent_gif = await cur.fetchone()
                is_new = False
                if recent_gif is None or self.is_next_day(await self.get_last_status()):
                    recent_gif = await self.add_daily_gif(user)
                    is_new = True
                    await self.set_last_status()
                print(f"{user.name} did daily at: {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
                return dict(recent_gif), is_new

    async def check_add_roll(self, user, admin=False):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:

                user_info = await self.get_user_info(user.id)

                if self.is_next_day_and_admin(user_info, admin):

                    await cur.execute("""
                    UPDATE users
                    SET roll_count = roll_count + 1
                    WHERE user_id = %s
                    RETURNING roll_count;
                    """, (user_info['user_id'],))

                    roll_count = await cur.fetchone()
                    if roll_count is None:
                        raise ValueError("Roll count: Should not be possible")

                    await conn.commit()

                    await self.set_user_last_status(user_info)

                    return roll_count[0]
                else:
                    await cur.execute("""
                    SELECT roll_count FROM users
                    WHERE user_id = %s;
                    """, (user_info['user_id'],))

                    roll_count = await cur.fetchone()
                    if roll_count is None:
                        raise ValueError("Roll count: Should not be possible")

                    await conn.commit()

                    await self.set_user_last_status(user_info)

                    return roll_count[0]

    async def subtract_roll(self, user_info):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:

                await cur.execute("""
                UPDATE users
                SET roll_count = roll_count - 1
                WHERE user_id = %s
                RETURNING roll_count;
                """, (user_info['user_id'],))

                roll_count = await cur.fetchone()
                if roll_count is None:
                    raise ValueError("Roll count: Should not be possible")
                await conn.commit()

                return roll_count[0]

    async def get_rand_gif_with_tier(self, tier):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:

                await cur.execute("""
                SELECT *
                FROM gifs
                WHERE tier = %s
                ORDER BY RANDOM()
                LIMIT 1
                """, (tier,))

                gif = await cur.fetchone()
                if gif is None:
                    raise ValueError("There are now gifs")
                return dict(gif)

    async def reset_pities(self, user_info, tier):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:

                which_counter = None
                if tier == "S":
                    which_counter = "s_pity"
                elif tier == "A":
                    which_counter = 'a_pity'
                else:
                    return

                await cur.execute(f"""
                UPDATE users
                SET {which_counter} = 0
                WHERE user_id = %s;
                """, (user_info['user_id'],))

    async def add_pities(self, user_info):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:

                await cur.execute("""
                UPDATE users
                SET s_pity = s_pity + 1,
                a_pity = a_pity + 1
                WHERE user_id = %s
                RETURNING s_pity, a_pity;
                """, (user_info['user_id'],))

                row = await cur.fetchone()
                if row is None:
                    raise ValueError("No pity, should not be possible")

                s_pity, a_pity = row
                await conn.commit()

                return s_pity, a_pity

    async def get_gif_from_gif_id(self, gif_id):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:

                await cur.execute("""
                SELECT * FROM gifs
                WHERE id = %s;
                """, (gif_id,))

                gif_info = await cur.fetchone()
                if gif_info is None:
                    raise ValueError("Could not find gif")
                return gif_info


    async def check_add_user(self, user_info):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:

                await cur.execute("""
                INSERT INTO users (user_id, username)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """, (user_info.id, user_info.name))

                await conn.commit()

    async def get_user_info(self, user_id):
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:

                await cur.execute("""
                SELECT * FROM users
                WHERE user_id = %s;
                """, (user_id,))

                user_info = await cur.fetchone()
                if user_info is None:
                    raise ValueError("User info not found")
                return user_info
    
    async def set_user_last_status(self, user_info):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:

                try:
                    await cur.execute("""
                    UPDATE users
                    SET last_status = %s
                    WHERE user_id = %s;
                    """, (datetime.now(), user_info['user_id'],))
                    # Add database check here

                    await conn.commit()
                except Exception as e:
                    print("Database error:", e)
                    traceback.print_exc()


    async def add_user_gif(self, user_info, gif):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
            
                await cur.execute("""
                INSERT INTO user_gifs (user_id, gif_id, obtain_date)
                VALUES (%s, %s, %s)
                """,(user_info['user_id'], gif['id'], datetime.now(),))

                await conn.commit()
                print(f"{user_info['user_id']} got gif id: {gif['id']}")

    # async def make_connection(self):
    #     load_dotenv()
    #
    #     db_url = os.environ.get('DATABASE_URL')
    #
    #     if db_url:
    #         connection = AsyncConnectionPool(conninfo=db_url, open=True)
    #
    #     else:
    #         envs = {
    #             'db_name' : os.environ.get('DB_NAME'),
    #             'db_user' : os.environ.get('DB_USER'),
    #             'db_password' : os.environ.get('DB_PASSWORD'),
    #             'db_host' : os.environ.get('DB_HOST'),
    #             'db_port' : os.environ.get('DB_PORT'),
    #         }
    #
    #         missing = [key for key, val in envs.items() if val is None]
    #         if missing:
    #             raise ValueError(f"Connection failed: {', '.join(missing)}")
    #
    #         conn_info = (
    #             f"dbname={envs['db_name']} "
    #             f"user={envs['db_user']} "
    #             f"password={envs['db_password']} "
    #             f"host={envs['db_host']} "
    #             f"port={envs['db_port']} "
    #         )
    #         connection = AsyncConnectionPool(conninfo=conn_info, open=True)
    #
    #         # add logging here
    #
    #     self.pool = connection
    async def open_pool(self):
        await self.pool.open()

    def is_next_day(self, last_status):
        est = pytz.timezone("US/Eastern")
        now_est = datetime.now(pytz.utc).astimezone(est)

        last_status = est.localize(last_status)
        last_day = last_status.date()
        four_am_last = est.localize(datetime.combine(last_day, datetime.min.time())) + timedelta(hours=4)

        if last_status >= four_am_last:
            threshold = four_am_last + timedelta(days=1)
        else:
            threshold = four_am_last

        return now_est >= threshold
    
    def is_next_day_and_admin(self, user_info, admin_flag):
        if user_info['user_id'] == OWNER_ID and admin_flag:
            return True
        return self.is_next_day(user_info['last_status'])

    async def close(self):
        if self.pool is not None:
            await self.pool.close()




