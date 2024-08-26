from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse

import uw_design_class.database_models as models
from uw_design_class.database_connection import get_db
from uw_design_class.singleton_logger import SingletonLogger

app = FastAPI()

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = SingletonLogger()

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    logger.log(f"Accessed home page with {len(posts)} posts", module="API-Routes")
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@router.post("/create-post")
def create_post(request: Request, 
                title: str = Form(...), 
                content: str = Form(...),
                authorid: str = Form(None),  # Make it optional in the form
                blogid: str = Form(None),    # Make it optional in the form
                db: Session = Depends(get_db)):
    
    # Use default values if not provided
    authorid = int(authorid) if authorid else 1
    blogid = int(blogid) if blogid else 1

    db_post = models.Post(
        title=title,
        content=content,
        publisheddate=datetime.now(),
        authorid=authorid,
        blogid=blogid
    )
    db.add(db_post)
    db.commit()
    logger.log(f"Created post with title: {title}", module="API-Routes")
    return RedirectResponse("/", status_code=303)

@router.get("/posts/{post_id}", response_class=HTMLResponse)
def read_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.postid == post_id).first()
    if not post:
        logger.log(f"Attempted to access non-existing post with id: {post_id}", module="API-Routes")
        raise HTTPException(status_code=404, detail="Post not found")
    logger.log(f"Accessed post with id: {post_id}", module="API-Routes")
    return templates.TemplateResponse("single_post.html", {"request": request, "post": post})

@router.get("/update-post/{post_id}", response_class=HTMLResponse)
def update_post_form(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.postid == post_id).first()
    if not post:
        logger.log(f"Attempted to update non-existing post with id: {post_id}", module="API-Routes")
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("update_post.html", {"request": request, "post": post})



@router.post("/commit-update-post/{post_id}")
def update_post_in_db(post_id: int, title: str = Form(...), content: str = Form(...),
                      authorid: int = Form(...), blogid: int = Form(...), db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.postid == post_id).first()
    if not db_post:
        logger.log(f"Attempted to update non-existing post with id: {post_id}", module="API-Routes")
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Update the fields with new data
    db_post.title = title
    db_post.content = content
    db_post.authorid = authorid
    db_post.blogid = blogid
    db_post.publisheddate = datetime.now()  # Optional: update the publish date to the current time
    
    db.commit()
    db.refresh(db_post)
    logger.log(f"Updated post with id: {post_id}", module="API-Routes")
    return RedirectResponse(f"/posts/{post_id}", status_code=303)

@router.post("/delete-post/{post_id}")
def delete_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.postid == post_id).first()
    if not db_post:
        logger.log(f"Attempted to delete non-existing post with id: {post_id}", module="API-Routes")
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    logger.log(f"Deleted post with id: {post_id}", module="API-Routes")
    return RedirectResponse("/", status_code=303)

# Include the router in the FastAPI app
app.include_router(router)
