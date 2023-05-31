from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

router = APIRouter()


@router.post("/blog-posts", status_code=201, response_model=schemas.BlogPost)
def create_blog_post(blog_post: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    new_blog_post = models.BlogPost(title=blog_post.title, content=blog_post.content, author_id=blog_post.author_id)
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)
    return new_blog_post


@router.get("/blog-posts/{blog_post_id}", response_model=schemas.BlogPost)
def read_blog_post(blog_post_id: int, db: Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_post_id).first()
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog_post


@router.put("/blog-posts/{blog_post_id}", response_model=schemas.BlogPost)
def update_blog_post(blog_post_id: int, blog_post: schemas.BlogPostUpdate, db: Session = Depends(get_db)):
    existing_blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_post_id).first()
    if not existing_blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    existing_blog_post.title = blog_post.title
    existing_blog_post.content = blog_post.content
    db.commit()
    db.refresh(existing_blog_post)
    return existing_blog_post


@router.delete("/blog-posts/{blog_post_id}")
def delete_blog_post(blog_post_id: int, db: Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_post_id).first()
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    db.delete(blog_post)
    db.commit()
    return {"message": "Blog post deleted"}


@router.post("/comments", status_code=201, response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    new_comment = models.Comment(content=comment.content, author_id=comment.author_id,
                                 blog_post_id=comment.blog_post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/comments/{comment_id}", response_model=schemas.Comment)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/comments/{comment_id}", response_model=schemas.Comment)
def update_comment(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)):
    existing_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    existing_comment.content = comment.content
    db.commit()
    db.refresh(existing_comment)
    return existing_comment


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}
