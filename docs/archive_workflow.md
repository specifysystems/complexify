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

