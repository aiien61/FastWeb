from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/header/{name}/{value}")
def header(name: str, value: str, response: Response):
    response.headers[name] = value
    return "good"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("header_response:app", reload=True)
