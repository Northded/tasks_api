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


class TaskDTO(TaskAddDTO):
      id: int


class TaskUpdateDTO(TaskAddDTO):
     ...