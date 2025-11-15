from fastapi import FastAPI
from app.api import routes_user

app = FastAPI(title="FastAPI ORM Project")

# Include your user routes
app.include_router(routes_user.router)

# Optional root route


@app.get("/")
async def root():
    return {"message": "FastAPI ORM Project is running!"}
