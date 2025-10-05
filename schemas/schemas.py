from pydantic import BaseModel, Field
from typing import Annotated, Literal


class TaskAddDTO(BaseModel):
    model_config = {
        "extra": "forbid"
        }
    
    name: Annotated[str, Field()]
    description: Annotated[str | None, Field(default=None)]
    status: Literal["DONE", "IN_PROGRESS", "BLOCKED"]


class TaskDTO(TaskAddDTO):
      id: int


class TaskUpdateDTO(TaskAddDTO):
     ...