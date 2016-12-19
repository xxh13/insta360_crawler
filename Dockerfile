FROM thonatos/ubuntu-python-phantomjs:2.7-2.1.1

MAINTAINER Thonatos.Yang <thonatos.yang@gmail.com>
LABEL vendor=implements.io
LABEL io.implements.version=0.1.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends supervisor nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app \
	&& mkdir -p /var/log/supervisor/ \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

ADD root /

# run server
COPY src/ /app

WORKDIR /app/

RUN pip install -r requirements.txt

EXPOSE 80 443 8000

CMD ["/usr/bin/supervisord","-n"]