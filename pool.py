from dotenv import load_dotenv
import os
from psycopg_pool import AsyncConnectionPool


load_dotenv()

db_url = os.environ.get('DATABASE_URL')

if db_url:
    pool = AsyncConnectionPool(conninfo=db_url, min_size=1, max_size=2, open=False, max_lifetime=300,)

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
    pool = AsyncConnectionPool(conninfo=conn_info, open=False, max_lifetime=300)

    # add logging here


