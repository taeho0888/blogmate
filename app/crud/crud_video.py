import os
import dotenv
import requests

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models, schemas

dotenv.load_dotenv()
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


def get(db: Session, id: int):
    return db.query(models.Video).filter(models.Video.id == id).first()


def list(db: Session):
    return db.query(models.Video).order_by(desc(models.Video.id)).all()


def create(db: Session, video: schemas.VideoCreate):
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


def delete(db: Session, video_id: int):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()

    if video:
        db.delete(video)
        db.commit()
        return True
    else:
        return False


def get_video_info(video_id: str):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        raise ValueError(f"Request 오류, status code={response.status_code}")

    response_json = response.json()

    if not response_json.get('items') or not response_json['items']:
        print(f"response['item'] 없음: {response_json}")
        raise ValueError("해당 video id에 대한 정보 없음")
    
    try:
        thumbnail_url = response_json['items'][0]['snippet']['thumbnails']['default']['url']
        video_title = response_json['items'][0]['snippet']['title']
        channel_name = response_json['items'][0]['snippet']['channelTitle']
    except (IndexError, KeyError) as e:
        print(f"동영상 정보 추출 에러: {e}")
        print(f"Response JSON: {response_json}")
        raise ValueError("Failed to extract video info.")

    return thumbnail_url, video_title, channel_name
