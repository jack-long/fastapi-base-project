# syntax=docker/dockerfile:1
FROM python:3.11-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY app .
CMD ["uvcorn", "app.main:app"]