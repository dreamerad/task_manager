import pytest
import asyncio
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_task_data():
    return {
        "title": "Тестовая задача",
        "description": "Описание тестовой задачи"
    }


@pytest.fixture
def sample_task_update_data():
    return {
        "title": "Обновленная задача",
        "description": "Обновленное описание",
        "status": "в работе"
    }
