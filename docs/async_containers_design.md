# Containers for Asynchronous Computations

## Initial Design

The initial design includes two container types: a controller and one or more workers.  The controller container is kept
alive by running an instance of the CC Tools Catalog Server and Makeflow instances are ran as needed.  The worker
container runs an instance of the WorkQueue Factory to ensure that a worker is always running and asking if work is
available from any of the Makeflow instances connected to the catalog server.

## Diagram

![This is an image](https://github.com/specifysystems/complexify/blob/6ff41d549b966cb549cbf21c55ea87c79423c205/docs/Async%20Containers.drawio.png)

### Symbology

* Containers are shown in blue
* Continuously running processes are shown in green
* Single-run scripts are shown in yellow

### Explanation

#### Controller Container

When the controller container starts up, it starts an instance of the CC Tools `Catalog Server`.  This serves as a deamon
process that will keep the container alive when computations may be idle.  It also serves as the gatekepeer to any
computations that need to be ran.

When a new workflow needs to be run, it starts and configures an instance of `Makeflow`.  This `Makeflow` instance registers
with the `Catalog Server` and advertises that it has work available for computation.  Workers connect to the `Makeflow`
instance (via the `Catalog Server`) and run available computations.  As `Makeflow` runs, it distributes work to the
connected workers and makes new work available as previous dependencies are completed.  Once all work is finished, the
`Makeflow` instance completes and stops.

The `Catalog Server` supports multiple instances of `Makeflow` and allows workers to move between those instances as
available work shifts from one to another.

#### Worker Container

There can, and probably should, be multiple instances of the worker container.  Each worker container starts up an
instance of the `WorkQueue Factory`.  The job of the `WorkQueue Factory` process is to keep the container alive as well as
to maintain an individual `WorkQueue Worker`.  This means that as a `WorkQueue Worker` instance completes for any reason,
the `WorkQueue Factory` will start another `WorkQueue Worker` instance so that there are always workers available to
perform computations.

The `WorkQueue Worker` instance is configured to connect to the `Catalog Server` running on the Controller Container and
to ask the `Catalog Server` which `Makeflow` instance it should connect to so that it can perform some work.  The
`Catalog Server` responds with a `Makeflow` instance and the `WorkQueue Worker` connects to it.  Once connected to a
`Makeflow` instance, the `WorkQueue Worker` asks for an individual task to perform.  The `Makeflow` instance responds
with job information (command to run, input files, what files should be returned) and the `WorkQueue Worker` runs the
job.  Once the `WorkQueue Worker` completes the task, it returns the result to the `Makeflow` instance and asks for
another job.  This cycle repeats until there is no additional work for the `WorkQueue Worker` to perform, either
because it has all be computed or there are no additional tasks that have their dependencies met at that time.  At
this point, the `WorkQueue Worker` instance will either finish and stop, or request another `Makeflow` instance to
connect to from the `Catalog Server`.  If the `WorkQueue Worker` stops (for any stopping condition), the
`WorkQueue Factory` will start another one.
