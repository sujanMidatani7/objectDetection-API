FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock /app/
COPY ./app /app/app
COPY ./app requirements.txt /app/

# Sync the project
RUN uv add -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
