FROM python:3.11-slim as base

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY pyproject.toml ./
COPY README.md ./

RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e .

COPY src/ ./src/
COPY main.py ./

RUN mkdir -p logs reports && \
    chown -R appuser:appuser /app && \
    chmod 755 logs && \
    chmod 777 reports

USER appuser

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base as development

USER root

RUN . .venv/bin/activate && \
    uv pip install -e ".[dev,test]"

RUN mkdir -p tests && \
    chown -R appuser:appuser /app && \
    chmod 755 logs && \
    chmod 777 reports

USER appuser

CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base as production

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1