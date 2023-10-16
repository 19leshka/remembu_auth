ARG python=python:3.11.5-slim

# Build stage:
FROM ${python} AS build

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      build-essential \
      libpq-dev

# Create the virtual environment.
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /app

RUN pip install poetry
# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Final stage:
FROM ${python}

# Install the runtime-only C library dependencies we need.
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      libpq5

# Copy the virtual environment from the first stage.
COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

# Copy the application in.
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "log_config.yml"]