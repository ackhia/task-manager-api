FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10


ENV MODULE_NAME=app.main \
    VARIABLE_NAME=app \
    PORT=8000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

WORKDIR /app

USER root

# Install OS dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev curl \
 && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

# Copy dependency metadata first for caching
COPY pyproject.toml uv.lock* /app/

# Export lockfile and install into system Python
RUN uv export --frozen --no-dev > requirements.txt \
 && uv pip install --system -r requirements.txt

# Copy the rest of the project
COPY . /app

RUN mkdir -p /app/data \
 && chown -R 1000:1000 /app

USER 1000

EXPOSE 8000