from fastapi import APIRouter
from fastapi import Depends, APIRouter, HTTPException, Request, Response, status
from typing import List, Optional
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Post, User 
from fastapi.templating import Jinja2Templates
from schema.post import PostBase, PostOauth
import oauth2
from schema.user import UserBase

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.get("/", response_model=List[PostBase])
def get_user_posts(
        db: Session = Depends(get_db), 
        current_user: User = Depends(oauth2.get_current_user),
        skip: int = 0,
        limit:int=10,
        search: Optional[str]=""):

    posts: List[Post] = db.query(Post).\
        filter(Post.user_id==current_user.id).\
        filter(Post.title.contains(search)).\
        limit(limit).offset(skip).all()
    
    return posts


@router.get("/{id}", status_code=200)
def get_post(
        id:int,
        db: Session = Depends(get_db),
        current_user: User = Depends(oauth2.get_current_user)):
    
    post = db.query(Post).filter(Post.id==id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exit"
        )
    if post.user_id != current_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return {'message': post}


@router.post("/", status_code= status.HTTP_201_CREATED)
async def create_post(new_post: PostOauth,
                    db: Session = Depends(get_db),
                    current_user = Depends(oauth2.get_current_user)):
    post_information = new_post.dict()
    post_information.update({"user_id":current_user.id})
    print(post_information)
    post = Post(**post_information)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id}")
def delete_user(id: int, db: Session=Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    post = db.query(Post).filter(PostBase.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exit"
        )
    if post.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return {"data":"post deleted",
            "deleted post": post.first()}



@router.put('/{post_id}')
async def update_post(post_update: PostBase, post_id:int, db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    post = db.query(Post).filter(Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post with id {post_id} does not exit"
        )
    post.update(post_update.dict(), synchronize_session=False)
    db.commit()
    return {'msg':'post updated'}