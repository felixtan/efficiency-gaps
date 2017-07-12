FROM python:3.4.6-slim
# FROM python:3.4.6

LABEL maintainer "contact@felixtan.io"

RUN pip3 install django==1.11 \
                 psycopg2==2.7 \
                 python-decouple==3.0


RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends postgresql && \
    apt-get clean

WORKDIR "/home"

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]
