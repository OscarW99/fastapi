from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get('message') == 'Hello World!'


# need to send data in the body for post requests
def test_create_user():
    res = client.post(
        '/users/', json={'email': 'gfroggy@gmail.com', 'password': 'eyo'})
    # can use schema model to do some of the validation for us (ie expected output fields/ format)
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'gfroggy@gmail.com'
    assert res.status_code == 201
