FROM python:stretch

ADD ./container /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3","-u", "run.py"]
