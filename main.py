import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.core.logging.config import setup_logging
from src.task.api.exeption_handlers import EXCEPTION_HANDLERS
from src.task.api.rest import router as task_router
from src.core.database.config import init_database, close_database

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения Task Manager")
    try:
        await init_database()
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")
        raise

    yield

    logger.info("Остановка приложения Task Manager")
    try:
        await close_database()
        logger.info("Соединения с БД закрыты")
    except Exception as e:
        logger.error(f"Ошибка закрытия БД: {e}")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Task Manager API",
        description="API для управления задачами с CRUD операциями",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    for exception_class, handler in EXCEPTION_HANDLERS.items():
        app.add_exception_handler(exception_class, handler)

    app.include_router(task_router, prefix="/api")

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    @app.get("/health", include_in_schema=False)
    async def health_check():
        return {"status": "healthy", "message": "Task Manager API is running"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)