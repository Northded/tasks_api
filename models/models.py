from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    ...


class TasksOrm(Base):

    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(
        primary_key=True
        )
    name: Mapped[str] = mapped_column(
        String(20),
        nullable=False, 
        )
    description: Mapped[str | None] 