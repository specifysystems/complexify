"""Module containing task metadata for building makeflows and job configurations."""
import glob
import json
import os


TASK_META_DIR = '/app/task_definitions/'


ALL_TASKS_PUBLIC = {}
ALL_TASKS = {}
for fn in glob.glob(os.path.join(TASK_META_DIR, '*.json')):
    with open(fn, mode='rt') as in_json:
        task_info = json.load(in_json)
    ALL_TASKS_PUBLIC[os.path.splitext(os.path.basename(fn))[0]] = task_info
    ALL_TASKS[os.path.splitext(os.path.basename(fn))[0]] = task_info
