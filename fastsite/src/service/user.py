import os
from datetime import timedelta, datetime
from jose import jwt
from model.user import User
from passlib.context import CryptContext
from errors import Missing

# NOTE: The service layer is responsible for choosing the data source.
# The key part of the testing strategy.
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as data
else:
    from data import user as data

# SECURITY: Loading secrets from environment variables is critical.
# NEVER hardcode secrets in the source code.
SECRET_KEY: str = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for JWT. Please set this environment variable.")

ALGORITHM: str = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hash: str) -> bool:
    """Hash <plain> and compare with <hash> from the database"""
    return pwd_context.verify(plain, hash)

def get_hash(plain: str) -> str:
    """Return the hash of a <plain> string"""
    return pwd_context.hash(plain)

def get_jwt_username(token: str) -> str | None:
    """Return username from JWT access <token>"""
    try:
        payload: dict[str, str] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None
    return username

def get_current_user(token: str) -> User | None:
    """Decode an OAuth access <token> and return the User"""
    if not (username := get_jwt_username(token)):
        return None
    
    if (user := lookup_user(username)):
        return user
    
    return None

def lookup_user(username: str) -> User | None:
    """Return a matching User from the database for <name>"""
    try:
        # FIX: The data layer function is called get_one, not get.
        if (user := data.get_one_by_name(username)):
            return user
    except Missing:
        # NOTE: Robustly handle the case where get_one raises an error.
        return None
    return None

def auth_user(name: str, plain: str) -> User | None:
    """Authenticate user <name> and <plain> password"""
    # Add a check for empty password to fail fast
    if not name or not plain:
        return None
    
    try:
        # The rest of your logic can be wrapped in a try block
        if not (user := lookup_user(name)):
            return None
        if not verify_password(plain, user.hash):
            return None
        return user
    except Exception:
        # If any unexpected error occurs (e.g. from the data layer)
        # just return None to prevent a 500 error.
        return None

def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    """Return a JWT access token"""
    src: dict = data.copy()
    now: datetime = datetime.now()
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# CRUD

def get_all() -> list[User]:
    return data.get_all()

def get_one_by_name(name: str, table: str | None = None) -> User:
    if table is None:
        return data.get_one_by_name(name)
    else:
        return data.get_one_by_name(name, table)

def create(user: User) -> User:
    # SECURITY: The service layer is responsible for business logic, including security.
    # Hashing the password here ensures no plaintext password ever touches the data layer.
    user.hash = get_hash(user.hash)
    return data.create(user)

def modify(name: str, user: User) -> User:
    return data.modify(name, user)

def delete(name: str) -> None:
    return data.delete(name)
