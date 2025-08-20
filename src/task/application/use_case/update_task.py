import logging
from typing import Optional

from src.task.application.interface.task_repository import TaskRepository
from src.task.domain.entities import Task, TaskStatus
from src.task.domain.exeptions.tasks_exeptions import TaskNotFoundError, TaskValidationError, TaskStatusTransitionError

logger = logging.getLogger(__name__)


class UpdateTaskUseCase:

    def __init__(self, task_repository: TaskRepository):
        self._repository = task_repository

    async def execute(
            self,
            task_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            status: Optional[str] = None
    ) -> Task:

        existing_task = await self._repository.get_by_id(task_id)
        if not existing_task:
            logger.warning(f"Задача не найдена для обновления: {task_id}")
            raise TaskNotFoundError(task_id)

        updated_task = existing_task

        try:
            if title is not None:
                updated_task = updated_task.update_title(title)

            if description is not None:
                updated_task = updated_task.update_description(description)

            if status is not None:
                try:
                    new_status = TaskStatus(status)

                    existing_task.validate_transition_to(new_status)

                    updated_task = updated_task.change_status(new_status)

                except ValueError as e:
                    if "is not a valid" in str(e):
                        valid_statuses = [s.value for s in TaskStatus]
                        raise TaskValidationError(f"Неверный статус: {status}. Допустимые: {valid_statuses}")
                    raise
                except TaskStatusTransitionError:
                    raise

            saved_task = await self._repository.update(updated_task)

            return saved_task

        except (TaskValidationError, TaskStatusTransitionError):
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при обновлении задачи {task_id}: {e}")
            raise TaskValidationError(f"Не удалось обновить задачу: {str(e)}")
