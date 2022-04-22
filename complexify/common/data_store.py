"""Module containing functions for operating with a data store."""
import sqlite3
from flask import g

DATABASE_FILENAME = '/db/complexify.db'

# Note: Much of the database setup with flask is taken from:
#    https://flask.palletsprojects.com/en/2.1.x/patterns/sqlite3/
# .....................................................................................
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_FILENAME)
        db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def _get_filename(object_type, identifier, extension):
    base_dir = UPLOAD_DIR
    if object_type.lower() == 'job':
        base_dir = JOB_DIR
    return os.path.join(base_dir, f'{identifier}{extension}')


def job_get(job_identifier):
    return query_db(
        'SELECT * FROM jobs WHERE job_identifier = ?', [job_identifier], one=True
    )
    
def job_get_configuration(job_identifier):
    return _get_filename('job', job_identifier, '_config.json')

def job_get_download_path(job_identifier):
    return _get_filename('job', job_identifier, '_download.zip')

def job_get_for_computation():
    con = get_db()
    con.isolation_level = 'EXCLUSIVE'
    con.execute('BEGIN EXCLUSIVE')
    cur = con.execute('SELECT * FROM job WHERE status = ? LIMIT 1', [JOB_READY])
    job_value = cur.fetchall()
    cur.close()
    con.commit()
    con.close()

def job_get_report(job_identifier):
    return _get_filename('job', job_identifier, '_report.json')

def job_post(job_configuration):
    pass

def upload_get(upload_identifier):
    return query_db(
        'SELECT * FROM uploads WHERE upload_identifier = ?',
        [upload_identifier],
        one=True,
    )

def upload_list():
    return query_db('SELECT * FROM uploads')
