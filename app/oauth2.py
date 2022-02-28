from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models, config
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


# I actually need to learn more about this
# This is used as a dependency on the token scheme
# But I'm unsure how this is necessary
# Maybe for OpenAPI purpose? Type hinting? 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret key, algorithm, expiration time
SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
EXPIRATION_TIME = config.settings.access_token_expire_minutes


# Function that uses jwt to create an access token
# JWT uses header + payload + signature (which uses secret key) to use a token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    
    # Create access token
    access_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return access_token


# Verifies an access token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")   
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    return token_data

# Once the verify_access_token function verifies a token, returns the owner of the token (user object from "users" table)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
        )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
    
    