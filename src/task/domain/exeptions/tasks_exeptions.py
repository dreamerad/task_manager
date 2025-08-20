class TaskDomainError(Exception):

    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)


class TaskNotFoundError(TaskDomainError):

    def __init__(self, task_id: str):
        message = f"Задача с ID {task_id} не найдена"
        super().__init__(message, "TASK_NOT_FOUND")
        self.task_id = task_id


class TaskValidationError(TaskDomainError):

    def __init__(self, message: str):
        super().__init__(message, "TASK_VALIDATION_ERROR")


class TaskStatusTransitionError(TaskDomainError):

    def __init__(self, from_status: str, to_status: str):
        message = f"Невозможно изменить статус с '{from_status}' на '{to_status}'"
        super().__init__(message, "TASK_STATUS_TRANSITION_ERROR")
        self.from_status = from_status
        self.to_status = to_status


class TaskAlreadyExistsError(TaskDomainError):

    def __init__(self, task_id: str):
        message = f"Задача с ID {task_id} уже существует"
        super().__init__(message, "TASK_ALREADY_EXISTS")
        self.task_id = task_id


class TaskBusinessRuleViolationError(TaskDomainError):

    def __init__(self, message: str):
        super().__init__(message, "TASK_BUSINESS_RULE_VIOLATION")


def handle_task_domain_error(error: TaskDomainError) -> dict:
    return {
        "success": False,
        "error": error.message,
        "error_code": error.error_code
    }


def is_task_domain_error(error: Exception) -> bool:
    return isinstance(error, TaskDomainError)
