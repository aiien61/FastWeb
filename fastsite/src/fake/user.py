from model.user import User
from errors import Missing, Duplicate

fakes = [
    User(name="kiwijobo", hash="newzealand"),
    User(name="emanager", hash="compani")
]

def find(name: str) -> User | None:
    for e in fakes:
        if e.name == name:
            return e
    return None

def check_missing(name: str):
    if not find(name):
        raise Missing(msg=f"Missing user {name}")
    
def check_duplicate(name: str):
    if find(name):
        raise Duplicate(msg=f"Duplicate user {name}")

# TODO: complete get_all() connection with db
def get_all() -> list[User]:
    """Return all users"""
    return fakes

def get_one(name: str) -> User:
    """Return one user"""
    check_missing(name)
    return find(name)

# TODO: complete create() connection with db
def create(user: User) -> User:
    """Add a user"""
    check_duplicate(user.name)
    return user

# TODO: complete modify() connection with db
def modify(name: str, user: User) -> User:
    """Partially modify a user"""
    check_missing(name)
    return user

# TODO: complete delete() connection with db
def delete(name: str) -> None:
    """Delete a user"""
    check_missing(name)
    return None
