from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import database, models, schemas, oauth2
from typing import List, Optional
from http import HTTPStatus
from sqlalchemy import func

router = APIRouter(prefix='/posts', tags=["posts"])

# Get all posts
# Structure => @router.method (route, status_code, response_model)
# Function name with type hinting on db session
# sql operation via sqlalchemy orm
# return data
# @router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostWithVote])
def get_all_posts(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# Create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.NewPost, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Delete post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    post_to_delete = db.query(models.Post).filter(models.Post.id == id)
    if not post_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post_to_delete.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not allowed")
    
    post_to_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT.value)

# Update post by id
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def put_post(id: int, post: schemas.NewPost, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)
    if not post_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post_to_update.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not allowed")
    post_to_update.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_to_update.first()

# Get all own posts
@router.get("/own", status_code=status.HTTP_200_OK, response_model=List[schemas.PostWithVote])
def get_all_own_posts(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    all_posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()
    return all_posts

# Get post by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostWithVote)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post.first()

