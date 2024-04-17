FROM python:3.10.13

WORKDIR /flask_709_22_1

COPY app.py .
COPY db.py .
COPY config.py .
COPY query.py .
COPY validate.py .

COPY requirements.txt .

RUN pip install -r requirements.txt