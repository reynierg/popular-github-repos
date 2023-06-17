# pull official base image
FROM python:3.11.2-slim-buster

# patch the image with the most recent security updates and bug fixes, which may have been
# released since the image was published on Docker Hub:
RUN apt-get update && \
    apt-get upgrade --yes

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create a new user to use it instead of root, avoiding unrestricted access to the host system,
# in case that the image gets compromised
ENV USERNAME repossuser
RUN useradd --create-home $USERNAME
USER $USERNAME
WORKDIR /home/$USERNAME

# install packages in a vrtual environment, to avoid potential version conflicts with the base
# image's global python installation
ENV VIRTUALENV=/home/$USERNAME/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

# install python dependencies
COPY --chown=$USERNAME requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements-dev.txt

# add app
COPY --chown=$USERNAME . .

RUN python -m pytest tests/ && \
    python -m flake8 app/ tests && \
    python -m isort app/ tests/ --check && \
    python -m black app/ --check && \
    python -m pylint app/ --disable=C0114,C0115,C0116 && \
    python -m bandit -r app/


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
