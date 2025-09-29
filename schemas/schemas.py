from pydantic import BaseModel, Field
from typing import Annotated


class TaskAddDTO(BaseModel):
    model_config = {
        "extra": "forbid"
        }
    
    name: Annotated[str, Field()]
    description: Annotated[str | None, Field(default=None)]


class TaskDTO(TaskAddDTO):
      id: int