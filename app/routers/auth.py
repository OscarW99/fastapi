from fastapi import FastAPI, APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import schemas, models, database, utils


router = APIRouter(
    tags=['Authentication']
)


# * LOOGIN
@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()
    # check email is correct
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    # check password is correct
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    # create a token and return it
    return {'token': 'example token!'}
