from youtube_transcript_api import YouTubeTranscriptApi

from sqlalchemy.orm import Session

from app import models


def create(db: Session, video_id: int):
    video = db.query(models.Video).filter_by(id=video_id).first()
    if video:
        video_url = video.video_url
    else:
        raise ValueError
    
    script, errored = get_script_info(video_url)

    db_script = models.Script(
        video_id=video_id,
        script=script,
        errored=errored
    )
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script


def get(db: Session, id: int):
    return db.query(models.Script).filter_by(video_id=id).first()


def get_script_info(video_url: str):
    try:
        print(video_url)
        scripts = YouTubeTranscriptApi.get_transcript(video_url, languages=['ko', 'en'])
        script = " ".join(script['text'] for script in scripts)
        errored = False
    except Exception as e:
        print(e)
        script = f"[오류] : {e}"
        errored = True

    return script, errored
