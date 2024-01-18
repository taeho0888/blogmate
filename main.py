from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    videos = crud.get_videos(db)

    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "data": videos}
    )


@app.post("/video", response_model=schemas.Video)
async def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.create_video(db=db, video=video)


@app.delete("/video/{id}", status_code=204)
def delete_video(id: int, db: Session = Depends(get_db)):
    success = crud.delete_video(db=db, video_id=id)
    if not success:
        raise HTTPException(status_code=404, detail=f"id {id}인 비디오를 찾을 수 없습니다.")
    return {"message": "삭제 완료"}


@app.get("/detail/{id}", response_class=HTMLResponse)
def detail_page(request: Request, id:int, db: Session = Depends(get_db)):
    video = crud.get_video(db, id=id)
    script = crud.get_script(db, id=id)

    return templates.TemplateResponse(
        name="detail.html",
        context={"request": request, "video": video, "script": script}
    )


@app.post("/script/{id}", response_model=schemas.Script)
async def create_script(id: int, db: Session = Depends(get_db)):
    return crud.create_script(db=db, video_id=id)


@app.get("/blog/{script_id}/stream")
async def blog_stream(script_id: int):
    # This is a simple example. You'd have your logic to fetch and stream blog data.
    async for blog_update in generate_blog_content(script_id):
        yield f"data: {blog_update}\n\n"


async def generate_blog_content(script_id: int):
    pass