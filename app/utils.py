from passlib.context import CryptContext

# Creates a CryptContext needed in hashing and verifying a password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashes a password
def hash(password: str):
    return pwd_context.hash(password)

# Verifies a password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)