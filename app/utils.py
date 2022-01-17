from passlib.context import CryptContext

# Just saying that bcrypt is the hashing algorithm we want to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# function to hash pasword based on hashing algo in pwd_context
def hash(password: str):
    return pwd_context.hash(password)


# function to take a raw password, hash it and compare it to a password in the database (based on hashing algo in pwd_context)
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
