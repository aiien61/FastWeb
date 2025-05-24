from fastapi import FastAPI, Body, Header

app = FastAPI()

@app.get("/hi/{who}")
def hi(who):
    return f"hi {who}"

@app.get("/hello")
def hello(who):
    return f"Hello {who}"

@app.post("/hey")
def hey(who: str = Body(embed=True)):
    return f"Hey {who}"

@app.post("/yo")
def yo(who: str = Header()):
    return f"Yo {who}"

@app.post("/agent")
def get_agent(user_agent: str = Header()):
    return user_agent

@app.get("/happy")
def happy(status_code=200):
    return ":)"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)