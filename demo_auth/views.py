from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Depends, APIRouter, HTTPException, status
from models.models import UsersOrm
from typing import Annotated
from deps import SessionDep
from core import Repository


router = APIRouter(
    prefix="/auth",
    tags=["Auth_enpoints"]
)


security = HTTPBasic()
SecurityDep = Annotated[HTTPBasicCredentials, Depends(security)]


@router.get("/basic_auth/")
async def basic_auth_credentials(
    credentials: SecurityDep,
    session: SessionDep
):
    username = credentials.username
    password = credentials.password
    data = await Repository.get_username(username=username, session=session)
    if username not in data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password or username",
            headers={"WWW-Authenticate": "Basic"}
        )
    correct_username, correct_password = data
    user = UsersOrm(
        username=correct_username,
        hashed_password=correct_password
    )
    is_correct = await user.verify_password(password)
    if not is_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password or username",
            headers={"WWW-Authenticate": "Basic"}
        )
    return {
        "username": correct_username,
        "status": "Authorized"
    }