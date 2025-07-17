from fastapi import FastAPI, Body, Header, Response

app = FastAPI()

@app.get("/hi/{who}")
def hi(who):
    return f"Hi? {who}?"

@app.get("/hello")
def hello(who):
    return f"Hello? {who}?"

@app.post("/hey")
def hey(who: str = Body(embed=True)):
    return f"Hey? {who}?"

@app.post("/greet")
def greet(who: str = Header()):
    return f"Hello? {who}?"

@app.post("/agent")
def get_agent(user_agent: str = Header()):
    return user_agent

@app.get("/happy")
def happy(status_code=200):
    return ":)"

@app.get("/header/{name}/{value}")
def header(name: str, value: str, response: Response):
    response.headers[name] = value
    return "normal body"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("hello:app", reload=True)
