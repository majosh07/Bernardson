from datetime import datetime, timedelta
from discord.ext.commands import param
import psycopg 
from psycopg.rows import dict_row
import pytz
from logging_config import logger

from pool import pool


OWNER_ID = 594617002736222219

# SHOULD add database checks for integrity and stuff  

async def fetch_value(query, params=None, commit=False):
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute("SET TIME ZONE 'US/Eastern';")
                await cur.execute(query, params)

                res = await cur.fetchone()
                if res is None:
                    raise ValueError(f"No result from:\n{query}\nParams:\n{params}")

                if commit:
                    await conn.commit()

                return res[0]

            except psycopg.IntegrityError:
                logger.exception("Integrity error:")  # e.g. duplicate key, not null violation
                raise
            except psycopg.OperationalError:
                logger.exception("Operational error:")  # e.g. connection issues
                raise
            except psycopg.DatabaseError:
                logger.exception("Database error:")  # general DB issues
                raise
            except Exception:
                logger.exception("Other error:")  # fallback
                raise

async def fetch_count(query, params=None, commit=False):
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute("SET TIME ZONE 'US/Eastern';")
                await cur.execute(query, params)

                res = await cur.fetchone()
                if res is None:
                    raise ValueError(f"No result from:\n{query}\nParams:\n{params}")

                if commit:
                    await conn.commit()

                return res

            except psycopg.IntegrityError:
                logger.exception("Integrity error:")  # e.g. duplicate key, not null violation
                raise
            except psycopg.OperationalError:
                logger.exception("Operational error:")  # e.g. connection issues
                raise
            except psycopg.DatabaseError:
                logger.exception("Database error:")  # general DB issues
                raise
            except Exception:
                logger.exception("Other error:")  # fallback
                raise

async def fetch_dict(query, params=None, commit=False):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            try:
                await cur.execute("SET TIME ZONE 'US/Eastern';")
                await cur.execute(query, params)

                row = await cur.fetchone()
                if row is None:
                    raise ValueError(f"Could not fetch dict: \n{query}\nParams: \n{params}")

                if commit:
                    await conn.commit()
                return row

            except psycopg.IntegrityError:
                logger.exception("Integrity error:")  # e.g. duplicate key, not null violation
                raise
            except psycopg.OperationalError:
                logger.exception("Operational error:")  # e.g. connection issues
                raise
            except psycopg.DatabaseError:
                logger.exception("Database error:")  # general DB issues
                raise
            except Exception:
                logger.exception("Other error:")  # fallback
                raise

async def exec_write(query, params=None, commit=True):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            try:
                await cur.execute("SET TIME ZONE 'US/Eastern';")
                await cur.execute(query, params)

                if commit:
                    await conn.commit()

            except psycopg.IntegrityError:
                logger.exception("Integrity error:")  # e.g. duplicate key, not null violation
            except psycopg.OperationalError:
                logger.exception("Operational error:")  # e.g. connection issues
            except psycopg.DatabaseError:
                logger.exception("Database error:")  # general DB issues
            except Exception:
                logger.exception("Other error:")  # fallback


def is_next_day(last_status):
    est = pytz.timezone("US/Eastern")
    now_est = datetime.now(pytz.utc).astimezone(est)

    if last_status.tzinfo is None:
        last_status = est.localize(last_status)
    else:
        last_status = last_status.astimezone(est)

    last_day = last_status.date()
    four_am_last = est.localize(datetime.combine(last_day, datetime.min.time())) + timedelta(hours=4)

    if last_status >= four_am_last:
        threshold = four_am_last + timedelta(days=1)
    else:
        threshold = four_am_last

    return now_est >= threshold

def is_next_day_and_admin(user_info, admin_flag):
    if user_info['user_id'] == OWNER_ID and admin_flag:
        return True
    return is_next_day(user_info['last_status'])


async def get_last_status():
    return await fetch_value("SELECT last_reset FROM daily_status;")


async def set_last_status():
    print(f"New status: {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    return await exec_write("""
                INSERT INTO daily_status (id, last_reset)
                VALUES (1, NOW())
                ON CONFLICT (id)
                DO UPDATE SET last_reset = NOW();
                """, commit=True)


async def get_num_gifs(user):
    query = """
            SELECT COUNT(*) FROM user_gifs
            WHERE user_id = %s;
            """
    return await fetch_value(query, params=(user.id,))

async def get_num_tier_gifs(user, tier):
    query = """
            SELECT COUNT(*) 
            FROM user_gifs
            INNER JOIN gifs ON user_gifs.gif_id = gifs.id
            WHERE user_gifs.user_id = %s AND gifs.tier = %s;
            """
    return await fetch_value(query, params=(user.id, tier))

async def add_daily_gif(user):
    print(f"New daily_gif at: {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    query = """
            INSERT INTO daily_gifs (gif_id, url, user_id, author)
            SELECT gifs.id, gifs.url, %s, %s
            FROM gifs
            ORDER BY RANDOM()
            LIMIT 1
            RETURNING gif_id, url, user_id, author, created_at;
            """
    return await fetch_dict(query, params=(user.id, user.name,), commit=True)

async def get_daily_gif(user):
    query = """
            SELECT gif_id, user_id, author, created_at, url FROM daily_gifs 
            ORDER BY created_at DESC
            LIMIT 1;
            """
    recent_gif = await fetch_dict(query,)
    is_new = False

    if recent_gif is None or is_next_day(await get_last_status()):
        recent_gif = await add_daily_gif(user)
        is_new = True
        await set_last_status()

    if recent_gif is None:
        logger.exception("get_daily_gif: recent_gif was None")
        raise ValueError("get_daily_gif: recent_gif was None")

    return dict(recent_gif), is_new


async def check_add_roll(user, admin=False):
    user_info = await get_user_info(user.id)

    if is_next_day_and_admin(user_info, admin):

        query = """
        UPDATE users
        SET roll_count = roll_count + 1
        WHERE user_id = %s
        RETURNING roll_count;
        """
        roll_count = await fetch_value(query, params=(user_info['user_id'],), commit=True)

        await set_user_last_status(user_info)

        return roll_count

    else:
        query = """
        SELECT roll_count FROM users
        WHERE user_id = %s;
        """

        roll_count = await fetch_value(query, params=(user_info['user_id'],), commit=True)
        if roll_count is None:
            logger.error("get_rand_gif_with_tier: No gif from tier somehow")
            raise ValueError("get_rand_gif_with_tier: No gif from tier somehow")

        await set_user_last_status(user_info)

        return roll_count

async def subtract_roll(user_info):
    query = """
            UPDATE users
            SET roll_count = roll_count - 1
            WHERE user_id = %s
            RETURNING roll_count;
            """

    roll_count = await fetch_value(query, params=(user_info['user_id'],), commit=True)
    return roll_count

async def get_rand_gif_with_tier(tier):
    query = """
            SELECT *
            FROM gifs
            WHERE tier = %s
            ORDER BY RANDOM()
            LIMIT 1
            """

    gif = await fetch_dict(query, params=(tier,))
    if gif is None:
        logger.error("get_rand_gif_with_tier: No gif from tier somehow")
        raise ValueError("get_rand_gif_with_tier: No gif from tier somehow")

    return dict(gif)

async def reset_pities(user_info, tier):

    which_counter = None
    if tier == "S":
        which_counter = "s_pity"
    elif tier == "A":
        which_counter = 'a_pity'
    else:
        return

    query = f"""
            UPDATE users
            SET {which_counter} = 0
            WHERE user_id = %s;
            """
    
    await exec_write(query, params=(user_info['user_id'],))


async def add_pities(user_info):
    query = """
            UPDATE users
            SET s_pity = s_pity + 1,
            a_pity = a_pity + 1
            WHERE user_id = %s
            RETURNING s_pity, a_pity;
            """

    row = await fetch_dict(query, params=(user_info['user_id'],), commit=True)
    if row is None:
        logger.error("add_pities: no row")
        raise ValueError("add_pities: no row")

    s_pity, a_pity = row['s_pity'], row['a_pity']


    return s_pity, a_pity

async def get_gif_from_gif_id(gif_id):
    query = """
            SELECT * FROM gifs
            WHERE id = %s;
            """

    gif_info = await fetch_dict(query, params=(gif_id,))

    return gif_info


async def check_add_user(user_info):
    query = """
            INSERT INTO users (user_id, username)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
            """

    await exec_write(query, params=(user_info.id, user_info.name))

async def get_user_info(user_id):
    query = """
            SELECT * FROM users
            WHERE user_id = %s;
            """

    user_info = await fetch_dict(query, params=(user_id,))

    return dict(user_info)
    
async def set_user_last_status(user_info):
    query = """
            UPDATE users
            SET last_status = %s
            WHERE user_id = %s;
            """

    await exec_write(query, params=(datetime.now(), user_info['user_id'],))


async def add_user_gif(user_info, gif):
    query = """
            INSERT INTO user_gifs (user_id, gif_id, obtain_date)
            VALUES (%s, %s, %s)
            """

    await exec_write(query, params=(user_info['user_id'], gif['id'], datetime.now(),))

