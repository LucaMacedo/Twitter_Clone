from fastapi import FastAPI
import uvicorn

app = FastAPI()

# decorator to define a GET endpoint.
# Test the application at http://127.0.0.1:4444/docs
@app.get("/") # root point
async def index(): # no asyncio is needed, but it is a good practice to use async def for better performance
    return {"message": "hello world"}

if __name__ == "__main__": # start application when it's main module. Otherwise you have to use the terminal to start the app.
    uvicorn.run(app, host="127.0.0.1", port=4444)

