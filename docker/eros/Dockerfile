FROM oubiwann/python
MAINTAINER Py3 Hacker <you@py.hacker>
RUN git clone https://github.com/masteringmatplotlib/cloud-deploy.git && \
    cd cloud-deploy && \
    make docker-setup
CMD PYTHONPATH=./cloud-deploy/lib:$PYTHONPATH python3
