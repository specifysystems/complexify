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
# Database
# .....................................................................................
# Contoller?
# .....................................................................................
# Makeflow

# .....................................................................................
# Catalog Server
#  Catalog server image, starts and maintains an instance of cctools catalog server

FROM conda_base as cat_server

RUN conda install -y -c conda-forge ndcctools
SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["catalog_server", "-p", "9097"]

# .....................................................................................
# Worker
#   Container that does computational work.  Use cctools work queue factory as daemon

FROM conda_base as worker

RUN conda update -n base -c conda-forge conda && \
    conda install -y -c conda-forge ndcctools tiledb=2.2.9 gdal libspatialindex rtree git openjdk=8

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
ENTRYPOINT ["work_queue_factory", "-T", "local", "-M", "lm*", "--catalog=cat_server:9097"]
