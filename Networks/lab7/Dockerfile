# Pull base image
FROM python:3.10.6

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY requirements.txt .


RUN pip install -r /code/requirements.txt
COPY . /code

