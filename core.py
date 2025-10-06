from sqlalchemy import select, update, delete, asc, desc, and_, or_
from sqlalchemy.orm import aliased
from models.models import TasksOrm, Status
from database import session_factory
from schemas.schemas import TaskAddDTO, TaskDTO, TaskUpdateDTO 
from deps import SessionDep



class Repository():
    @classmethod
    async def add_one(
        cls, 
        data: TaskAddDTO
    ) -> int:
        async with session_factory() as session:
            task_dict = data.model_dump()
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
        )
        if priority == "asc":
            query = (
                query
                .order_by(asc(TasksOrm.priority))
            )
        else:
            query = (
                query
                .order_by(desc(TasksOrm.priority))
            )

        result = await session.execute(query)
        tasks = result.scalars().all()
        return [TaskDTO.model_validate(task, from_attributes=True) for task in tasks]
    
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
        return [TaskDTO.model_validate(task, from_attributes=True) for task in tasks]




    



    