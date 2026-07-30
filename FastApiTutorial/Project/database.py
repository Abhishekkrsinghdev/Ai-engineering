from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

db_url=URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT",3306)),
    database=os.getenv("DB_NAME")
)

engine=create_engine(db_url)

metadata=MetaData()

Sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()