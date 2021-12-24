from os import path


class ShotgunUtil:

    def __init__(self):
        pass

    @staticmethod
    def create_version(shotgun, job_data):
        data = {
            'code': path.basename(job_data['movie']),
            'project': {
                'type': 'Project',
                'id': job_data['projectId']
            },
            'sg_path_to_movie': job_data['movie']
        }
        shotgun.config.sudo_as_login = job_data['userName']
        return shotgun.create('Version', data)

    @staticmethod
    def upload_version(shotgun, version):
        return shotgun.upload('Version', version['id'], version['sg_path_to_movie'], 'sg_uploaded_movie')
