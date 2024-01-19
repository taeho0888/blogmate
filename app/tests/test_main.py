from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.api.deps import get_db

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_video():
    response = client.post(
        "/video/", 
        json = {
            "video_url": "s8kBm_Eb6lE", 
            "video_title": "절대 망할 수 없는 테이블 9개 탑티어 삼겹살집", 
            "channel_name": "정육왕 MeatCreator"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["video_url"] == "s8kBm_Eb6lE"
    assert data["video_title"] == "절대 망할 수 없는 테이블 9개 탑티어 삼겹살집"
    assert data["channel_name"] == "정육왕 MeatCreator"
    video_id = data["id"]

    response = client.delete(f"/video/{video_id}")
    assert response.status_code == 204


def test_delete_video():
    response = client.post(
        "/video/", 
        json={
            "video_url": "s8kBm_Eb6lE", 
            "video_title": "절대 망할 수 없는 테이블 9개 탑티어 삼겹살집", 
            "channel_name": "정육왕 MeatCreator"
        }
    )
    video_id = response.json()["id"]

    response = client.delete(f"/video/{video_id}")
    assert response.status_code == 204

    response = client.delete(f"/video/{video_id}")
    assert response.status_code == 404
