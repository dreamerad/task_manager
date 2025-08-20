import logging

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.task.domain.exeptions.tasks_exeptions import (
    TaskAlreadyExistsError,
    TaskBusinessRuleViolationError,
    TaskDomainError,
    TaskNotFoundError,
    TaskStatusTransitionError,
    TaskValidationError,
)

logger = logging.getLogger(__name__)


async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    logger.warning(f"Task not found: {exc.task_id}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "task_id": exc.task_id
        }
    )


async def task_validation_handler(request: Request, exc: TaskValidationError) -> JSONResponse:
    logger.warning(f"Task validation error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": exc.message,
            "error_code": exc.error_code
        }
    )


async def task_status_transition_handler(request: Request, exc: TaskStatusTransitionError) -> JSONResponse:
    logger.warning(f"Invalid status transition: {exc.from_status} -> {exc.to_status}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "from_status": exc.from_status,
            "to_status": exc.to_status
        }
    )


async def task_already_exists_handler(request: Request, exc: TaskAlreadyExistsError) -> JSONResponse:
    logger.warning(f"Task already exists: {exc.task_id}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "task_id": exc.task_id
        }
    )


async def task_business_rule_handler(request: Request, exc: TaskBusinessRuleViolationError) -> JSONResponse:
    logger.warning(f"Business rule violation: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": exc.message,
            "error_code": exc.error_code
        }
    )


async def generic_task_domain_handler(request: Request, exc: TaskDomainError) -> JSONResponse:
    logger.error(f"Domain error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": exc.message,
            "error_code": exc.error_code
        }
    )


def _serialize_validation_errors(errors: list) -> list:
    serialized_errors = []
    for error in errors:
        serialized_error = {
            "type": error.get("type", "validation_error"),
            "loc": error.get("loc", []),
            "msg": error.get("msg", "Validation error"),
            "input": str(error.get("input", ""))
        }

        if "ctx" in error and error["ctx"]:
            ctx = error["ctx"]
            if "error" in ctx:
                if isinstance(ctx["error"], ValueError):
                    serialized_error["ctx"] = {"error": str(ctx["error"])}
                else:
                    serialized_error["ctx"] = {"error": str(ctx["error"])}
            else:
                serialized_error["ctx"] = {k: str(v) for k, v in ctx.items()}

        serialized_errors.append(serialized_error)

    return serialized_errors


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning(f"Validation error: {exc}")

    serialized_errors = _serialize_validation_errors(exc.errors())

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Ошибка валидации входных данных",
            "error_code": "VALIDATION_ERROR",
            "details": serialized_errors
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "error_code": "HTTP_ERROR"
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Внутренняя ошибка сервера",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )


EXCEPTION_HANDLERS = {
    TaskNotFoundError: task_not_found_handler,
    TaskValidationError: task_validation_handler,
    TaskStatusTransitionError: task_status_transition_handler,
    TaskAlreadyExistsError: task_already_exists_handler,
    TaskBusinessRuleViolationError: task_business_rule_handler,
    TaskDomainError: generic_task_domain_handler,
    RequestValidationError: validation_exception_handler,
    HTTPException: http_exception_handler,
    Exception: generic_exception_handler,
}
