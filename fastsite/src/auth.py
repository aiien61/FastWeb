import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

secret_user: str = "YOUR-USER-NAME"
secret_password: str = "YOUR-PASSWORD"

basic = HTTPBasic()

@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if (creds.username == secret_user) and (creds.password == secret_password):
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(status_code=401, detail="You're a wrong guy!")

if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)
