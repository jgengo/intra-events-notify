FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache wget

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

RUN adduser -D -s /bin/sh app
RUN chown -R app:app /app

COPY . .
RUN chown -R app:app /app
USER app

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 