FROM python:3.10.11

WORKDIR /app

ENV TOKEN=change_me
ENV CLIENT_ID=change_me
ENV CLIENT_SECRET=change_me

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY osunldatabase_temp.json .

COPY main.py .
CMD ["python", "main.py"]