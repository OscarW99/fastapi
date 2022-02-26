from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base

# set database address + create connection
#@###########
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
#@###########


# We can set the scope of a fixture - usefulll when we don't want to clear our db tables after testing login as then we can test other things that require us to be logged in.
# drop all tables in test db, add all tables fresh, try to yield db
@pytest.fixture(scope='module')  # !########
def session():
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# override prod db to be test db and yield it. Then yield testing client.
# yield basically works by allowing us to run some code before and some code after our test has run.
@pytest.fixture(scope='module')  # !########
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
