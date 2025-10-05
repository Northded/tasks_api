from fastapi import APIRouter, Depends
from typing import Annotated
from schemas.schemas import TaskAddDTO, TaskDTO, TaskUpdateDTO
from core import Repository
from deps import SessionDep


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


@router.get("")
async def get_tasks():
    tasks = await Repository.find_all()
    return {"tasks": tasks} 


@router.put("")
async def update_task(
    id: int,
    data: TaskUpdateDTO,
    session: SessionDep
):
    tasks = await Repository.update_one(data=data, id=id, session=session)
    return {"updated": tasks}
 