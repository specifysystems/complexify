# Run a Makeflow By Hand

* Start up the containers

  ```commandline
  docker-compose up
  ```

* Attach to the job flow container

  ```commandline
  docker-compose exec job_flow bash
  ```

* Start a makeflow (from the jobflow container)

  ```commandline
  makeflow -C catalog_server:9097 -T wq -a -N lm-some_name --jx some_makeflow.jx
  ```

* If you need to re-run, clean up the makeflow first

  ```
  makeflow -c --jx some_makeflow.jx
  ```

makeflow -C catalog_server:9097 -T wq -N lmheuchera -a --jx ../demo_makeflows/split_occ_makeflow.jx

work_queue_factory -T local -S ./cj/ --catalog=catalog_server:9097 -M lm.\*
