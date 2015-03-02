FROM ubuntu
MAINTAINER Duncan McGreggor <oubiwann@gmail.com>
ENV PYDIR Python-3.4.2
ENV PYBALL ${PYDIR}.tgz
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y -q ca-certificates git build-essential
RUN apt-get install -y -q libssl-dev libcurl4-openssl-dev
RUN apt-get install -y -q curl
RUN apt-get install -y -q cython3 libpython3.4-dev python3.4-dev
RUN apt-get build-dep -y python3.4
RUN curl -L -o $PYBALL https://www.python.org/ftp/python/3.4.2/$PYBALL && \
    tar xvzf $PYBALL && \
    cd $PYDIR && \
    ./configure && \
    make && \
    make install
RUN apt-get install -y -q python3-numpy python3-scipy python3-pandas
CMD python3
