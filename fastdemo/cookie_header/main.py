from fastapi import FastAPI, Cookie, Header, Response
from typing import Optional
import uvicorn 

app = FastAPI()

@app.put("/settings")
async def update_settings(*,
                          response: Response,
                          favorite_schema: Optional[str] = Cookie(None, alias="favorite-schema"),
                          api_token: Optional[str] = Header(None, alias="api-token")):
    
    result = {
        "favorite_schema": favorite_schema,
        "api_token": api_token
    }

    response.set_cookie(key="favorite-schema", value="light")

    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)