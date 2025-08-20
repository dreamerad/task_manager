import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.task.domain.exeptions.tasks_exeptions import TaskStatusTransitionError, TaskValidationError


class TaskStatus(Enum):
    CREATED = "создано"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.title or not self.title.strip():
            raise TaskValidationError("Название задачи не может быть пустым")

        if len(self.title.strip()) > 200:
            raise TaskValidationError("Название задачи не может превышать 200 символов")

        if len(self.description) > 1000:
            raise TaskValidationError("Описание задачи не может превышать 1000 символов")

    @classmethod
    def create(cls, title: str, description: str) -> 'Task':
        if not title or not title.strip():
            raise ValueError("Название задачи обязательно")

        now = datetime.utcnow()
        task_id = str(uuid.uuid4())

        return cls(
            id=task_id,
            title=title.strip(),
            description=description.strip(),
            status=TaskStatus.CREATED,
            created_at=now,
            updated_at=now
        )

    def update_title(self, new_title: str) -> 'Task':
        if not new_title or not new_title.strip():
            raise ValueError("Название задачи не может быть пустым")

        return Task(
            id=self.id,
            title=new_title.strip(),
            description=self.description,
            status=self.status,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def update_description(self, new_description: str) -> 'Task':
        return Task(
            id=self.id,
            title=self.title,
            description=new_description.strip(),
            status=self.status,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def change_status(self, new_status: TaskStatus) -> 'Task':
        if not isinstance(new_status, TaskStatus):
            raise ValueError("Неверный статус задачи")

        return Task(
            id=self.id,
            title=self.title,
            description=self.description,
            status=new_status,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    def can_be_deleted(self) -> bool:
        return True

    def get_status_display(self) -> str:
        return self.status.value

    def validate_transition_to(self, new_status: TaskStatus) -> bool:
        transitions = {
            TaskStatus.CREATED: [TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED],
            TaskStatus.IN_PROGRESS: [TaskStatus.COMPLETED, TaskStatus.CREATED],
            TaskStatus.COMPLETED: [TaskStatus.IN_PROGRESS]
        }

        allowed_statuses = transitions.get(self.status, [])
        is_valid = new_status in allowed_statuses or new_status == self.status

        if not is_valid:
            raise TaskStatusTransitionError(self.status.value, new_status.value)

        return True

    def __str__(self) -> str:
        return f"Task(id={self.id[:8]}..., title='{self.title}', status={self.status.value})"
