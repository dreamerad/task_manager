import logging

from src.task.application.interface.task_repository import TaskRepository
from src.task.domain.exeptions.tasks_exeptions import TaskNotFoundError, TaskBusinessRuleViolationError

logger = logging.getLogger(__name__)


class DeleteTaskUseCase:

    def __init__(self, task_repository: TaskRepository):
        self._repository = task_repository

    async def execute(self, task_id: str) -> bool:

        task = await self._repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(task_id)

        if not task.can_be_deleted():
            raise TaskBusinessRuleViolationError(f"Задача с ID {task_id} не может быть удалена")

        deleted = await self._repository.delete(task_id)

        if not deleted:
            raise TaskBusinessRuleViolationError(f"Не удалось удалить задачу с ID {task_id}")
        return deleted
