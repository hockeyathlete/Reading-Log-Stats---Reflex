import reflex as rx
# from dotenv import load_dotenv
from sqlmodel import create_engine
# import os # Import the os module

# Retrieve the DATABASE_URL from environment variables
# Provide a default value for local development if not set, or raise an error if critical
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine("psql 'postgresql://neondb_owner:npg_wTSH6B2oaKGF@ep-blue-silence-ae8a2zpy-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'")

def create_db_and_tables():
    from app.models import SQLModel
    SQLModel.metadata.create_all(engine)
