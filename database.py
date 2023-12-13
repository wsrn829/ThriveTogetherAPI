import psycopg2
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Modify these values with your PostgreSQL credentials

load_dotenv()

db_user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('PORT')


db_config = {
    'user': db_user,
    'password': password,
    'dbname': db_name,
    'host': host
}

DATABASE_URL = f'postgresql://{db_user}:{password}@{host}:{port}/{db_name}'


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# def create_database_engine():
#     return create_engine(DATABASE_URI)


def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)
        return connection
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")


def close_connection(connection):
    if connection:
        connection.close()
