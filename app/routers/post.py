from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from  sqlalchemy.orm import Session,aliased
from sqlalchemy import func
from ..database import engine, get_db
from typing import  List, Optional


router = APIRouter(
    prefix = "/posts" ,
tags = ["posts"] # this instead of putting /posts in all routers
)
@router.get("/", response_model=List[schemas.PostOut]) # get all post
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts """ )
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   # Assuming you want to count votes per post and get the posts with their vote counts
    posts_query = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label("votes")
    ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
    .group_by(models.Post.id)  # Group by the post ID

    posts = posts_query.all()  # Make sure to call .all() on the query object, not on a list
    return  posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)  #201 to display a created post
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):   # this will check for title and content and str
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(new_post1.title,
                    #new_post1.content, new_post1.published)) # the %s is to avoid sql injection
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post (owner_id = current_user.id, **post.dict())# this unpack the dict and also like a short code or(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # is like RETURNING
    return  new_post

@router.get("/{id}", response_model=schemas.PostOut) # geting a post with a specific id
def get_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):     # to convert id to int     # response: Response response is to make sure it tells the front end when we put in an id that does not exist
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    #post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    posts_query = db.query(
            models.Post, 
            func.count(models.Vote.post_id).label("votes")
        ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id)  # Group by the post ID

    post = posts_query.filter(models.Post.id == id).first()  # Make sure to call .all() on the query object, not on a list
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT )
def delete_post (id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deleting post
    #cursor.execute("""DELETE  FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post =  cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post =  post_query.first()
    if post is None:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")  
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    post_query.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)  #so we dont send a message back after delete

@router.put("/{id}", response_model=schemas.Post)
def updated_posts(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
    #                 RETURNING *""",(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


