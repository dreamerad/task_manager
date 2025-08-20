import logging

from src.task.application.interface.task_repository import TaskRepository
from src.task.domain.entities import Task
from src.task.domain.exeptions.tasks_exeptions import TaskValidationError

logger = logging.getLogger(__name__)


class CreateTaskUseCase:

    def __init__(self, task_repository: TaskRepository):
        self._repository = task_repository

    async def execute(self, title: str, description: str = "") -> Task:

        try:
            task = Task.create(title=title, description=description)
            created_task = await self._repository.create(task)

            return created_task

        except TaskValidationError:
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при создании задачи: {e}")
            raise TaskValidationError(f"Не удалось создать задачу: {str(e)}")
