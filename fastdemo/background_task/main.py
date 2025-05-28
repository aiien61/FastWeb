from fastapi import FastAPI, BackgroundTasks
import uvicorn
import time

app = FastAPI()

def send_message(msg: str):
    print(f'Start sending "{msg}"')
    time.sleep(10)
    print(f'Complete sending "{msg}"')
    return True

@app.post("/notify")
async def send_notification(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message, msg=message)
    return {"message": f"sending notification {message} in background"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3_000, reload=True)