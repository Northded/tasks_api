from fastapi import APIRouter, Depends
from typing import Annotated
from schemas.schemas import TaskAddDTO, TaskDTO
from core import Repository


router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


@router.post("")
async def add_task(
    task: Annotated[TaskAddDTO, Depends()],
):
    task_id = await Repository.add_one(task)
    return {"ok": True, "task_ID": task_id}


@router.get("", response_model=list[TaskDTO])
async def get_tasks():
    tasks = await Repository.find_all()
    return {"tasks": tasks} 
