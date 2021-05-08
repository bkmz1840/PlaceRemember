# syntax=docker/dockerfile:1
FROM python:3.8
WORKDIR /placeRemember
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install coverage
COPY . .
CMD ["python", "manage.py", "test"]

