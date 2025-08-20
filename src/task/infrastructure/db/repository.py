import logging
import uuid
from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Task as DBTask
from ...application.interface.task_repository import TaskRepository
from ...domain.entities import Task, TaskStatus

logger = logging.getLogger(__name__)


class DatabaseTaskRepository(TaskRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self._logger = logging.getLogger(__name__)

    async def create(self, task: Task) -> Task:
        try:
            db_task = DBTask(
                id=uuid.UUID(task.id) if isinstance(task.id, str) else task.id,
                title=task.title,
                description=task.description,
                status=task.status.value,
                created_at=task.created_at,
                updated_at=task.updated_at
            )

            self._session.add(db_task)
            await self._session.commit()
            await self._session.refresh(db_task)

            self._logger.info(f"Создана задача в БД: {task.id} - '{task.title}'")
            return self._db_to_domain(db_task)

        except Exception as e:
            await self._session.rollback()
            self._logger.error(f"Ошибка создания задачи в БД {task.id}: {e}")
            raise

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        try:
            uid = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
            stmt = select(DBTask).where(DBTask.id == uid)
            result = await self._session.execute(stmt)
            db_task = result.scalar_one_or_none()

            if db_task:
                self._logger.debug(f"Найдена задача в БД: {task_id}")
                return self._db_to_domain(db_task)

            self._logger.debug(f"Задача не найдена в БД: {task_id}")
            return None

        except Exception as e:
            self._logger.error(f"Ошибка получения задачи из БД {task_id}: {e}")
            raise

    async def get_all(self) -> List[Task]:
        try:
            stmt = select(DBTask).order_by(DBTask.created_at.desc())
            result = await self._session.execute(stmt)
            db_tasks = result.scalars().all()

            tasks = [self._db_to_domain(db_task) for db_task in db_tasks]
            self._logger.debug(f"Получено {len(tasks)} задач из БД")
            return tasks

        except Exception as e:
            self._logger.error(f"Ошибка получения всех задач из БД: {e}")
            raise

    async def update(self, task: Task) -> Task:
        try:
            uid = uuid.UUID(task.id) if isinstance(task.id, str) else task.id
            stmt = update(DBTask).where(DBTask.id == uid).values(
                title=task.title,
                description=task.description,
                status=task.status.value,
                updated_at=task.updated_at
            )

            result = await self._session.execute(stmt)

            if result.rowcount == 0:
                raise ValueError(f"Задача с ID {task.id} не найдена для обновления")

            await self._session.commit()

            updated_task = await self.get_by_id(task.id)
            if not updated_task:
                raise ValueError(f"Не удалось получить обновленную задачу {task.id}")

            self._logger.info(f"Обновлена задача в БД: {task.id} - '{task.title}'")
            return updated_task

        except Exception as e:
            await self._session.rollback()
            self._logger.error(f"Ошибка обновления задачи в БД {task.id}: {e}")
            raise

    async def delete(self, task_id: str) -> bool:
        try:
            uid = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
            stmt = delete(DBTask).where(DBTask.id == uid)
            result = await self._session.execute(stmt)
            await self._session.commit()

            success = result.rowcount > 0
            if success:
                self._logger.info(f"Удалена задача из БД: {task_id}")
            else:
                self._logger.warning(f"Попытка удалить несуществующую задачу: {task_id}")

            return success

        except Exception as e:
            await self._session.rollback()
            self._logger.error(f"Ошибка удаления задачи из БД {task_id}: {e}")
            raise

    async def exists(self, task_id: str) -> bool:
        try:
            uid = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
            stmt = select(DBTask.id).where(DBTask.id == uid)
            result = await self._session.execute(stmt)
            exists = result.scalar_one_or_none() is not None

            self._logger.debug(f"Проверка существования задачи {task_id}: {exists}")
            return exists

        except Exception as e:
            self._logger.error(f"Ошибка проверки существования задачи {task_id}: {e}")
            return False

    async def find_by_numeric_id(self, numeric_id: int) -> Optional[Task]:
        return None

    async def get_by_status(self, status: str) -> List[Task]:
        try:
            stmt = select(DBTask).where(DBTask.status == status).order_by(DBTask.created_at.desc())
            result = await self._session.execute(stmt)
            db_tasks = result.scalars().all()

            tasks = [self._db_to_domain(db_task) for db_task in db_tasks]
            self._logger.debug(f"Получено {len(tasks)} задач со статусом '{status}' из БД")
            return tasks

        except Exception as e:
            self._logger.error(f"Ошибка получения задач по статусу '{status}' из БД: {e}")
            raise

    def _db_to_domain(self, db_task: DBTask) -> Task:
        try:
            return Task(
                id=str(db_task.id),
                title=db_task.title,
                description=db_task.description,
                status=TaskStatus(db_task.status),
                created_at=db_task.created_at,
                updated_at=db_task.updated_at
            )
        except Exception as e:
            self._logger.error(f"Ошибка конвертации DBTask в Task (ID: {db_task.id}): {e}")
            raise

    def _domain_to_db(self, task: Task) -> DBTask:
        try:
            return DBTask(
                id=uuid.UUID(task.id) if isinstance(task.id, str) else task.id,
                title=task.title,
                description=task.description,
                status=task.status.value,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
        except Exception as e:
            self._logger.error(f"Ошибка конвертации Task в DBTask (ID: {task.id}): {e}")
            raise

    async def get_count(self) -> int:
        try:
            from sqlalchemy import func
            stmt = select(func.count(DBTask.id))
            result = await self._session.execute(stmt)
            count = result.scalar() or 0

            self._logger.debug(f"Общее количество задач в БД: {count}")
            return count

        except Exception as e:
            self._logger.error(f"Ошибка получения количества задач: {e}")
            return 0

    async def get_statistics(self) -> dict:
        try:
            from sqlalchemy import func

            total_stmt = select(func.count(DBTask.id))
            total_result = await self._session.execute(total_stmt)
            total = total_result.scalar() or 0

            status_stmt = select(DBTask.status, func.count(DBTask.id)).group_by(DBTask.status)
            status_result = await self._session.execute(status_stmt)
            status_counts = dict(status_result.fetchall())

            statistics = {
                "total": total,
                "by_status": status_counts
            }

            self._logger.debug(f"Статистика из БД: {statistics}")
            return statistics

        except Exception as e:
            self._logger.error(f"Ошибка получения статистики из БД: {e}")
            return {"total": 0, "by_status": {}}
