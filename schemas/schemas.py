from pydantic import BaseModel, Field
from typing import Annotated, Literal
from models.models import Status


class UserDTO(BaseModel):
    id: int
    username: Annotated[str, Field()]


class UserRegisterDTO(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: Annotated[str, Field(min_length=6)]
    model_config = {"extra": "forbid"}
    

class TaskBaseDTO(BaseModel):
    name: Annotated[str, Field()]
    description: Annotated[str | None, Field(default=None)]
    status: Annotated[Status, Field()]
    priority: Annotated[int, Field(gt=0, le=3)]


class TaskAddDTO(TaskBaseDTO):
    username: Annotated[str, Field()]  # Для создания задачи


class TaskDTO(TaskBaseDTO):
    id: int
    user: UserDTO  # Для возврата задачи с информацией о пользователе


class TaskUpdateDTO(BaseModel):
    name: Annotated[str | None, Field(default=None)]
    description: Annotated[str | None, Field(default=None)]
    status: Annotated[Status | None, Field(default=None)]
    priority: Annotated[int | None, Field(gt=0, le=3, default=None)]