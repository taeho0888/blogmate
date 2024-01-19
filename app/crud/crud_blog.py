import os
from dotenv import load_dotenv
from openai import OpenAI

from sqlalchemy.orm import Session

from app import models

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MAX_SCRIPT_LENGTH = 1700
CLIENT = OpenAI(api_key=OPENAI_API_KEY)
PROMPT = """
            You are a summarizer and I'm a client. 
            I'll give you the script of a YouTube video, and you should summarize that. 
            Please summarize the video script and divide it into several paragraphs.
            Please give me a summary of the summary you just sent me by numbering it so that I can see it at a glance.
            Write it with Korean.
        """


def create(db: Session, script_id: int):
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


def get(db: Session, id: int):
    return db.query(models.Blog).filter(models.Blog.id == id).first()


def get_by_script_id(db: Session, script_id: int):
    return db.query(models.Blog).filter(models.Blog.script_id == script_id).first()


def get_blog_info(script: str):
    try:
        response = CLIENT.chat.completions.create(
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
