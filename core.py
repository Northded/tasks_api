from sqlalchemy import select
from sqlalchemy.orm import aliased
from models.models import TasksOrm
from database import session_factory
from schemas.schemas import TaskAddDTO, TaskDTO 


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

    