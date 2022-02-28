from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils
from typing import List

router = APIRouter(prefix='/users', tags=["users"])

# Create new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.NewUser, db: Session = Depends(database.get_db)):
    
    user.password = utils.hash(user.password)    
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_all_users(db: Session = Depends(database.get_db)):
    all_users = db.query(models.User).all()
    return all_users

# Get user by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user.first()

# Delete a user
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):
    user_to_delete = db.query(models.User).filter(models.User.id == id)
    if not user_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user_to_delete.first())
    db.commit()
    return