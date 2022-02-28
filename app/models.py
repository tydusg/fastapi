from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


# Sqlalchemy function used to create a base class
# We'll pass this into our class when making them
Base = declarative_base()


# Create the Post table
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True")

    # Create a timestamp
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    
    # Create a Foreign Key referencing id column from "users" table
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Returns the user based on the owner_id
    # Uses the class name, not the table name
    owner = relationship("User")


# Create the User table
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    # Create a timestamp
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")) 


# Create the Vote table
class Vote(Base):
    __tablename__ = "votes"
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True) 