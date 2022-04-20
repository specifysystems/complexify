"""Complexify API Flask App."""
from flask import Blueprint, jsonify, request

from complexify.common.datatypes import ALL_DATA_TYPES


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
#@bp.route('/job', methods=['POST'])
# .....................................................................................
#@bp.route('/job/<string:job_identifier>', methods=['GET'])
# .....................................................................................
#@bp.route('/job/<string:job_identifier>/config', methods=['GET'])
# .....................................................................................
#@bp.route('/job/<string:job_identifier>/download', methods=['GET'])
# .....................................................................................
#@bp.route('/job/<string:job_identifier>/report', methods=['GET'])
# .....................................................................................
#@bp.route('/job/<string:job_identifier>/status', methods=['GET', 'PUT'])
# .....................................................................................
#@bp.route('/task', methods=['GET'])
# .....................................................................................
#@bp.route('/task/<string:task_identifier>', methods=['GET'])
# .....................................................................................
#@bp.route('/upload', methods=['GET', 'POST'])
# .....................................................................................
#@bp.route('/upload/<string:upload_identifier>', methods=['GET', 'PUT'])


"""
def task_type_list
def task_get_info
def data_type_list
def data_type_info
def upload_data
def upload_list
def job_post():
def job_get_status
def job_download
def job_get_report
def job_config_get
def job_config_update
"""

