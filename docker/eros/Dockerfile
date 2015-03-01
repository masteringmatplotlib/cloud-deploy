FROM oubiwann/python
MAINTAINER Py3 Hacker <you@py.hacker>
RUN git clone https://github.com/masteringmatplotlib/cloud-deploy.git
RUN pip3 install typecheck-decorator==0.3b
RUN pip3 install Image
RUN pip3 install scikit-image
RUN pip3 install boto
RUN pip3 install awscli
CMD PYTHONPATH=./cloud-deploy/lib:$PYTHONPATH python3
