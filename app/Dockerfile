FROM ghcr.io/astral-sh/uv:0.12.17-python3.14-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY app/ app/

RUN useradd -m -u 1000 appuser
USER appuser

EXPOSE 8000

CMD ["echo", "Hello!"]
