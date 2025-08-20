from abc import ABC, abstractmethod
from typing import List, Optional

from src.task.domain.entities import Task


class TaskRepository(ABC):

    @abstractmethod
    async def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def delete(self, task_id: str) -> bool:
        pass

    @abstractmethod
    async def exists(self, task_id: str) -> bool:
        pass
