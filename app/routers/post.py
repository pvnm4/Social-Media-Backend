from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import Optional,List
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth2
from app.database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.Post])
async def get_post(db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user),
                         Limit: int = 10, skip: int = 0, search: Optional[str] = ""):
          
          #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
          posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
          return posts


@router.get("/{id}",response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
        post = db.query(models.Post).filter(models.Post.id == id ).first()
        
        if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Post with the id:{id} was not found")
        return post



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post )
async def create_post(post: schemas.CreatePost, db: Session = Depends(get_db),
                       current_user : int = Depends(oauth2.get_current_user) ):
            

        
            new_post = models.Post(owner_id= current_user.id, **post.dict())
            db.add(new_post)
            db.commit()
            db.refresh(new_post)

            return new_post




@router.delete("/{id}")
async def get_post(id: int, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
        post_query = db.query(models.Post).filter(models.Post.id == id)
        
        post = post_query.first()

        if post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Post with the id:{id} was not found")
        
        if post.owner_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Post withe id:{id} does not exists")
        

        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}",response_model=schemas.Post)
async def get_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
        post_query = db.query(models.Post).filter(models.Post.id == id)
        
        post = post_query.first()

        if post == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Post with the id:{id} does not exists")
        
        if post.owner_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Not authorized to perform requested action")
        
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()
