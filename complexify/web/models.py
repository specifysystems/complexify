"""Complexify data models for API."""
import complexify.common.data_store as data_store


# .....................................................................................
class Job:
    """Class representing computational job requests."""
    # .......................
    def __init__(
        self,
        job_identifier=None,
        status=None,
        user=None,
        create_time=None,
        last_modified_time=None,
    ):
        self.identifier = job_identifier
        self.status = status
        self.user = user
        self.create_time = create_time
        self.last_modified_time = last_modified_time

    # .......................
    @classmethod
    def create_from_configuration(cls, job_configuration):
        return cls.from_record(data_store.job_post(job_configuration))

    # .......................
    @classmethod
    def from_identifier(cls, job_identifier):
        return cls.from_record(data_store.job_get(job_identifier))

    # .......................
    @classmethod
    def from_lock(cls):
        """Get a job to compute."""
        return cls.from_record(data_store.job_get_for_computation())

    # .......................
    @classmethod
    def from_record(cls, job_record):
        return cls(**job_record)

    # .......................
    def get_configuration(self):
        with open(
            data_store.job_get_configuration(self.identifier), mode='rt'
        ) as in_json:
            return json.load(in_json)

    # .......................
    def get_download_path(self):
        return data_store.job_get_download_path(self.identifier)

    # .......................
    def get_metadata(self):
        job_metadata = {
            'identifier': self.identifier,
            'status': self.status,
            'user': self.user,
            'creation_time': self.create_time,
            'last_modified': self.last_modified_time,
        }
        return job_metadata

    # .......................
    def get_report(self):
        with open(data_store.job_get_report(self.identifier), mode='rt') as in_json:
            return json.load(in_json)


# .....................................................................................
class Upload:
    # .......................
    def __init__(self, ):
        pass

    # .......................
    @classmethod
    def from_identifier(cls, upload_identifier):
        return cls.from_record(data_store.upload_get(upload_identifier))

    # .......................
    @classmethod
    def from_record(cls, upload_record):
        return cls.__init__(**upload_record)


# .....................................................................................
def get_uploads_list():
    """Get a list of the uploaded data files."""
    return [
        Upload.from_record(upload_record) for upload_record in data_store.upload_list()
    ]
