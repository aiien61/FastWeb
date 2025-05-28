from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import jwt 
import uvicorn

app = FastAPI()

SECURITY_KEY: str = "THIS IS SECURITY KEY"
ALGORITHM = "HS256"
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

class Token(BaseModel):
    access_token: str
    token_type: str


def validate_user(username: str, password: str):
    """Simulate database"""
    if username == "admin" and password == "admin123":
        return username
    return None


def get_current_username(token: str = Depends(oauth2_schema)):
    unauth_exp = HTTPException(status_code=401, detail="Unauthorized")
    try:
        token_data = jwt.decode(token, SECURITY_KEY, ALGORITHM)
        if token_data:
            username = token_data.get("username", None)
            exp = token_data.get("exp", None)

    except Exception as e:
        raise unauth_exp
    
    if not username:
        raise HTTPException(
            status_code=401, detail="Unauthorized: unauthorized user")

    now = datetime.now(timezone.utc).timestamp()
    if now > exp:
        raise HTTPException(status_code=401, detail="Unauthorized: the token has expired")
    
    return username

@app.post("/token")
async def login(login_form: OAuth2PasswordRequestForm = Depends()):
    username = validate_user(login_form.username, login_form.password)
    if not username:
        raise HTTPException(status_code=401, 
                            detail="Incorrect username or password", 
                            headers={"WWW-Authenticate": "Bearer"})
    
    now = datetime.now(timezone.utc)
    token_data = {
        "username": username,
        "iat": int(now.timestamp()), # issued at
        "exp": now + timedelta(seconds=10)
    }
    token = jwt.encode(token_data, SECURITY_KEY, ALGORITHM)
    return Token(access_token=token, token_type="bearer")


@app.get("/items")
async def get_item(username: str = Depends(get_current_username)):
    return {"current user": username}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3_000, reload=True)