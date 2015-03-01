FROM ipython/scipystack
MAINTAINER Duncan McGreggor <oubiwann@gmail.com>
ENV PYDIR Python-3.4.2
ENV PYBALL ${PYDIR}.tgz
RUN apt-get build-dep -y python3.4
RUN curl -L -o $PYBALL https://www.python.org/ftp/python/3.4.2/$PYBALL && \
    tar xvzf $PYBALL && \
    cd $PYDIR && \
    ./configure && \
    make && \
    make install
CMD python3
