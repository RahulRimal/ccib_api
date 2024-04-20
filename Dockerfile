FROM python:3.12

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    fish && \
    apt-get install -y pre-commit && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install pre-commit


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR /app
ENV USER app

RUN useradd -ms /bin/bash ${USER}
RUN groupadd -f ${USER}

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR ${PROJECT_DIR}

RUN chown -R ${USER}:${USER} .

USER ${USER}

SHELL ["/usr/bin/fish"]