General approach
================

The initial approach I am taking is to have a controlling container that manages makeflow workflows and (potentially) multiple worker
containers that connect to this controlling container (via Docker network) to pull work and push back results via WorkQueue workers.

I think that a few more containers will become useful eventually for a web interface and some sort of light database for workflows.
It may also be useful to have a "matt daemon" like service running in another container to connect to the controller.

Makeflow Controller Container - makeflow
========================================

The "makeflow" container runs an instance of the cctools catalog server.  I am currently manually starting makeflows and registering
them with the catalog server but it may be better to have a "matt daemon" like container that pulls workflows and submits them to
the catalog server rather than doing everything in the same container.

Worker Container - worker
=========================

The "worker" container builds off of the controller container (same base install of cctools and others) and each instance runs
"work_queue_factory" to continuously run "work_queue_workers" to compute jobs.  This base worker container should probably be 
"subclassed" for various unrelated computations but currently we install all compute tools (lmpy, maxent, syftorium, etc).  The
primary reason for that is how the containers are started.  For this first iteration, I specify a number of workers to start when
bringing up the Docker compose file.  Ideally, this could be dynamic and more workers of one type could be started when they are
needed (more SDM workers when creating SDMs, less when doing occurrence set analyses or other).

We can set up makeflows to require different workers for different job types via categories.


Things to figure out
====================

1. We need to share a network across multiple physical machines and start workers on multiple physical machines that can talk to the controller.
2. Can we dynamically scale up and down workers of various types to meet computation needs?
3. It does seem that each container "should do one thing and do it well", should we split things up more to do that?
