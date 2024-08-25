FROM ubuntu:22.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

LABEL maintainer="pablochen <bogenarc@gmail>"

ENV PYTHON_VERSION=3.10

RUN apt-get update && \
    apt-get install -y python${PYTHON_VERSION} && \
	apt-get install -y python3-pip && \
	apt-get clean


WORKDIR /app

RUN \
   echo 'alias python="/usr/bin/python3"' >> /root/.bashrc && \
   echo 'alias pip="/usr/bin/pip3"' >> /root/.bashrc && \
   source /root/.bashrc

RUN pip install packaging

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN rm -rf /app/requirements.txt /app/Dockerfile

ENV PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "front.py", "--server.port", "1888"]