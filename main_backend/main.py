from fastapi import FastAPI

# Tworzymy aplikację FastAPI
app = FastAPI()

# Prosty endpoint GET /hello
@app.get("/hello")
def hello_world():
    return {"message": "Hello World main_backend"}