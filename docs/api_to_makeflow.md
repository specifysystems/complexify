# API request to makeflow

We need a flexible method for creating workflows from API requests.  For single tasks,
this is fairly straightforward, for example, to create an SDM for a CSV file of occurrences,
`occurrence.csv` with environmental layers `bio1.asc`, `bio2.asc`, `bio3.asc` and some
maxent parameters, the request could look like:

```json
{
    "user": "Some User",
    "email": "myemail@user.com",
    "tasks": [
        {
            "name": "sdm_model",
            "inputs": {
                "occurrences": "occurrence.csv",
                "layers": [
                    "bio1.asc",
                    "bio2.asc",
                    "bio3.asc"
                ],
                # Maxent Parameters
                "do_clamping": true
            },
            "outputs": {
                "raster_filename": "my_model.asc",
                "log_filename": "my_model_log.txt"
            }
        }
    ]
}
```

This is fine for very simple tasks, but those simple tasks don't really require our services.
Let's say we have a slightly more complicated workflow and we want to create models for
three species, with data in the same `occurrence.csv` file, called `sp1`, `sp2`, and `sp3`.
Our request needs to be changed because we can only specify one output filename for the
raster and one for the log, but we have created three of each.  One thing we could do is
template the filenames so the request could look like:

```json
{
    "user": "Some User",
    "email": "myemail@user.com",
    "tasks": [
        {
            "name": "sdm_model",
            "inputs": {
                "occurrences": "occurrence.csv",
                "layers": [
                    "bio1.asc",
                    "bio2.asc",
                    "bio3.asc"
                ],
                # Maxent Parameters
                "do_clamping": true
            },
            "outputs": {
                "raster_filename": "{species}_model.asc",
                "log_filename": "{species}_model_log.txt"
            }
        }
    ]
}
```

Alternatively, we could just not specify output files and have the backend be smart enough
to name them different things.  That may work for this case but I think it is clear that
problems will arise when there are multiple outputs of the same type for a single process.
Additionally, specifying a request where the output of one process should be the input of
multiple other processes will also cause problems if we do not have a good way to specify
how the tasks should be connected.

I think that one potential option for addressing this is to use references.  This kind of
thing is done for formats like EML (and probably other XML formats) and I would guess JSON
as well.  So let's say that we want to create a unified dataset from our own `occurrence.csv`
file as well as a DarwinCore Archive file from gbif, `my_dwca.zip`.  We want to convert
the occurrence data into a common CSV format, clean it, and then create models for all of
the species then create an output package from those models.  We could do something like:

```json
{
    "user": "Some User",
    "email": "myemail@user.com",
    "tasks": [
        {
            "aggregate_and_clean_occurrence_data",
            "inputs": {
               "occurrence_inputs": [
                   {
                       "occurrence_type": "csv",
                       "occurrence_file": "occurrence.csv"
                       "species_key": "species_name",
                       "x_key": "lon",
                       "y_key": "lat",
                       "wranglers": [
                           {
                               "wrangler_type": "accepted_name_modifier",
                               "use_authority": "gbif"
                           }
                           {
                               "ref": "$csv_to_common_wrangler"
                           }
                       ]
                   },
                   {
                       "occurrence_type": "dwca",
                       "occurrence_file": "my_dwca.zip",
                       "wranglers": [
                           {
                               "ref": "$dwca_to_common_wrangler"
                           }
                       ]
                   }
               ]
               "aggregate_wranglers": [
                   {
                       "wrangler_type": "decimal_precision_filter",
                       "decimal_places": 4
                   }
                   {
                       "ref": "$duplicate_filter"
                   }
               ]
            },
            "task_id": "process_occurrences"
        }
        {
            "name": "sdm_model",
            "inputs": {
                "occurrences": {
                    "ref": "$process_occurrences.occurrence_sets"
                }
                "layers": [
                    "bio1.asc",
                    "bio2.asc",
                    "bio3.asc"
                ],
                # Maxent Parameters
                "do_clamping": true
            },
            "task_id": "maxent_models"
        },
        {
            "name": "package_models",
            "inputs": {
                "models": {
                    "ref": "$maxent_models.models"
                },
                # Maxent parameters and we'll assume enviornmental layers
                "model_parameters": {
                    "ref": "$maxent_models.parameters"
                }
            }
        }
    ],
    "definitions": [
       {
           "id": "duplicate_filter",
           "type": "data_wrangler",
           "wrangler_type": "duplicate_occurrence_filter"
       },
       {
           "id": "csv_to_common_wrangler",
           "type": "data_wrangler",
           "wrangler_type": "attribute_modifier_wrangler",
           "attributes": [
               {
                  "name": "species",
                  "map_field": "species_name"
               },
               {
                  "name": "x",
                  "map_field": "lon"
               },
               {
                  "name": "y",
                  "map_field": "lat"
               },
               {
                  "name": "source",
                  "const": "my_csv"
               }
           ]
       }
       {
           "id": "dwca_to_common_wrangler",
           "type": "data_wrangler",
           "wrangler_type": "attribute_modifier_wrangler",
           "attributes": [
               {
                  "name": "species",
                  "map_field": "species_epithet"
               },
               {
                  "name": "x",
                  "map_field": "decimalLongitude"
               },
               {
                  "name": "y",
                  "map_field": "decimalLongitude"
               },
               {
                  "name": "source",
                  "map_field": "dataset"
               }
           ]
       }
    ]
}
```

## Conversion from API request to Makeflow

Because the inputs and outputs are defined in this sort of schema, we can utilized those to
create Makeflows.  There are still some hurdles though as Makeflow does require known output
files and we don't necessarily know all of the outputs of a process upon definition.
However, we can get around this in a few ways, one of which is to actually utilize multiple
Makeflow configurations for a single request.  For example, we do not know what species are
contained in the occurrence data and therefore we do not know the individual files that will
be created (assuming they are related to species name) so we could have one workflow that
processes the occurrence data without knowing specific species outputs but it could still
produce a known aggregate file, named something like `all_occurrences.zip` and another file
`species_present.txt`.  At the conclusion of that makeflow, we would unzip
`all_occurrences.zip` and create a new makeflow for creating maxent models using the species
names that are present in `species_present.txt`.  There is a bit of magic left to figure out
but makeflow supports submakeflows so it may be possible to still do everything in one
umbrella process that creates sub-makeflows for future steps in earlier ones.  This isn't
an issue with the API to Makeflow conversion so much as an issue with creating a Makeflow
with outputs unknown at creation time.
