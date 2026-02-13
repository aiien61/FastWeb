from fastapi import FastAPI, Cookie, Header, Response
from typing import Optional

app = FastAPI()

"""
For parameters of Cookie and Header
Try not to use underscore (_) in between variable characters
Use alias to replace underscore with dash (-)
"""
@app.get('/items')
async def update_item(*,
                      response: Response,
                      favor_schema: Optional[str] = Cookie(None, alias="favor-schema"),
                      api_token: Optional[str] = Header(None, alias="api-token")):
    
    result_dict: dict = {
        "favor_schema": favor_schema,
        "api_token": api_token
    }

    response.set_cookie(key="favor-schema", value="dark")
    
    return result_dict

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cookie_header:app", reload=True)