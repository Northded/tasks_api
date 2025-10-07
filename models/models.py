from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint, ForeignKey
from passlib.context import CryptContext
from enum import Enum


pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


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
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["UsersOrm"] = relationship(
        back_populates="tasks"
    )

    __table_args__ = (
        CheckConstraint(
            '0 < priority AND priority <= 3', 
            name='priority_range',
            ),
    )


class UsersOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(20)
    )
    hashed_password: Mapped[str]
    tasks: Mapped[list["TasksOrm"]] = relationship(
        back_populates="user"
    )
 

    async def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def get_password_hash(cls, password: str):
        truncated_password = password[:72]
        return pwd_context.hash(truncated_password) 
