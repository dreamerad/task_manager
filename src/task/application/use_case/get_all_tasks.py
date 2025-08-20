import logging
from typing import List

from src.task.application.interface.task_repository import TaskRepository
from src.task.domain.entities import Task

logger = logging.getLogger(__name__)


class GetAllTasksUseCase:

    def __init__(self, task_repository: TaskRepository):
        self._repository = task_repository

    async def execute(self) -> List[Task]:
        tasks = await self._repository.get_all()
        return tasks
