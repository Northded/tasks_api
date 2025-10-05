from sqlalchemy import select, update, delete
from sqlalchemy.orm import aliased
from models.models import TasksOrm, Status
from database import session_factory
from schemas.schemas import TaskAddDTO, TaskDTO, TaskUpdateDTO 
from deps import SessionDep



class Repository():
    @classmethod
    async def add_one(cls, data: TaskAddDTO) -> int:
        async with session_factory() as session:
            task_dict = data.model_dump()
            task = TasksOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[TaskDTO]:
        async with session_factory() as session:
            query = (
                select(TasksOrm)
            )
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [TaskDTO.model_validate(col, from_attributes=True) for col in task_models]
            return task_schemas
        
    @classmethod 
    async def update_one(cls, id: int, session: SessionDep, data: TaskUpdateDTO) -> TaskDTO:
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
    async def delete_task(cls, id: int, session: SessionDep):
        query = (
            delete(TasksOrm)
            .where(TasksOrm.id == id)
        )
        await session.execute(query)
        await session.commit()
    
    @classmethod
    async def find_by_status_filter(cls, status: str | None, session: SessionDep):
        query = (
            select(TasksOrm)
        )
        if status:
            query = (
                query
                .where(TasksOrm.status == status)
            )

        result = await session.execute(query)
        tasks = result.scalars().all()
        return [TaskDTO.model_validate(task, from_attributes=True) for task in tasks]

    



    