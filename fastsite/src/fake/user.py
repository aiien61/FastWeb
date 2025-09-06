from model.user import User
from errors import Missing, Duplicate

fakes = [
    User(name="kiwijobo", hash="newzealand"),
    User(name="emanager", hash="compani")
]

def find(name: str) -> User | None:
    for _user in fakes:
        if _user.name == name:
            return _user
    return None

def check_missing(name: str):
    if not find(name):
        raise Missing(msg=f"Missing user {name}")
    
def check_duplicate(name: str):
    if find(name):
        raise Duplicate(msg=f"Duplicate user {name}")

def get_all() -> list[User]:
    """Return all users"""
    return fakes

def get_one_by_name(name: str) -> User:
    """Return one user"""
    check_missing(name)
    return find(name)

def create(user: User) -> User:
    """Add a user"""
    check_duplicate(user.name)
    fakes.append(user)
    return fakes[-1]

def modify(name: str, user: User) -> User:
    """Partially modify a user"""
    check_missing(name)
    id_to_modify: int = None
    for id, _user in enumerate(fakes):
        if _user.name == name:
            fakes[id] = user
            id_to_modify = id
            break

    return fakes[id_to_modify]

def delete(name: str) -> None:
    """Delete a user"""
    check_missing(name)
    id_to_delete: int = None
    for id, _user in enumerate(fakes):
        if _user.name == name:
            id_to_delete = id
            break

    fakes.pop(id_to_delete)
    return None
