from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, CheckConstraint
from enum import Enum

class Base(DeclarativeBase):
    ...


class Status(Enum):
    DONE = "DONE"
    PROGRESS = "PROGRESS"
    BLOCKED = "BLOCKED"

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
    status: Mapped[Status | None] = mapped_column(
        nullable=True
        )
    priority: Mapped[int] = mapped_column(
        nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            '0 < priority AND priority <= 3', 
            name='priority_range',
            ),
    )