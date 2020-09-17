FROM python:3.7

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Some ugly copying
COPY ./app ./app
COPY app.py ./app
COPY logging.conf ./app
COPY ./api ./app/api
COPY .env ./app

WORKDIR /app

# install dependencies
RUN pip install --upgrade pip

RUN pip install -r api/requirements/base.txt

ENTRYPOINT ["python"]
CMD ["app.py"]