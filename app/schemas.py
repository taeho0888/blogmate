from pydantic import BaseModel


class VideoBase(BaseModel):
    video_url: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    thumbnail_url: str
    video_title: str
    channel_name: str

    class Config:
        from_attribute = True


class ScriptBase(BaseModel):
    video_id: int


class ScriptCreate(ScriptBase):
    pass


class Script(ScriptBase):
    id: int
    errored: bool | None = False
    script: str

    class Config:
        from_attribute = True


class BlogBase(BaseModel):
    blog: str
    errored: bool | None = False


class BlogCreate(BlogBase):
    script_id: int


class Blog(BlogBase):
    id: int

    class Config:
        from_attribute = True
