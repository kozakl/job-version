import shotgun_api3
from pprint import pprint


def main():
    sg = shotgun_api3.Shotgun('https://juicewro.shotgunstudio.com',
                              'job-version-daemon',
                              '3819096b36111394a58a2d7280059e1951eafcaba663b53ba2fe546cd3cab6f7')

    sg.config.sudo_as_login = 't.dyrdula'
    data = {
        'code': 'Test.mp4',
        'project': {
            'type': 'Project',
            'id': 127
        },
        'user': {'type': 'HumanUser', 'id': 87},
        'updated_by': {'type': 'HumanUser', 'id': 87},
        'sg_path_to_movie': '../Test.mp4',
    }

    version = sg.create('Version', data)

    sg.config.sudo_as_login = 'kozak'
    data = {
        'code': 'Test.mp4',
        'project': {
            'type': 'Project',
            'id': 127
        },
        'user': {'type': 'HumanUser', 'id': 87},
        'updated_by': {'type': 'HumanUser', 'id': 87},
        'sg_path_to_movie': '../Test.mp4',
    }

    version = sg.create('Version', data)
    #sg.upload('Version', version['id'], '../Test.mp4', 'sg_uploaded_movie')
    pprint( version )
    pprint(sg.config)


if __name__ == "__main__":
    main()
