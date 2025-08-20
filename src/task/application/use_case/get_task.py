import logging

from src.task.application.interface.task_repository import TaskRepository
from src.task.domain.entities import Task
from src.task.domain.exeptions.tasks_exeptions import TaskNotFoundError

logger = logging.getLogger(__name__)


class GetTaskUseCase:

    def __init__(self, task_repository: TaskRepository):
        self._repository = task_repository

    async def execute(self, task_id: str) -> Task:
        task = await self._repository.get_by_id(task_id)
        if not task:
            logger.warning(f"Задача не найдена: {task_id}")
            raise TaskNotFoundError(task_id)

        return task
