from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Task


class TaskRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Создание задачи"""
        pass

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Получение задачи по ID"""
        pass

    @abstractmethod
    async def get_all(self) -> List[Task]:
        """Получение всех задач"""
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Обновление задачи"""
        pass

    @abstractmethod
    async def delete(self, task_id: str) -> bool:
        """Удаление задачи"""
        pass
