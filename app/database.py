# This file just sets up the ORM, to connect it to postgres. Can copy and paste this for every project.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency # function to conect to database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



###############################
##### connect to database #####
# Can copy and paste for any project #
# ! we are using sqlalchemy now instead to connect to database. I will keep this here for documentation purposes.
###############################
# while True:
#     try:
#         # Connect to your postgres DB
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         # Open a cursor to perform database operations
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(5)
###############################