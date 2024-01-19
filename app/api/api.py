from fastapi import APIRouter

from .endpoints import blogs, home, scripts, videos


api_router = APIRouter()
api_router.include_router(blogs.router, prefix="/blog")
api_router.include_router(home.router)
api_router.include_router(scripts.router, prefix="/script")
api_router.include_router(videos.router, prefix="/video")