FROM python:2.7.12-alpine

RUN mkdir -p /root/.pip/
COPY pip.conf /root/.pip/
  
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories

RUN apk add --update gcc g++ libgcc make \
    && zlib-dev libjpeg-turbo-dev tiff-dev \
    && mariadb-dev 

RUN pip install pillow mysqlclient