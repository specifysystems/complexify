"""Complexify API Flask App."""
from flask import Blueprint, jsonify, request, send_file

from complexify.common.datatypes import ALL_DATA_TYPES
from complexify.common.tasks import ALL_TASKS_PUBLIC
from complexify.web.models import get_uploads_list, Job, Upload


bp = Blueprint('complexify', __name__, url_prefix='/api')


# .....................................................................................
@bp.route('/datatype/', methods=['GET'])
def datatype_list():
    """Get a list of the data types used in complexify.

    Returns:
        list of dict: A list of dictionaries describing available data types.
    """
    return jsonify(list(ALL_DATA_TYPES.values()))


# .....................................................................................
@bp.route('/datatype/<string:data_type_identifier>', methods=['GET'])
def datatype_info(data_type_identifier):
    """Get information about a specific data type.

    Returns:
        dict: A dictionary of information about a data type.
    """
    return ALL_DATA_TYPES[data_type_identifier]


# .....................................................................................
@bp.route('/job', methods=['POST'])
def job_post():
    """POST a new job for computation."""
    job = Job.create_from_config(request.get_json(force=True))
    return job.get_metadata()


# .....................................................................................
@bp.route('/job/lock', methods=['POST'])
def job_lock():
    """Lock a job for computation."""
    job = Job.from_lock()
    return job.get_metadata()


# .....................................................................................
@bp.route('/job/<string:job_identifier>', methods=['GET'])
def job_get(job_identifer):
    """Get job metadata."""
    job = Job.from_identifier(job_identifer)
    return job.get_metadata()


# .....................................................................................
@bp.route('/job/<string:job_identifier>/config', methods=['GET'])
def job_get_config(job_identifer):
    """Get job configuration."""
    job = Job.from_identifier(job_identifer)
    return job.get_configuration()


# .....................................................................................
@bp.route('/job/<string:job_identifier>/download', methods=['GET'])
def job_download(job_identifer):
    """Get job download."""
    job = Job.from_identifier(job_identifer)
    download_filename = job.get_download_path()
    send_file(download_filename, as_attachment=True)


# .....................................................................................
@bp.route('/job/<string:job_identifier>/report', methods=['GET'])
def job_get_report(job_identifer):
    """Get job report."""
    job = Job.from_identifier(job_identifer)
    return job.get_report()


# .....................................................................................
@bp.route('/job/<string:job_identifier>/status', methods=['GET'])
def job_get_status(job_identifier):
    """Get job status."""
    job = Job.from_identifier(job_identifer)
    return job.get_metadata()


# .....................................................................................
@bp.route('/job/<string:job_identifier>/status/<int:new_status>', methods=['PUT'])
def job_set_status(job_identifier, new_status):
    """Set job status."""
    job = Job.from_identifier(job_identifer)
    job.set_status(new_status)
    return job.get_metadata()


# .....................................................................................
@bp.route('/task/', methods=['GET'])
def task_list():
    """Get a list of the available tasks in complexify.

    Returns:
        list of dict: A list of dictionaries describing available tasks.
    """
    return jsonify(list(ALL_TASKS_PUBLIC.values()))


# .....................................................................................
@bp.route('/task/<string:task_identifier>', methods=['GET'])
def task_info(task_identifier):
    """Get information about a specific task.

    Returns:
        dict: A dictionary of information about a specific task.
    """
    return ALL_TASKS_PUBLIC[task_identifier]


# .....................................................................................
@bp.route('/upload', methods=['GET'])
def upload_list():
    """List available upload files."""
    return get_uploads_list()


# .....................................................................................
@bp.route('/upload', methods=['POST'])
def upload_post():
    """Upload a new file to be used in computations."""
    name = request.args['name']
    data_type = request.args['data_type']
    upload = Upload.from_post(name, data_type, request.data)
    return upload.get_metadata()


# .....................................................................................
@bp.route('/upload/<string:upload_identifier>', methods=['GET', 'PUT'])
def upload_get_put(upload_identifier):
    """GET or update an uploaded file."""
    upload = Upload.from_identifier(upload_identifier)

    if request.method == 'PUT':
        upload.set_content(request.data)

    return upload.get_metadata()


# .....................................................................................
@bp.route('/upload/<string:upload_identifier>/download', methods=['GET'])
def upload_download(upload_identifier):
    """Download a file previously uploaded."""
    upload = Upload.from_identifier(upload_identifier)
    send_file(uploade.get_download_path(), as_attachment=True)
