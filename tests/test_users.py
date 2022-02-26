from app import schemas
from .database import client, session


#################


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello World!'


# need to send data in the body for post requests
def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'gfroggy@gmail.com', 'password': 'eyo'})
    # can use schema model to do some of the validation for us (ie expected output fields/ format)
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'gfroggy@gmail.com'
    assert res.status_code == 201


def test_login_user(client):
    res = client.post(
        '/login', data={'username': 'gfroggy@gmail.com', 'password': 'eyo'})

    assert res.status_code == 200
