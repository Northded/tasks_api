from fastapi import APIRouter, Depends
from typing import Literal
from schemas.schemas import TaskAddDTO, TaskUpdateDTO, UserRegisterDTO
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
async def get_tasks(
    session: SessionDep,
    priority: Literal["asc", "desc"] = None
):
    if not priority:
        tasks = await Repository.find_all()
        return {"tasks": tasks} 
    tasks = await Repository.find_by_priority_sorted(session=session, priority=priority)
    return {"tasks": tasks} 

@router.put("/{id}")
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
    keyword: str | None = None,
    priority: int | None = None,
):
    tasks = await Repository.find_tasks_with_filters(
        status=status, 
        session=session, 
        priority=priority,
        keyword=keyword,
    )
    return {"tasks": tasks}

@router.post("/registration/")
async def add_new_user(
    session: SessionDep,
    data: UserRegisterDTO,
):
    user = await Repository.register_user(
        session=session,
        username=data.username,
        password=data.password,
    )
    return {"ok": "User added"}