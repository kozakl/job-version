import shotgun_api3
import json
import time
import glob
from pprint import pprint
import os
import sys

sg = shotgun_api3.Shotgun('https://juicewro.shotgunstudio.com',
                          'job-version-daemon',
                          '3819096b36111394a58a2d7280059e1951eafcaba663b53ba2fe546cd3cab6f7')


def main():
    while True:
        update()
        time.sleep(15)


def update():
    print('Update')

    jobs = filter(os.path.isfile, glob.glob('S:/jobs/*'))
    for job in jobs:
        data = json.load(open(job, 'r'))
        version = create_version(data)
        print upload_version(version)


def create_version(data):
    sg.config.sudo_as_login = data['userName']
    datax = {
        'code': 'Test.mp4',
        'project': {
            'type': 'Project',
            'id': 127
        },
        'user': {'type': 'HumanUser', 'id': 87},
        'updated_by': {'type': 'HumanUser', 'id': 87},
        'sg_path_to_movie': 'W:/0000_sg_development/render/Draft/shotgun_h264.mov',
    }
    return sg.create('Version', datax)


def upload_version(version):
    sg.upload('Version', version['id'], 'W:/0000_sg_development/render/Draft/shotgun_h264.mov', 'sg_uploaded_movie')


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    main()
