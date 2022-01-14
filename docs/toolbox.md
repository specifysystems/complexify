# Toolbox
Set of backend computational tools for all branded projects in the Lifemapper and 
Specify Network Universe.

Computational workflows are accepted as (CCTools) Makeflows, initiated by Workers.

This corresponds loosely to LmCompute in old Lifemapper.

Also known as Asynchronous Workflow Machine


## Goals
Toolbox that will perform computations on well-defined inputs producing defined outputs.  
This will perform calculations for Lifemapper  


## Initial data categories:

**typeodata** (species/environmental/scenario type):
  * code, name, description
  * examples
    * species: Bison, Bison, "Genus level, two extant and six extinct species of bison"
    * environmental: BIO1, annual_temp, "Annual Mean Temperature"
    * scenario: WORLDCLIM-curr, curr_climate, "Worldclim 1.4 Bioclimatic variables"
    * biogeo hypotheses: continental_divide, "Continental Divide", 
    * shpgrid: shapegrid_na1, "NA 1 degree", "North American, 1 degree resolution"
  
**geolayer**
  * filename, typeodata, metadata (dict)
  * categories:
    * Species occurrence point file
      * csv_filename, typeodata (species), metadata (contains field definition filename or field defs)
    * Species distribution raster
      * rst_filename, typeodata (species), metadata (value range, meaning)
    * Environmental raster (env_rst)
      * rst_filename, typeodata (environmental), metadata (may be empty)
    * SDM projection (sdm_rst)
      * rst_filename, typeodata (species), metadata (SDM modeling, projection params)
    * Biogeographic hypotheses (biogeo)
      * shp_filename, typeodata, metadata (value meanings)
    * Shapegrid (Vector/polygon layer for assessing the contents of each cell/polygon)
      * shp_filename, typeodata (shpgrid)
    
**scenario**: list of raster (all environmental data)
  * [envraster, ...], typeodata


## Initial tools:

All tools create metadata which can be stored, converted to EML, used for packaging.  
Metadata from multi-step workflows can be aggregated to describe the final outputs of
workflow, and provide information for query and package display.


**CSV (Occurrences) sort/split on field (species)**
   * IN: CSV file containing multiple species
   * IN: metadata file defining fields (group)
   * OUT: list of occdata (CSV files)

**SDM**
  * IN: list of species occurrence files 
  * IN: list of scenarios (with matching spentypes)
  * IN: parameters (algorithm, algparams, modeling-typeodata)
  * OUT: list of sdm_proj

**Build Shapegrid**
  * IN: parameters (extent, resolution, etc)
  * OUT: shapegrid

**Intersect**
   * IN: list of geolayers (i.e. any of species occ, species raster, env raster, sdm proj, biogeo)
   * IN: shapegrid
   * IN: parameters (intersection rules)
   * OUT: matrix (aka PAM, GRIM, etc)

**RAD Calc**
  * IN: matrix
  * IN: parameters (desired calcs and parameters)
  * OUT: list of calculations, individual measures, matrices, tables, etc

**Packaging**



Roadmap to new Toolbox
