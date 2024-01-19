from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.api.deps import get_db
from app.crud import crud_script

router = APIRouter()


@router.post("/{id}", response_model=schemas.Script)
async def create_script(id: int, db: Session = Depends(get_db)):
    return crud_script.create(db=db, video_id=id)
