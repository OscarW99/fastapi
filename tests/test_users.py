import pytest
from jose import jwt
from app import schemas
from app.config import settings


#################


def test_root(client):  # you put fixtures inside of the brackets for a test function
    res = client.get("/")
    assert res.json().get('message') == 'Hello World!'


# need to send data in the body for post requests
def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'gfroggyff@gmail.com', 'password': 'eyo'})
    # can use schema model to do some of the validation for us (ie expected output fields/ format)
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'gfroggyff@gmail.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrong_email", 'password', 403),
    ("oscar-wright@mail.com", 'wrong_password', 403),
    (None, 'password', 422),
    ("oscar-wright@mail.com", None, 422),
    ("oscar-wright@mail.com", 'wrong_password', 403)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        '/login',  data={'username': email, 'password': password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'
