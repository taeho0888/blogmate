from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_url = Column(String, index=True)
    thumbnail_url = Column(String)
    channel_name = Column(String)
    video_title = Column(String)

    scripts = relationship("Script", back_populates="video", cascade="all, delete-orphan")


class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    script = Column(Text)
    errored = Column(Boolean, default=False)

    video = relationship("Video", back_populates="scripts")
    blog = relationship("Blog", uselist=False, back_populates="script", cascade="all, delete-orphan")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    script_id = Column(Integer, ForeignKey("scripts.id"))
    blog = Column(Text)
    errored = Column(Boolean, default=False)

    script = relationship("Script", back_populates="blog")
