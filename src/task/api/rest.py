import logging
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.responses import Response

from .dependencies import TaskRepositoryDepend
from .models import (
    TaskCreateRequest, TaskUpdateRequest, TaskResponse,
    TaskListResponse, ErrorResponse
)
from ..application.use_case.create_task import CreateTaskUseCase
from ..application.use_case.delete_task import DeleteTaskUseCase
from ..application.use_case.get_all_tasks import GetAllTasksUseCase
from ..application.use_case.get_task import GetTaskUseCase
from ..application.use_case.update_task import UpdateTaskUseCase

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание новой задачи",
    description="Создает новую задачу с указанным названием и описанием",
    responses={
        201: {"description": "Задача успешно создана"},
        400: {"model": ErrorResponse, "description": "Некорректные данные"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"}
    }
)
async def create_task(
        task_data: TaskCreateRequest,
        task_repository: TaskRepositoryDepend
) -> TaskResponse:
    use_case = CreateTaskUseCase(task_repository)
    task = await use_case.execute(
        title=task_data.title,
        description=task_data.description
    )
    return TaskResponse.from_domain(task)


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Получение списка задач",
    description="Возвращает список всех задач с возможностью фильтрации по статусу",
    responses={
        200: {"description": "Список задач успешно получен"},
        400: {"model": ErrorResponse, "description": "Некорректные параметры фильтрации"}
    }
)
async def get_tasks(
        task_repository: TaskRepositoryDepend,
) -> TaskListResponse:
    use_case = GetAllTasksUseCase(task_repository)
    tasks = await use_case.execute()

    return TaskListResponse.from_domain_list(tasks)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получение задачи по ID",
    description="Возвращает задачу с указанным идентификатором",
    responses={
        200: {"description": "Задача найдена"},
        404: {"model": ErrorResponse, "description": "Задача не найдена"},
        400: {"model": ErrorResponse, "description": "Некорректный ID задачи"}
    }
)
async def get_task(
        task_id: UUID,
        task_repository: TaskRepositoryDepend
) -> TaskResponse:
    use_case = GetTaskUseCase(task_repository)
    task = await use_case.execute(str(task_id))
    return TaskResponse.from_domain(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Обновление задачи",
    description="Обновляет существующую задачу",
    responses={
        200: {"description": "Задача успешно обновлена"},
        404: {"model": ErrorResponse, "description": "Задача не найдена"},
        400: {"model": ErrorResponse, "description": "Некорректные данные для обновления"}
    }
)
async def update_task(
        task_id: UUID,
        task_data: TaskUpdateRequest,
        task_repository: TaskRepositoryDepend
) -> TaskResponse:
    use_case = UpdateTaskUseCase(task_repository)
    task = await use_case.execute(
        task_id=str(task_id),
        title=task_data.title,
        description=task_data.description,
        status=task_data.status
    )
    return TaskResponse.from_domain(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление задачи",
    description="Удаляет задачу с указанным идентификатором",
    responses={
        204: {"description": "Задача успешно удалена"},
        404: {"model": ErrorResponse, "description": "Задача не найдена"},
        400: {"model": ErrorResponse, "description": "Задача не может быть удалена"}
    }
)
async def delete_task(
        task_id: UUID,
        task_repository: TaskRepositoryDepend
):
    use_case = DeleteTaskUseCase(task_repository)
    await use_case.execute(str(task_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
