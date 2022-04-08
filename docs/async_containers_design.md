# Containers for Asynchronous Computations

## Design (April 8, 2022)

The design includes five or six container types as documented below.

## Diagram

![System Design](images/lm_container_diagram.drawio.png)

Symbology:
* Boxes are individual container types with a title and the main tools on the container
* Arrows indicate communication
* Ellipses indicate that multiple instances of a container can / will exist


### Containers

#### Web Services Container

The web services container runs some Python web services framework, probably Flask, on top of some web server, like NGINX.
The job of this container is to provide web services for job submission, job status check, and output retrieval.

#### Database Container

The database container should provide a very light database framework for storing workflow job information.  This likely
only needs one or two tables.

#### LM Controller Container (may not be needed)

The LM controller container would act like the `MattDaemon` tool did in the previous incarnation of Lifemapper.  It would
determine when and how many workflow jobs to run and then start instances of the `Makeflow Container`.  There may be some
security concerns with a container starting other containers so we may skip this container in favor of running a more
static number of `Makeflow Containers`.  

#### Makeflow Container

The makeflow container pulls a job from the database and runs the computations.  This will likely involve translating a
job request from some configuration file (likely JSON) into one or more Makeflow files.  We would run multiple instances
of the makeflow container that are started either by the `LM Controller Container` or we would set some `scale` value at
start up.  If we use teh LM Controller Container, these makeflow containers would run once and then exit.  If we do not,
there would be an added daemon that would get a workflow job to run, run everything, catalog the results, and then repeat.

#### Catalog Server Container

The Catalog Server Container runs an instance of the CC Tools Catalog Server.  ALl makeflow instances would register with
the catalog server and advertise available work for the workqueue instances.  Workqueue instances connect to the catalog
server which helps determine which of the running makeflow instances they should connect to.

#### Worker Container

The worker container does the actual computational work.  We would run multiple copies of this image to achieve a level
of parallelism.  Each running container would utilize CC Tools WorkQueue factory to continuously request work via the
catalog server and then individual running makeflows.  The work should use one of the available tools from lmpy, lmtools,
biotaphypy, and syftr.

----

### Example job flow

1. A job request is submitted via a web service call to the `Web Services Container`
2. The `Web Services Container` validates the request
3. The `Web Services Container` catalogs the job request using the `Database Container` and returns a callback URL to the user
4. A `Makeflow Container` is started by `LM Controller Container` (or already running)
5. The `Makeflow Container` translates the job request into one or more makeflows
6. Each makeflow registers with the catalog server on the `Catalog Server Container`
7. Instances of `Worker Container` run WorkQueue workers that connect to the catalog server on `Catalog Server Container` to find the makeflow to connect to
8. WorkQueue workers on `Worker Container` instances pull, run, and send back completed tasks to a makeflow on `Makeflow Container`
9. Once all work is complete the `Makeflow Container` catalogs outputs and updates the job status on the `Database Container`
10. Status checks through web services on `Web Service Container` now show that the job is complete and provide an output download URL
11. The user requests and downloads the output package for the job they submitted from `Web Services Container`.
