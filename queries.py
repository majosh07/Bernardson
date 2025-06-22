from pool import pool
import psycopg
from psycopg.rows import dict_row
from logging_config import logger


def fetch_value(query, params=None, commit=False):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SET TIME ZONE 'US/Eastern';")
                cur.execute(query, params)

                res = cur.fetchone()
                if res is None:
                    return None
                    # raise ValueError(f"No result from:\n{query}\nParams:\n{params}")

                if commit:
                    conn.commit()

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

def fetch_all(query, params=None, commit=False):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SET TIME ZONE 'US/Eastern';")
                cur.execute(query, params)

                res =  cur.fetchall()
                if res is None:
                    raise ValueError(f"No result from:\n{query}\nParams:\n{params}")

                if commit:
                     conn.commit()

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

def fetch_count(query, params=None, commit=False):
     with pool.connection() as conn:
         with conn.cursor() as cur:
            try:
                cur.execute("SET TIME ZONE 'US/Eastern';")
                cur.execute(query, params)

                res =  cur.fetchone()
                if res is None:
                    raise ValueError(f"No result from:\n{query}\nParams:\n{params}")

                if commit:
                     conn.commit()

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

def fetch_dict(query, params=None, commit=False):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            try:
                cur.execute("SET TIME ZONE 'US/Eastern';")
                cur.execute(query, params)

                row =  cur.fetchone()
                if row is None:
                    return None
                    # raise ValueError(f"No result from:\n{query}\nParams:\n{params}")

                if commit:
                     conn.commit()
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

def exec_write(query, params=None, commit=True):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            try:
                cur.execute("SET TIME ZONE 'US/EASTERN';") 
                cur.execute(query, params)

                if commit:
                     conn.commit()

            except psycopg.IntegrityError:
                logger.exception("Integrity error:")  # e.g. duplicate key, not null violation
            except psycopg.OperationalError:
                logger.exception("Operational error:")  # e.g. connection issues
            except psycopg.DatabaseError:
                logger.exception("Database error:")  # general DB issues
            except Exception:
                logger.exception("Other error:")  # fallback

def fetch_dict_all(query, params=None, commit=False):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            try:
                cur.execute("SET TIME ZONE 'US/Eastern';")
                cur.execute(query, params)

                row =  cur.fetchall()
                if row is None:
                    return None
                    # raise ValueError(f"No result from:\n{query}\nParams:\n{params}")

                if commit:
                     conn.commit()
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
