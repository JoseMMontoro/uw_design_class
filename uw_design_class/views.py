
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse

from uw_design_class.database_setup import get_db
from uw_design_class.services import (create_new_post, delete_post,
                                      get_post_by_id, get_posts, update_post)
from uw_design_class.singleton_logger import SingletonLogger

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = SingletonLogger()

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    posts = get_posts(db)
    logger.log(f"Accessed home page with {len(posts)} posts", module="View-Routes")
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@router.post("/create-post")
def create_post(title: str = Form(...), content: str = Form(...), authorid: str = Form(None), blogid: str = Form(None), db: Session = Depends(get_db)):
    create_new_post(db, title, content, authorid, blogid)
    logger.log(f"Created post with title: {title}", module="View-Routes")
    return RedirectResponse("/", status_code=303)

@router.get("/posts/{post_id}", response_class=HTMLResponse)
def read_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        logger.log(f"Attempted to access non-existing post with id: {post_id}", module="View-Routes")
        raise HTTPException(status_code=404, detail="Post not found")
    logger.log(f"Accessed post with id: {post_id}", module="View-Routes")
    return templates.TemplateResponse("single_post.html", {"request": request, "post": post})

@router.get("/update-post/{post_id}", response_class=HTMLResponse)
def update_post_form(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        logger.log(f"Attempted to update non-existing post with id: {post_id}", module="View-Routes")
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("update_post.html", {"request": request, "post": post})

@router.post("/commit-update-post/{post_id}")
def update_post_in_db(post_id: int, title: str = Form(...), content: str = Form(...), authorid: int = Form(...), blogid: int = Form(...), db: Session = Depends(get_db)):
    update_post(db, post_id, title, content, authorid, blogid)
    logger.log(f"Updated post with id: {post_id}", module="View-Routes")
    return RedirectResponse(f"/posts/{post_id}", status_code=303)

@router.post("/delete-post/{post_id}")
def delete_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    delete_post(db, post_id)
    logger.log(f"Deleted post with id: {post_id}", module="View-Routes")
    return RedirectResponse("/", status_code=303)
