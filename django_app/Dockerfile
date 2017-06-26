FROM ubuntu:16.04

# Download, build, install Python3.4
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        apt-utils \
        wget \
        xz-utils \

        # Python3 build dependencies
        build-essential \
        libssl-dev \
        libbz2-dev \
        libgdbm-dev \
        libsqlite3-dev \
        libncursesw5-dev \
        tk-dev \
        liblzma-dev \
        libreadline-dev && \

    wget https://www.python.org/ftp/python/3.4.6/Python-3.4.6.tar.xz && \
    tar xvf Python-3.4.6.tar.xz && \
    rm Python-3.4.6.tar.xz && \
    cd Python-3.4.6 && \
    ./configure && \
    make && \
    # make test && \
    make install && \
    cd .. && \
    rm -rf cd Python-3.4.6

# Set up virtual env for Python3.4
RUN pip3 install virtualenv==15 && \
    virtualenv --python=$(which python3.4) env && \
    /bin/bash -c "source /env/bin/activate && \
        pip3.4 install django==1.11 psycopg2==2.7" && \
    mkdir /env/app

WORKDIR /env/app

EXPOSE 8000 8000

CMD ["django-admin", "runserver"]
