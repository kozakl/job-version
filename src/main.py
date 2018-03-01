import shotgun_api3
import json
import time
import glob
from pprint import pprint
import os
import sys
import os.path

sg = shotgun_api3.Shotgun('https://juicewro.shotgunstudio.com',
                          'job-version-daemon',
                          '3819096b36111394a58a2d7280059e1951eafcaba663b53ba2fe546cd3cab6f7')


def main():
    while True:
        update()
        time.sleep(15)


def update():
    jobs = filter(os.path.isfile, glob.glob('S:/jobs/*'))
    for job in jobs:
        data = json.load(open(job, 'r'))
        if os.path.isfile(data['movie']):
            try:
                version = create_version(data)
                upload_version(version)
                os.remove(job)
            except Exception as exception:
                print(exception)


def create_version(job_data):
    sg.config.sudo_as_login = job_data['userName']
    data = {
        'code': os.path.basename(job_data['movie']),
        'project': {
            'type': 'Project',
            'id': job_data['projectId']
        },
        'sg_path_to_movie': job_data['movie'],
    }
    return sg.create('Version', data)


def upload_version(version):
    sg.upload('Version', version['id'], version['sg_path_to_movie'], 'sg_uploaded_movie')


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    main()
