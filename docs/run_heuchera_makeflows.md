# Run Heuchera Demo Makeflows

## Set up the demo

All commands are from the root of the `complexify` repository.  Create a demo directory (that will be shared with the `job_flow` container.)

```commandline
mkdir ./demo/
cp ./test_cases/heuchera/demo_makeflows/*.jx demo/
cp -r ./test_cases/heuchera/uploads/* demo/
```

## Start up the containers

Again, from the `complexify` repository root.

  ```commandline
  docker-compose up
  ```

## Attach to the job flow container

  ```commandline
  docker-compose exec job_flow bash
  ```

## Run the makeflows (from the job flow container)

### Run the split occurrences makeflow
  ```commandline
  # cd /demo/
  # makeflow -C catalog_server:9097 -T wq -N lmheuchera-occ -a --jx split_occ_makeflow.jx
  ```

### Unzip the species data and run SDMs makeflow

  ```commandline
  # cd /demo/
  # unzip species_records.zip
  # makeflow -C catalog_server:9097 -T wq -N lmheuchera-sdm -a --jx sdms_makeflow.jx
  ```

### Run multispecies makeflow
