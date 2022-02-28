import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings



# Properly parse passwords containing special characters
password = urllib.parse.quote_plus(settings.database_password)

# Create an engine connected to Postgres along with the proper authentication and address
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session object in order to interact with the database
Session = sessionmaker(bind=engine)

# Helper function to create a session
# From FastAPI docs
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()