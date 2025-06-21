from queries import *
from datetime import datetime, timedelta
import psycopg 
import pytz
from logging_config import logger




OWNER_ID = 594617002736222219

# SHOULD add database checks for integrity and stuff  


def get_now_and_threshold_est(last_status):
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

    return now_est, threshold

def has_day_passed(last_status):
    now_est, threshold = get_now_and_threshold_est(last_status)

    return now_est >= threshold

def has_day_passed_admin(user_info, admin_flag):
    if user_info['user_id'] == OWNER_ID and admin_flag:
        return True
    return has_day_passed(user_info['last_status'])

def is_next_day(last_status):
    now_est, threshold = get_now_and_threshold_est(last_status)
    cap = threshold + timedelta(days=1)

    return now_est >= threshold and now_est <= cap

def is_today(last_status):
    now_est, threshold = get_now_and_threshold_est(last_status)
    return now_est < threshold



def get_last_status():
    return fetch_value("SELECT last_status FROM daily_status;")


def set_last_status():
    now_est = datetime.now(pytz.utc).astimezone(pytz.timezone("US/Eastern"))
    print(f"New status: {now_est.strftime('%m-%d-%Y %I:%M %p')}")
    return exec_write("""
                INSERT INTO daily_status (id, last_status)
                VALUES (1, NOW())
                ON CONFLICT (id)
                DO UPDATE SET last_status = NOW();
                """, commit=True)


def get_num_gifs(user):
    query = """
            SELECT COUNT(*) FROM user_gifs
            WHERE user_id = %s;
            """

    amount = fetch_value(query, params=(user.id,))
    if amount is None:
        amount = 0
    return amount

def get_num_tier_gifs(user, tier):
    query = """
            SELECT COUNT(*)
            FROM user_gifs
            INNER JOIN gifs ON user_gifs.gif_id = gifs.id
            WHERE user_gifs.user_id = %s AND gifs.tier = %s;
            """
    amount = fetch_value(query, params=(user.id, tier))
    if amount is None:
        amount = 0
    return amount

def add_daily_gif(user):
    print(f"New daily_gif at: {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    query = """
            INSERT INTO daily_gifs (gif_id, url, user_id, author)
            SELECT gifs.id, gifs.url, %s, %s
            FROM gifs
            ORDER BY RANDOM()
            LIMIT 1
            RETURNING gif_id, url, user_id, author, created_at;
            """
    return fetch_dict(query, params=(user.id, user.name,), commit=True)

def get_daily_gif(user):
    query = """
            SELECT gif_id, user_id, author, created_at, url FROM daily_gifs 
            ORDER BY created_at DESC
            LIMIT 1;
            """
    recent_gif = fetch_dict(query,)
    is_new = False

    if recent_gif is None or has_day_passed(get_last_status()):
        recent_gif = add_daily_gif(user)
        is_new = True
        set_last_status()

    if recent_gif is None:
        logger.exception("get_daily_gif: recent_gif was None")
        raise ValueError("get_daily_gif: recent_gif was None")

    return dict(recent_gif), is_new


def check_add_roll(user, was_bonus, admin_daily=False):
    user_info = get_user_info(user.id)

    if has_day_passed_admin(user_info, admin_daily):

        increase = 1
        if was_bonus:
            increase = 2

        query = """
        UPDATE users
        SET roll_count = roll_count + %s
        WHERE user_id = %s
        RETURNING roll_count;
        """
        roll_count = fetch_value(query, params=(increase, user_info['user_id'],), commit=True)

        set_user_last_status(user_info)

        return roll_count

    else:
        query = """
        SELECT roll_count FROM users
        WHERE user_id = %s;
        """

        roll_count = fetch_value(query, params=(user_info['user_id'],), commit=True)
        if roll_count is None:
            logger.error("get_rand_gif_with_tier: No gif from tier somehow")
            raise ValueError("get_rand_gif_with_tier: No gif from tier somehow")

        set_user_last_status(user_info)

        return roll_count

# relies on check_add_roll setting user_last_status after this is run
def check_add_daily_streak(user, admin_streak=False):
    user_info = get_user_info(user.id)

    if is_next_day(user_info['last_status']) or admin_streak:
        # num days in a week
        query = """
        UPDATE users
        SET daily_streak = daily_streak + 1
        WHERE user_id = %s
        RETURNING daily_streak, 
        CASE WHEN daily_streak %% 7 = 0 THEN true ELSE false END AS was_bonus;
        """

        values = fetch_dict(query, params=(user_info['user_id'],), commit=True)
        if values is None:
            logger.error("didn't get values")
            raise ValueError("didn't get values")

        return values['daily_streak'], values['was_bonus']
    elif is_today(user_info['last_status']):
        query = """
        SELECT daily_streak
        FROM users
        WHERE user_id = %s;
        """

        daily_streak = fetch_value(query, params=(user_info['user_id'],))
        if daily_streak is None:
            logger.error("didn't get daily streak")
            raise ValueError("didn't get daily streak")
        return daily_streak, False

    else:
        query = """
        UPDATE users
        SET daily_streak = 0
        WHERE user_id = %s
        RETURNING daily_streak;
        """

        daily_streak = fetch_value(query, params=(user_info['user_id'],), commit=True)
        if daily_streak is None:
            logger.error("didn't get daily streak")
            raise ValueError("didn't get daily streak")

        return daily_streak, False


def subtract_roll(user_info):
    query = """
            UPDATE users
            SET roll_count = roll_count - 1
            WHERE user_id = %s
            RETURNING roll_count;
            """

    roll_count = fetch_value(query, params=(user_info['user_id'],), commit=True)
    return roll_count

def get_rand_gif_with_tier(tier):
    query = """
            SELECT *
            FROM gifs
            WHERE tier = %s
            ORDER BY RANDOM()
            LIMIT 1
            """

    gif = fetch_dict(query, params=(tier,))
    if gif is None:
        logger.error("get_rand_gif_with_tier: No gif from tier somehow")
        raise ValueError("get_rand_gif_with_tier: No gif from tier somehow")

    return dict(gif)

def reset_pities(user_info, tier):

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
    
    exec_write(query, params=(user_info['user_id'],))


def add_pities(user_info):
    query = """
            UPDATE users
            SET s_pity = s_pity + 1,
            a_pity = a_pity + 1
            WHERE user_id = %s
            RETURNING s_pity, a_pity;
            """

    row = fetch_dict(query, params=(user_info['user_id'],), commit=True)
    if row is None:
        logger.error("add_pities: no row")
        raise ValueError("add_pities: no row")

    s_pity, a_pity = row['s_pity'], row['a_pity']


    return s_pity, a_pity

def get_gif_from_gif_id(gif_id):
    query = """
            SELECT * FROM gifs
            WHERE id = %s;
            """

    gif_info = fetch_dict(query, params=(gif_id,))

    return gif_info

def get_user_gifs(gif_id, user):
    query = """
            SELECT id, obtain_date, gif_id, user_id FROM user_gifs
            WHERE gif_id = %s AND user_id = %s
            ORDER BY obtain_date DESC;
            """

    gifs_info = fetch_all(query, params=(gif_id, user.id))

    return gifs_info

# returns None if it doesn't find one
def find_user_gifs(gif_id, user):
    try:
        gifs = get_user_gifs(gif_id, user)
        if not len(gifs):
            return None
        return gifs
    except psycopg.DatabaseError as e:
        logger.info(e)
        return None
    except Exception as e:
        logger.info(e)
        return None


def find_user_gif_by_id(id):
    query = """
            SELECT * FROM user_gifs
            WHERE id = %s;
            """
    gif = fetch_dict(query, params=(id,))

    if gif is None:
        return None

    return gif



def check_add_user(user_info):
    query = """
            INSERT INTO users (user_id, username)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
            """

    exec_write(query, params=(user_info.id, user_info.name))

def get_user_info(user_id):
    query = """
            SELECT * FROM users
            WHERE user_id = %s;
            """

    user_info = fetch_dict(query, params=(user_id,))

    return dict(user_info)
    
def set_user_last_status(user_info):
    query = """
            UPDATE users
            SET last_status = NOW()
            WHERE user_id = %s;
            """ 

    exec_write(query, params=(user_info['user_id'],))


def add_user_gif(user_info, gif):
    query = """
            INSERT INTO user_gifs (user_id, gif_id)
            VALUES (%s, %s)
            """

    exec_write(query, params=(user_info['user_id'], gif['id'],))

def check_gif_in_fav(gif_id, user_id):
    query = """
            SELECT * FROM user_favorites
            WHERE user_id = %s AND gif_id = %s;
            """
    try:
        return fetch_dict(query, params=(user_id, gif_id,))
    except ValueError:
        return None

def add_fav_gif(gif, user):
    query = """
            INSERT INTO user_favorites (user_id, gif_id)
            VALUES (%s, %s);
            """
    exec_write(query, params=(user.id, gif['id'],))


def remove_fav_gif(gif_id, user_id):
    query = """
            DELETE FROM user_favorites 
            WHERE user_id = %s AND gif_id = %s;
            """
    exec_write(query, params=(user_id, gif_id,))


