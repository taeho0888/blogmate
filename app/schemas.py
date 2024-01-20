from pydantic import BaseModel, ConfigDict


class VideoBase(BaseModel):
    video_url: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    model_config = ConfigDict(from_attribute=True)

    id: int
    thumbnail_url: str
    video_title: str
    channel_name: str


class ScriptBase(BaseModel):
    video_id: int


class ScriptCreate(ScriptBase):
    pass


class Script(ScriptBase):
    model_config = ConfigDict(from_attribute=True)

    id: int
    errored: bool | None = False
    script: str


class BlogBase(BaseModel):
    blog: str
    errored: bool | None = False


class BlogCreate(BlogBase):
    script_id: int


class Blog(BlogBase):
    model_config = ConfigDict(from_attribute=True)

    id: int
