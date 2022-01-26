FROM conda/miniconda3:latest as cctools

RUN conda update -n base -c conda-forge conda
RUN conda install -y -c conda-forge ndcctools gdal libspatialindex rtree


FROM cctools as worker

RUN apt-get update && \
    apt-get install -y git openjdk-8-jdk

RUN pip install specify-lmpy

RUN mkdir git && \
    cd git && \
    git clone https://github.com/mrmaxent/Maxent.git

ENV MAXENT_VERSION=3.4.4
ENV MAXENT_JAR=/git/Maxent/ArchivedReleases/$MAXENT_VERSION/maxent.jar
