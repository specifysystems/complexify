"""Job processing tool to run computations for a job configuration."""
from enum import Enum
import os
import subprocess
import time
import zipfile

from complexify.common.tasks import ALL_TASKS


# .....................................................................................
CATALOG_SERVER = 'cat_server:9097'
POLL_WAIT_TIME = 30


# .....................................................................................
class TaskStatus(Enum):
    WAITING = 1
    RUNNING = 2
    COMPLETE = 3


# .....................................................................................
class JobProcessor:
    """A class for processing job configuration files with Makeflow."""
    # .......................
    def __init__(self, job_config):
        """Constructor for JobProcessor."""
        self.job_config = job_config
        self._process_incoming_tasks(job_config)
        self.log_files = []
        self.mf_files = []
        self.tasks = {}
        self.job_id = job_config['job_id']
        self.work_dir = self.job_id

    # .......................
    def _build_makeflow_command(self, jx_filename, log_filename):
        """Build a makeflow command to run a chunk of job tasks.

        Args:
            jx_filename (str): File with makeflow arguments in jx format.
            log_filename (str): File for makeflow logging.

        Returns:
            list: A list of command line arguments.
        """
        return [
            'makeflow',
            '-jx',
            jx_filename,
            '-T',
            'wq',
            '-C',
            CATALOG_SERVER,
            '-o',
            log_filename,
            '-a'
        ]

    # .......................
    def _get_next_makeflow(self):
        """Get the next makeflow configuration file to run.

        Returns:
            str: Path to file containing next makeflow configuration.
            str: Path to file for makeflow logging.
        """
        run_id = len(self.log_files)
        makeflow_config_filename = f'mf-{self.job_id}-{run_id}.jx'
        log_filename = f'log-{self.job_id}-{run_id}.log'
        blocked = set()
        for task_id, task in self.tasks.items():
            # Check if the task is waiting
            if task['status'] == TaskStatus.WAITING:
                # Check inputs, recurse as needed
                blocked = self._prepare_task_to_run(task_id, blocked=blocked)

        # Go through tasks and add any RUNNING tasks to next makeflow
        raise NotImplementedError()
        return makeflow_config_filename, log_filename

    # .......................
    def _get_task_outputs(self, task_id):
        """Get any task outputs that were previously unknown and mark task.

        Args:
            task_id (str): The task identifier string.
        """
        raise NotImplementedError()

    # .......................
    def _prepare_task_to_run(self, task_id, blocked=None):
        """Prepares a task to run if possible.

        Returns:
            set: A set of blocked task ids.
        """
        if blocked is None:
            blocked = set()
        # Todo: This check is likely redundant...
        if self.tasks[task_id]['status'] == TaskStatus.WAITING:
            # Check inputs
            for task_input in self.tasks[task_id]['inputs']:
                # If input is a reference, process it
                if 'ref' in task_input.keys():
                    ref_task_id = task_input['ref']
                    # If ref task is already blocked or outputs are unknown
                    #     this task is blocked
                    if ref_task_id in blocked or self.tasks[ref_task_id]['unknown_outputs']:
                        blocked.add(task_id)

                    # If reference task is waiting, recurse
                    elif self.tasks[ref_task_id]['status'] == TaskStatus.WAITING:
                        ref_blocked = self._prepare_task_to_run(ref_task_id)
                        if ref_task_id in ref_blocked:
                            blocked.add(task_id)
                            blocked.union(ref_blocked)
                # If this task is already blocked, don't continue
                if task_id in blocked:
                    return blocked
        # If we made it here, this task isn't blocked
        self.tasks[task_id]['status'] = TaskStatus.RUNNING
        return blocked

    # .......................
    def _process_incoming_tasks(self, job_config):
        """Process the job configuration to get tasks.

        Args:
            job_config (dict): A job configuration dictionary.
        """
        for task_config in job_config['tasks']:
            task_type = task_config['task']
            # Get the task definition so we know how to process
            tas_defn = ALL_TASKS[task_type]
            # - process parameters
            # - determine if outputs are unknown
            # - How to process outputs
            # - How to construct command
            task_id = task_config['identifier']
            self.tasks[task_id] = dict(
                status=TaskStatus.WAITING,
                unknown_outputs=unknown_outputs
            )
        raise NotImplementedError()

    # .......................
    def _run_next_makeflow(self):
        """Run the next makeflow for the job."""
        # Get next makeflow files
        next_mf_config, next_mf_log = self._get_next_makeflow()
        self.mf_files.append(next_mf_config)
        self.log_files.append(next_mf_log)

        # Build command and run it
        mf_cmd_list = self._build_makeflow_command(next_mf_config, next_mf_log)
        mf_proc = subprocess.Popen(mf_cmd_list, shell=True)
        while mf_proc.poll() is None:
            time.sleep(POLL_WAIT_TIME)

        # Process finished tasks
        self._unlock_tasks()

    # .......................
    def _tasks_left(self):
        """Get a boolean indicating if there are tasks left to compute.

        Returns:
            bool: Indication if there are tasks left to compute.
        """
        for task in self.tasks.values():
            if task['status'] in [TaskStatus.RUNNING, TaskStatus.WAITING]:
                return True
        return False

    # .......................
    def _unlock_tasks(self):
        """Unlock tasks that were in recently completed makeflow."""
        for task_id, task in self.tasks.items():
            if task['status'] == TaskStatus.RUNNING:
                task['status'] = TaskStatus.COMPLETE
                # Get task outputs if unknown
                if task['unknown_outputs']:
                    self._get_task_outputs(task_id)

    # .......................
    def compute(self):
        """Run the job computations.

        Returns:
            bool: Indication if the job completed successfully.
        """
        success = True
        try:
            while self._tasks_left():
                self._run_next_makeflow()
        except Exception as err:
            success = False
        return success

    # .......................
    def package_logs(self, output_filename):
        """Package logs and return a filename.

        Args:
            output_filename (str): Path to write packaged log files.
        """
        with zipfile.ZipFile(output_filename, mode='w') as zip_out:
            for log_filename in self.log_files:
                zip_out.write(log_filename)

    # .......................
    def package_outputs(self, output_filename):
        """Package outputs and return a filename.

        Args:
            output_filename (str): Path to write output package.

        Returns:
            str: A file path to the output package.
        """
        with zipfile.ZipFile(output_filename, mode='w') as zip_out:
            for root, dirs, files in os.walk(self.work_dir):
                for filename in files:
                    zip_out.write(filename)
