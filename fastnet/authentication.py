from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from jose import JWSError, jwt
from passlib.context import CryptContext

SECURITY_KEY: str = "WHATEVER-KEY-YOU-LIKE"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

# ----- fake DB -----
fake_users_db: dict = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("123")
    }
}

def get_fake_db():
    return {
        "admin": {
            "username": "admin",
            "hashed_password": pwd_context.hash("123")
        }
    }

class Token(BaseModel):
    access_token: str
    token_type: str


# ---- 密碼驗證 ----
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate_user(username: str, password: str):
    db: dict =  get_fake_db()
    user = db.get(username)
    if not user:
        return None
    if not verify_password(password, user['hashed_password']):
        return None
    return user

# ---- 建立 JWT ----
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)

# ---- 解析 JWT ----
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Invalid authentication",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    
    except JWSError:
        raise credentials_exception
    
    return username

# ---- login ----
@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    token = create_access_token({"sub": user["username"]},
                                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {"access_token": token, "token_type": "bearer"}

# ---- protected API ----
@app.get("/orders")
async def get_orders(username: str = Depends(get_current_user)):
    return {'current_user': username}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("authentication:app", reload=True)
