import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

from sqlalchemy import desc
from sqlalchemy.orm import Session

import models, schemas

load_dotenv()

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MAX_SCRIPT_LENGTH = 1700
client = OpenAI(api_key=OPENAI_API_KEY)

def get_video(db: Session, id: int):
    return db.query(models.Video).filter(models.Video.id == id).first()


def get_videos(db: Session):
    return db.query(models.Video).order_by(desc(models.Video.id)).all()


def create_video(db: Session, video: schemas.VideoCreate):
    thumbnail_url, video_title, channel_name = get_video_info(video.video_url)

    db_video = models.Video(
        video_url=video.video_url,
        thumbnail_url=thumbnail_url, 
        video_title=video_title,
        channel_name=channel_name
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def delete_video(db: Session, video_id: int):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()

    if video:
        db.delete(video)
        db.commit()
        return True
    else:
        return False


def create_script(db: Session, video_id: int):
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


def get_script(db: Session, id: int):
    return db.query(models.Script).filter_by(video_id=id).first()


def create_blog(db: Session, script_id: int):
    db_script = db.query(models.Script).filter_by(id=script_id).first()
    if db_script:
        script = db_script.script
    else:
        raise ValueError
    
    blog, errored = get_blog_info(script)

    db_blog = models.Blog(
        script_id=script_id,
        blog=blog,
        errored=errored
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def get_blog(db: Session, id: int):
    return db.query(models.Blog).filter(models.Blog.id == id).first()


def get_blog_by_script_id(db: Session, script_id: int):
    return db.query(models.Blog).filter(models.Blog.script_id == script_id).first()


def get_video_info(video_url: str):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_url}&key={YOUTUBE_API_KEY}"
    
    response = requests.get(url)

    if response.status_code != 200:
        print(response.status_code)
        raise ValueError
    
    response_json = response.json()
    thumbnail_url = response_json['items'][0]['snippet']['thumbnails']['default']['url']
    video_title = response_json['items'][0]['snippet']['title']
    channel_name = response_json['items'][0]['snippet']['channelTitle']

    return thumbnail_url, video_title, channel_name


def get_script_info(video_url: str):
    try:
        print(video_url)
        scripts = YouTubeTranscriptApi.get_transcript(video_url, languages=['ko'])
        script = " ".join(script['text'] for script in scripts)
        errored = False
    except Exception as e:
        print(e)
        script = f"[오류] : {e}"
        errored = True

    return script, errored


PROMPT = """
            You are a summarizer and I'm a client. 
            I'll give you the script of a YouTube video, and you should summarize that. 
            Please summarize the video script and divide it into several paragraphs.
            Please give me a summary of the summary you just sent me by numbering it so that I can see it at a glance.
            Write it with Korean.
        """

def get_blog_info(script: str):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{PROMPT}"},
                {"role": "user", "content": f"{script[:MAX_SCRIPT_LENGTH]}"}
            ],
            max_tokens=2000,
            temperature=1
        )
        blog = str(response.choices[0].message.content)
        errored = False
    except Exception as e:
        blog = f"[GPT 오류] {e}"
        errored = True

    return blog, errored

    
    