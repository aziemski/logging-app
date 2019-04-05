FROM python:3.7

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY app /app

ENTRYPOINT ["python", "-u", "app.py"]
