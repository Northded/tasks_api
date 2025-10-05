from fastapi import APIRouter, Depends
from typing import Annotated
from schemas.schemas import TaskAddDTO, TaskDTO, TaskUpdateDTO
from core import Repository
from deps import SessionDep
from models.models import Status


router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


@router.post("")
async def add_task(
    task: TaskAddDTO,
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
    session: SessionDep,
):
    tasks = await Repository.update_one(data=data, id=id, session=session)
    return {"updated": tasks}


@router.delete("")
async def del_task(
    id: int,
    session: SessionDep,
):
    await Repository.delete_task(id=id, session=session)
    return {"ok": True}


@router.get("/filtred/")
async def get_filtred_by_status_tasks(
    session: SessionDep,
    status: Status | None = None, 
    ):
    tasks = await Repository.find_by_status_filter(status=status, session=session)
    return {"tasks": tasks}