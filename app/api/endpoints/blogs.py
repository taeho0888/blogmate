from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_blog
from app.api.deps import get_db


router = APIRouter()


@router.post("/{script_id}", response_model=schemas.Blog)
async def create_blog(script_id: int, db: Session = Depends(get_db)):
    return crud_blog.create(db=db, script_id=script_id)


@router.get("/{id}", response_model=schemas.Blog)
async def get_blog(id: int, db: Session = Depends(get_db)):
    return crud_blog.get(db=db, id=id)