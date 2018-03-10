FROM python:stretch

ADD ./container /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python3", "run.py"]
