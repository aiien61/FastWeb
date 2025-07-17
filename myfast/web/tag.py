from fastapi import FastAPI, HTTPException
from datetime import datetime
from model.tag import TagIn, Tag, TagOut
import service.tag as service

app = FastAPI()

@app.post("/")
def create(tag_in: TagIn) -> TagIn:
    tag: Tag = Tag(tag=tag_in.tag, created=datetime.now(), secret="shhh")
    service.create(tag)
    return tag_in

@app.get("/{tag_str}", response_model=TagOut)
def get_one(tag_str: str) -> TagOut:
    tag: Tag = service.get(tag_str)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagOut(tag=tag.tag, created=tag.created)
