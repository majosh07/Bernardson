from sqlalchemy import create_engine
from models import Base

SUPABASE_DB_URL = "postgresql+psycopg://postgres.hqutnvpijstopdxvvhux:we_l0ve_bern%40rdSON@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
LOCAL_DB_URL = "postgresql+psycopg://majosh:we_l0ve_bern%40rdSON@localhost:5432/bernardson"

engine = create_engine(LOCAL_DB_URL, echo=True)

Base.metadata.create_all(engine)
