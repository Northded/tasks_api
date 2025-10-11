from typing import Annotated
from sqlalchemy import select, update, delete, asc, desc, and_, or_
from sqlalchemy.orm import aliased, selectinload
from models.models import TasksOrm, UsersOrm
from database import session_factory
from schemas.schemas import TaskAddDTO, TaskDTO, TaskUpdateDTO, UserDTO
from deps import SessionDep
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()


class Repository():
    @classmethod
    async def add_one(
        cls, 
        data: TaskAddDTO
    ) -> int:
        async with session_factory() as session:
            query = (
                select(UsersOrm)
                .where(UsersOrm.username == data.username)
            )
            res = await session.execute(query)
            user = res.scalars().first()
            user_id = user.id
            task_dict = data.model_dump(
                exclude={"username"},
            )
            task_dict["user_id"] = user_id
            task = TasksOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id
        
    @classmethod 
    async def update_one(
        cls, 
        id: int, 
        session: SessionDep, 
        data: TaskUpdateDTO
    ) -> TaskDTO:
        query = (
            update(TasksOrm)
            .where(TasksOrm.id == id)
            .values(**data.model_dump())
            .returning(TasksOrm)
        )
        result = await session.execute(query)
        await session.commit()
        row = result.fetchone()
        return TaskDTO.model_validate(row[0], from_attributes=True)
    
    @classmethod
    async def delete_task(
        cls, 
        id: int, 
        session: SessionDep
    ):
        query = (
            delete(TasksOrm)
            .where(TasksOrm.id == id)
        )
        await session.execute(query)
        await session.commit()
    
    @classmethod
    async def find_by_priority_sorted(
        cls, 
        session: SessionDep, 
        priority: str = 'asc'
    ) -> list[TaskDTO]:
        query = (
            select(TasksOrm)
            .options(selectinload(TasksOrm.user))
        )
        if priority == "asc":
            query = (
                query.order_by(asc(TasksOrm.priority))
            )
        else:
            query = (
                query.order_by(desc(TasksOrm.priority))
            )

        result = await session.execute(query)
        tasks = result.scalars().all()
        
        task_dtos = []
        for task in tasks:
            user_dto = UserDTO(id=task.user.id, username=task.user.username)
            task_dto = TaskDTO(
                id=task.id,
                name=task.name,
                description=task.description,
                status=task.status,
                priority=task.priority,
                user=user_dto
            )
            task_dtos.append(task_dto)
        
        return task_dtos
    
    @classmethod
    async def find_tasks_with_filters(
        cls,
        session: SessionDep,
        keyword: str | None = None,
        status: str | None = None,
        priority: int | None = None,
    ):
        query = (
            select(TasksOrm)
        )

        conditions = []

        if keyword:

            keyword_like = f"%{keyword}%"

            conditions.append(
                or_(
                    TasksOrm.description.ilike(keyword_like),
                    TasksOrm.name.ilike(keyword_like)
                )
            )
        if status:
            conditions.append(
                TasksOrm.status == status
            )
        if priority:
            conditions.append(
                TasksOrm.priority == priority
            )
        if conditions:
            query = (
                query.where(and_(*conditions))
            )
        result = await session.execute(query)
        tasks = result.scalars().all()
        task_dtos = []
        for task in tasks:
            user_dto = UserDTO(id=task.user.id, username=task.user.username)
            task_dto = TaskDTO(
                id=task.id,
                name=task.name,
                description=task.description,
                status=task.status,
                priority=task.priority,
                user=user_dto
            )
            task_dtos.append(task_dto)
        return task_dtos
    
    @classmethod
    async def register_user(
        cls, 
        session: SessionDep,
        username: str,     
        password: str,     
    ):
        query = (
            select(UsersOrm)
            .where(UsersOrm.username == username)
        )
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise ValueError(f"User with username - {username} is existed")
        hashed_pass = UsersOrm.get_password_hash(password=password)
        user = UsersOrm(username=username, hashed_password=hashed_pass)
        session.add(user)
        await session.flush()
        await session.refresh(user)
        await session.commit()

    @classmethod
    async def get_username(
        cls, 
        username: str, 
        session: SessionDep
    ):
        query = (
            select(UsersOrm.username, UsersOrm.hashed_password)
            .where(UsersOrm.username == username)
        )
        user = await session.execute(query)
        result = user.one_or_none()
        if not result:
            raise ValueError(f"User {username} is not existed")
        return result