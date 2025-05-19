from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi import FastAPI, Path, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .dependecies import current_user, fastapi_users
from app.auth.auth import auth_backend
from app.helpers.helpers import to_start, to_shutdown
from app.schemas import UserOut, UserRead, UserCreate
from .order_routes import order_router

@asynccontextmanager
async def lifespan_func(app: FastAPI):
   await to_start()
   print("База готова")
   yield
   await to_shutdown()
   print("База очищена")

app = FastAPI(lifespan=lifespan_func)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate),
    tags=["me"],
)

app.include_router(
    order_router,
    tags=['orders']
)