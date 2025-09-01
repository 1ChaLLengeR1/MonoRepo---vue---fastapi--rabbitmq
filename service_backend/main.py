from fastapi import FastAPI
from contextlib import asynccontextmanager
from messaging.consumer import start_consumer_thread

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_consumer_thread()
    print("RabbitMQ consumer started")
    yield
    # Shutdown
    print("Application shutting down")



# Tworzymy aplikację FastAPI
app = FastAPI(lifespan=lifespan)

# Prosty endpoint GET /hello
@app.get("/hello")
def hello_world():
    return {"message": "Hello World main_service"}