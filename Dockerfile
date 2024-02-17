FROM python:3.11-bullseye

RUN apt update && apt update && apt install -y postgresql-client
RUN apt install -y libblas3 liblapack3 liblapack-dev libblas-dev gfortran libatlas-base-dev

RUN pip install poetry==1.7.1
ENV POETRY_VIRTUALENVS_IN_PROJECT true

COPY pyproject.toml /app/
WORKDIR /app
RUN poetry install --no-interaction --no-root --no-dev

COPY . /app

RUN poetry install --no-interaction
ENTRYPOINT ["poetry", "run", "sentinel", "-v"]
