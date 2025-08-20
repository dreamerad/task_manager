from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator

from src.task.domain.entities import TaskStatus
from src.task.infrastructure.db.models import Task


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    description: str = Field("", max_length=1000, description="Описание задачи")

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Название задачи не может быть пустым')
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        return v.strip()

    class Config:
        schema_extra = {
            "example": {
                "title": "Изучить FastAPI",
                "description": "Изучить основы FastAPI для создания REST API"
            }
        }


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Новое название задачи")
    description: Optional[str] = Field(None, max_length=1000, description="Новое описание задачи")
    status: Optional[str] = Field(None, description="Новый статус задачи")

    @validator('title')
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Название задачи не может быть пустым')
        return v.strip() if v else v

    @validator('description')
    def validate_description(cls, v):
        return v.strip() if v else v

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = [status.value for status in TaskStatus]
            if v not in valid_statuses:
                raise ValueError(f'Неверный статус. Допустимые: {valid_statuses}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "title": "Изучить FastAPI",
                "description": "Изучить основы FastAPI и создать тестовое приложение",
                "status": "в работе"
            }
        }


class TaskResponse(BaseModel):
    id: str = Field(..., description="Уникальный идентификатор задачи")
    title: str = Field(..., description="Название задачи")
    description: str = Field(..., description="Описание задачи")
    status: str = Field(..., description="Статус задачи")
    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    @classmethod
    def from_domain(cls, task: Task) -> 'TaskResponse':
        return cls(
            id=str(task.id),
            title=task.title,
            description=task.description,
            status=task.status.value,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Изучить FastAPI",
                "description": "Изучить основы FastAPI для создания REST API",
                "status": "создано",
                "created_at": "2023-12-01T10:00:00Z",
                "updated_at": "2023-12-01T10:00:00Z"
            }
        }


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse] = Field(..., description="Список задач")
    total: int = Field(..., description="Общее количество задач")

    @classmethod
    def from_domain_list(cls, tasks: List[Task]) -> 'TaskListResponse':
        return cls(
            tasks=[TaskResponse.from_domain(task) for task in tasks],
            total=len(tasks)
        )

    class Config:
        schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Изучить FastAPI",
                        "description": "Изучить основы FastAPI для создания REST API",
                        "status": "создано",
                        "created_at": "2023-12-01T10:00:00Z",
                        "updated_at": "2023-12-01T10:00:00Z"
                    }
                ],
                "total": 1
            }
        }


class TaskStatusInfo(BaseModel):
    status: str = Field(..., description="Статус задачи")
    display_name: str = Field(..., description="Отображаемое название статуса")
    description: str = Field(..., description="Описание статуса")

    class Config:
        schema_extra = {
            "example": {
                "status": "создано",
                "display_name": "Создано",
                "description": "Задача создана и готова к выполнению"
            }
        }


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Сообщение об ошибке")
    error_code: Optional[str] = Field(None, description="Код ошибки")
    details: Optional[dict] = Field(None, description="Дополнительные детали ошибки")

    class Config:
        schema_extra = {
            "example": {
                "error": "Задача не найдена",
                "error_code": "TASK_NOT_FOUND",
                "details": {"task_id": "123e4567-e89b-12d3-a456-426614174000"}
            }
        }


class SuccessResponse(BaseModel):
    message: str = Field(..., description="Сообщение об успешной операции")
    success: bool = Field(True, description="Флаг успешности")

    class Config:
        schema_extra = {
            "example": {
                "message": "Задача успешно удалена",
                "success": True
            }
        }