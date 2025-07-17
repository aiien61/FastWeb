from model.tag import Tag
from typing import Optional

# This is a simplified in-memory database for demo purposes.
# In a real app, interact with a proper db instead.
_tags_db = {}

def create(tag: Tag) -> None:
    """
    Saves a new Tag object.
    """
    _tags_db[tag.tag] = tag

def get(tag_str: str) -> Optional[Tag]:
    """
    Retrieves a Tag object by its tag string.
    """
    return _tags_db.get(tag_str)
