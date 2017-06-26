FROM python:3.4.6-slim

LABEL maintainer "contact@felixtan.io"

ENV WORKING_DIR="/home/app"

RUN pip3 install django==1.11 psycopg2==2.7 && \
    mkdir ${WORKING_DIR}

WORKDIR ${WORKING_DIR}

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
