FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -U pip
RUN apt-get update
ADD . /code/
ADD start.sh .
ADD wait-for-it.sh .
RUN ["chmod", "+x", "./start.sh"]
RUN ["chmod", "+x", "./wait-for-it.sh"]


RUN pip install -r requirements.txt
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y build-essential
RUN apt-get install -y libssl-dev
RUN apt-get install -y python3-dev
RUN apt-get install -y default-libmysqlclient-dev

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# fr_FR.UTF-8 UTF-8/fr_FR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG fr_FR.UTF-8
ENV LC_ALL fr_FR.UTF-8