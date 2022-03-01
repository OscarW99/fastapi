from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

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
@pytest.fixture
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
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# This fixture will create a new user -> this user wil be used for downstream CRUD testing
@pytest.fixture
def test_user(client):
    user_data = {'email': 'oscar-wright@mail.com', 'password': 'password'}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    # new user is a json with everything in schemas.UserOut but also with password
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {'email': '2oscar-wright@mail.com', 'password': 'password'}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


# So the client is basically the user and they need authorization to send requests. Mkaing an authorized client fixture will save us authorizing the client every time.
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# This fixture will allow us to test our get post functions as we need posts in the database for this.
@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [
        {
            'title': 'this is title',
            'content': 'this is content',
            'user_id': test_user['id']
        },
        {
            'title': 'this is title2',
            'content': 'this is content2',
            'user_id': test_user['id']
        },
        {
            'title': 'this is title3',
            'content': 'this is content3',
            'user_id': test_user['id']
        },
        {
            'title': 'this is title4',
            'content': 'this is content3',
            'user_id': test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = list(map(create_post_model, post_data))

    session.add_all(post_map)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
