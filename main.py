from fastapi import FastAPI, Query
from database import create_db
from contextlib import asynccontextmanager
from routes.routes import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    print("ON")
    yield
    print("OFF")


app = FastAPI(lifespan=lifespan)
app.include_router(router=tasks_router)


if __name__ == "__main__":
    ... 