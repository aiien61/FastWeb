from fastapi import FastAPI, Path
import uvicorn

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., title="User ID", ge=1, le=1000)):
    return {"user info": f"This is the user {user_id}"}

@app.get("/books/{book_name}")
async def get_book(book_name: str = Path(..., title="Book Name", min_length=3, max_length=20)):
    return {"book info": f"This is a book {book_name}"}

@app.get("/citizen/{citizen_id}")
async def get_citizen(citizen_id: str = Path(..., title="Citizen ID", regex="^[A-Z][12]00[0-9]{7}$")):
    return {"citizen info": f"This is a citizen {citizen_id}"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)