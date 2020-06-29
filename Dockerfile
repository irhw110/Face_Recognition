# Base
FROM centos:centos7 

# System dependencies
RUN yum install -y \
        epel-release \
    && yum install -y \
        python3 python3-pip \
        python3-dev build-essential \
        python3-devel \
        make \
        gcc \
        gcc-c++ \
        cmake \
    && yum clean all

RUN python3 -m pip install --upgrade pip

# Install requirement
ADD requirements.txt /apps/face_compare/requirements.txt
RUN pip3 install -r /apps/face_compare/requirements.txt

RUN pip3 install opencv-python
RUN yum install -y libXext libSM libXrender

# Source code
COPY . /apps/face_compare
WORKDIR /apps/face_compare

# Network interfaces
EXPOSE 5000

CMD python3 -u api.py