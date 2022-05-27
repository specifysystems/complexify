# .....................................................................................
# Conda base
#  Base image for installing packages with Conda
FROM conda/miniconda3:latest as conda_base

RUN conda update -n base -c conda-forge conda
# Install conda-pack for shrinking images
# RUN conda install -c conda-forge conda-pack

# .....................................................................................
# Web server
# .....................................................................................
FROM ubuntu:latest as complexify_api

RUN apt-get update && apt-get install -y python3 python3-pip sqlite3

# Copy web requirements
COPY ./web-requirements.txt /app/requirements.txt
COPY ./complexify/common /app/complexify/common
COPY ./complexify/web /app/complexify/web
COPY ./complexify/task_definitions /app/task_definitions

EXPOSE 5000

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install -r /app/requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "/app/complexify/web/app.py" ]


# .....................................................................................
# Job Flow container - Wrapped makeflows

FROM conda_base as job_flow

RUN conda update -n base -c conda-forge conda && \
    conda install -y -c conda-forge ndcctools zip unzip

COPY ./job_flow-requirements.txt /app/requirements.txt
COPY ./complexify/common /app/complexify/common
COPY ./complexify/job_flow /app/complexify/job_flow

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install -r /app/requirements.txt

SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["python", "/app/complexify/job_flow/daemon.py"]

# .....................................................................................
# Catalog Server
#  Catalog server image, starts and maintains an instance of cctools catalog server

FROM conda_base as cat_server

RUN conda update -n base -c conda-forge conda && \
    conda install -y -c conda-forge ndcctools

SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["catalog_server", "-p", "9097"]

# .....................................................................................
# Worker
#   Container that does computational work.  Use cctools work queue factory as daemon

FROM conda_base as worker

RUN conda update -n base -c conda-forge conda && \
    conda install -y -c conda-forge ndcctools tiledb=2.2.9 gdal libspatialindex rtree git zip openjdk=8

ENV PROJ_LIB=/usr/local/share/proj/

RUN pip install specify-lmpy

# Install BiotaPhyPy
RUN mkdir git && \
    cd git && \
	git clone https://github.com/biotaphy/BiotaPhyPy.git && \
	cd BiotaPhyPy && \
	pip install .

# Install lmtools
RUN cd git && \
    git clone https://github.com/specifysystems/lmtools.git && \
	cd lmtools && \
	pip install .

# Maxent
RUN cd git && \
    git clone https://github.com/mrmaxent/Maxent.git

ENV MAXENT_VERSION=3.4.4
ENV MAXENT_JAR=/git/Maxent/ArchivedReleases/$MAXENT_VERSION/maxent.jar

SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["work_queue_factory", "-T", "local", "--debug=all", "-N", "lm.\\*", "--catalog=catalog_server:9097"]
