from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import crud_video
from app.crud import crud_blog, crud_script, crud_video

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    videos = crud_video.list(db)

    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "data": videos}
    )


@router.get("/detail/{id}", response_class=HTMLResponse)
def detail_page(request: Request, id:int, db: Session = Depends(get_db)):
    video = crud_video.get(db, id=id)
    script = crud_script.get(db, id=id)
    if script:
        blog = crud_blog.get_by_script_id(db, script_id=script.id)
    else:
        blog = None

    return templates.TemplateResponse(
        name="detail.html",
        context={
            "request": request, 
            "video": video, 
            "script": script,
            "blog": blog
        }
    )
