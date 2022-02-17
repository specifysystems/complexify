# New Archive / Syftorium computations workflow

## Version 1

This version focuses on recursively splitting the occurrence data by taxonomy until we get to the species
level where models and Syftorium analyses are performed.  The outputs are then packaged on the way back
up the taxonomic tree until there is a full package of outputs and Syftorium data.  It will be important
to add more collection analysis steps for Syftorium and add multispecies analyses to the outputs.


## Diagram

![This is an image](https://github.com/specifysystems/complexify/blob/main/docs/species_wf.drawio.png)


## Symbology

* Yellow ellipses indicate files
* Green rectangles are processes
* Boxes with dotted lines indicate that the contained is done multiple times (for each genus, species, occurrence file, etc)
* Arrowed lines show flow from one process to the next


## Basic Summary

The workflow starts by reading one or more occurrence data files with unknown contents.  As the data is
read from each file, it is modified as necessary (resolving taxon name, converting to a common format,
etc) and split according to some value, like Kingdom name, then written to the appropriate file location.
We also write out a file containing all values for each kingdom (all phyla present in each kingdom)
along with the data files.

The information about the phyla in the kingdom is used to create a web page for the kingdom.  This page
will also reference the heat map generated using the kingdom's occurrences.

The occurrence data will be split recursively using the same method by using each rank in the taxon tree.
Each of the taxa will have a web page generated as well as a heat map of point distributions for that taxon.
This process continues until species level where additional steps are performed such as creating a
distribution model and syftorium analyses.  These outputs are then packaged for each species and returned
to the genus workflow which assembles all of the outputs for each species it contains and packages them
before returning those to the family, which repeats the process for all of the genera.  This continues
until we reach the domain level where all of the outputs are assembled into a package to be returned
and a collection of syftorium outputs to be cataloged by the syftorium web services.
