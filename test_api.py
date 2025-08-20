import os

import requests

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
API_TASKS_URL = f"{API_BASE_URL}/api/tasks"


def test_create_task():
    payload = {
        "title": "Тестовая задача",
        "description": "Описание тестовой задачи"
    }

    response = requests.post(API_TASKS_URL, json=payload)

    if response.status_code == 201:
        task = response.json()
        print(f"Задача создана: {task['id']}")
        return task
    else:
        print(f"Ошибка создания задачи: {response.status_code}")
        return None


def test_get_task(task_id):
    response = requests.get(f"{API_TASKS_URL}/{task_id}")

    if response.status_code == 200:
        task = response.json()
        print(f"Задача получена: {task['title']}")
        return task
    else:
        print(f"Ошибка получения задачи: {response.status_code}")
        return None


def test_update_task(task_id):
    payload = {
        "title": "Обновленная задача",
        "status": "в работе"
    }

    response = requests.put(f"{API_TASKS_URL}/{task_id}", json=payload)

    if response.status_code == 200:
        task = response.json()
        print(f"адача обновлена: {task['title']} - {task['status']}")
        return task
    else:
        print(f"Ошибка обновления задачи: {response.status_code}")
        return None


def test_get_all_tasks():
    response = requests.get(API_TASKS_URL)

    if response.status_code == 200:
        tasks = response.json()
        print(f"Получено задач: {tasks['total']}")
        return tasks
    else:
        print(f"Ошибка получения списка задач: {response.status_code}")
        return None


def test_delete_task(task_id):
    response = requests.delete(f"{API_TASKS_URL}/{task_id}")

    if response.status_code == 204:
        print(f"Задача удалена")
        return True
    else:
        print(f"Ошибка удаления задачи: {response.status_code}")
        return False


def test_error_handling():
    payload = {"description": "Задача без названия"}
    response = requests.post(API_TASKS_URL, json=payload)

    if response.status_code == 422:
        print("Ошибка валидации обработана корректно")
    else:
        print(f"Неожиданный статус: {response.status_code}")

    fake_id = "123e4567-e89b-12d3-a456-426614174000"
    response = requests.get(f"{API_TASKS_URL}/{fake_id}")

    if response.status_code == 404:
        print("Ошибка 404 обработана корректно")
    else:
        print(f"Неожиданный статус: {response.status_code}")


def main():
    print("Запуск тестов API Task Manager")
    print(f"API URL: {API_TASKS_URL}")
    print("-" * 50)

    # Тест создания задачи
    task = test_create_task()
    if not task:
        return

    task_id = task['id']

    retrieved_task = test_get_task(task_id)
    if not retrieved_task:
        return

    updated_task = test_update_task(task_id)
    if not updated_task:
        return

    all_tasks = test_get_all_tasks()
    if not all_tasks:
        return

    test_error_handling()

    print("-" * 50)
    print("Все тесты завершены!")


if __name__ == "__main__":
    main()
