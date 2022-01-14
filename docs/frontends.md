# Frontends
Set of named entry points for all branded projects in the Lifemapper and Specify Network
Universe.

Computational workflows are defined in (CCTools) Makeflows, dispatched to Workers.

## Goals
Frontends accessible to outside users through APIs, and possibly client libraries and
simple web applications.

## Initial frontends:

### Biotaphy
A publicly accessible set of APIs and a web application allowing users to
request a workflow.  This frontend will
* accept a newly requested workflow through APIs or through the web application
  (which wrap the APIs)
* error check and assemble the data and parameters
* create a makeflow for pickup by a worker

This access point will replace https://data.lifemapper.org/biotaphy/


### Public Lifemapper archive

A publicly accessible set of APIs and a web-based user interface to an archive of SDMs
computed from GBIF data, for a pretty face on SDM tools and on Lifemapper-GBIF collaboration.
This frontend serves data through APIs and maps through a mapping application (Mapserver?).
It has a website with interactive exploration tools built on top of the APIs and mapping
application.

Archive creation is initiated by an LM administrator, with GBIF data, scenarios,
parameters, by sending (or referencing) input data to the toolbox.  The toolbox returns
outputs (or references on shared storage).  The workflow initially consists of 3 steps:
 1. CSV sort/split (in: GBIF data)
 2. SDM (in: step 1 output, scenarios, parameters)
 3. Package (in: step 2 output)

This replaces the APIs and web application in the old LmServer for query/explore of
SDMs built from the GBIF archive.


### Broker

Set of API tools that accept data requests, assembles responses from one or more
external data sources, standardizes results, and returns results.

Synchronous requests, such as taxonomic information, or single point resolution, will
be resolved locally. Asynchronous requests, such as all species X data from aggregator Y
will be sent to the Toolbox for resolution and standardization (and optionally other
processing, such as data cleaning), then passed through the Broker back to the user.

SDM processing for users will be accessed through the Broker

### Syftorium (to be renamed?)

Public access to the tools  Toolbox/Ansychronous Workflow Machine.

### Specify Cache
