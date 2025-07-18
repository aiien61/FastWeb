from model import Creature
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/creature")
def get_all() -> list[Creature]:
    from data import get_creatures
    return get_creatures()

if __name__ == "__main__":
    uvicorn.run("web:app", reload=True)