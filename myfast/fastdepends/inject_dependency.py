from fastapi import FastAPI, Depends, params
import uvicorn

app = FastAPI()

def user_dep(name: str = params, password: str = params):
    return {"name": name, "valid": True}

@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    return user

if __name__ == "__main__":
    uvicorn.run("inject_dependency:app", reload=True)
