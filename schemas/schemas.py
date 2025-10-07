from pydantic import BaseModel, Field
from typing import Annotated, Literal
from models.models import Status


class TaskAddDTO(BaseModel):
    model_config = {
        "extra": "forbid"
        }
    
    name: Annotated[str, Field()]
    description: Annotated[str | None, Field(default=None)]
    status: Annotated[Status, Field()]
    priority: Annotated[int, Field(gt=0, le=3)]



class TaskDTO(TaskAddDTO):
      id: int


class TaskUpdateDTO(TaskAddDTO):
     ...


class UsersAddDTO(BaseModel):
    model_config = {
        "extra": "forbid"
        }
    username: Annotated[str, Field()]
    password: Annotated[str | None, Field()]
    

class UsersDTO(UsersAddDTO):
    id: int
    tasks: Annotated[list["TaskDTO"], Field()]
