# Task Definitions

## Description

This directory contains task metadata that will be exposed through the API.  Each file defines
the metadata for a particular task including inputs, outputs, command to run, and identifier.
Any file added should include valid task metadata and it will automatically be made available
in Complexify.

## Schema

```
type: object
properties:
  identifier:
    type: string
  inputs:
    type: array
    items:
      type: object
      properties:
        name:
          type: string
        required:
          type: bool
        prefix:
          type: string
        data_type:
          type: string
		sub_types:
		  type: array
		choices:
		  type: array
  output:
    type: array
    items:
      type: object
      properties:
        name:
          type: string
        required:
          type: bool
        prefix:
          type: string
        data_type:
          type: string
		sub_types:
		  type: array
		choices:
		  type: array
  command:
    type: string
```
