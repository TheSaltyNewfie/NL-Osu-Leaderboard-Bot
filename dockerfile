FROM python:3.10.11

WORKDIR /app

ENV TOKEN=change_me
ENV CLIENT_ID=change_me
ENV CLIENT_SECRET=change_me
ENV MYSQL_IP=change_me
ENV MYSQL_USER=change_me
ENV MYSQL_PASS=change_me
ENV MYSQL_DB_NAME=change_me

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /db/ ./db/

COPY main.py .
CMD ["python", "main.py"]