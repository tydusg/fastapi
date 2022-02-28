from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# Create database tables, if not already present (based on models in models.py)
# from . import models, database
# models.Base.metadata.create_all(database.engine)
# We have alembic now to take care of managing the database structure

# Create an instance of the FastAPI app
app = FastAPI()

origins = ["https://www.google.com"]


# CORS middleware stuff
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )




# Import the routers (from routers/ post.py, user.py, auth.py)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Sample path operation based on '/' or root endpoint
@app.get('/')
def root():
    return {"message": "Welcome to my API. This is the root"}