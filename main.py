from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

app = FastAPI()
ALLOWED_ORIGIN = "https://dash-w1czue.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/stats")
def stats(values: str = Query(...)):
    nums = [int(x) for x in values.split(",")]
    return {
        "email": "your-email@example.com",
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums) if nums else 0,
    }
