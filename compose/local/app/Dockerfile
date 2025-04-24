################################
# PYTHON-BASE
# Env variables
################################
FROM python:3.13.3-slim AS python-base

# python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Pip Settings
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=2.1.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    # paths
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    APP_PATH="/app"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

################################
# BUILDER-BASE
# Common dependencies
################################
FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        make \
        curl \
        build-essential \
        libpq-dev  \
        wait-for-it \
        gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

# copy project requirement files here to ensure they will be cached
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN --mount=type=cache,target=/root/.cache \
    poetry install --without=dev

################################
# DEVELOPMENT
# Development environment and devcontainer
################################
FROM python-base AS development
ENV FASTAPI_ENV=development
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
WORKDIR $PYSETUP_PATH

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo build-essential git bash-completion nano ssh make wait-for-it libpq-dev

# Installs dev-only dependencies
RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev

# Create devcontainer user and add it to sudoers
RUN groupadd --gid 1000 dev-user \
  && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
  && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
  && chmod 0440 /etc/sudoers.d/dev-user

# Give dev-user ownership of $PYSETUP_PATH
RUN chown -R dev-user:dev-user $PYSETUP_PATH \
  && chown -R dev-user:dev-user /home/dev-user

# Code mount point
WORKDIR $APP_PATH

COPY ./compose/production/app/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY . $APP_PATH

ENTRYPOINT ["/entrypoint"]

################################
# PRODUCTION
# Final runtime
################################
FROM python-base AS production
ENV FASTAPI_ENV=production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
WORKDIR $APP_PATH
RUN addgroup --system app \
  && adduser --system --ingroup app app

COPY --chown=app:app ./compose/production/app/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=app:app ./compose/production/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --chown=app:app . $APP_PATH
RUN chown -R app:app $APP_PATH

USER app

ENTRYPOINT ["/entrypoint"]
