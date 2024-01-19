from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_video
from app.api.deps import get_db


router = APIRouter()


@router.post("/", response_model=schemas.Video)
async def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud_video.create(db=db, video=video)


@router.delete("/{id}", status_code=204)
def delete_video(id: int, db: Session = Depends(get_db)):
    success = crud_video.delete(db=db, video_id=id)
    if not success:
        raise HTTPException(status_code=404, detail=f"id {id}인 비디오를 찾을 수 없습니다.")
    return {"message": "삭제 완료"}
