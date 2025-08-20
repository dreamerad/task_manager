from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.config import get_async_session
from src.task.application.interface.task_repository import TaskRepository
from src.task.infrastructure.db.repository import DatabaseTaskRepository


def get_task_repository(session: AsyncSession = Depends(get_async_session)) -> TaskRepository:
    return DatabaseTaskRepository(session)


TaskRepositoryDepend = Annotated[TaskRepository, Depends(get_task_repository)]
