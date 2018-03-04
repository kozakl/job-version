import shutil
import os

from datetime import datetime
from glob import glob
from os import path


class JobUtil:

    def __init__(self):
        pass

    @staticmethod
    def get_total_jobs():
        return len(filter(path.isfile, glob('S:/jobs/*')))

    @staticmethod
    def move_to_log(job):
        if not path.exists('S:/log/jobs'):
            os.makedirs('S:/log/jobs')
        shutil.move(job, 'S:/log/jobs/' + path.basename(job))

    @staticmethod
    def is_expired(job_data, hours):
        date = datetime.strptime(job_data['date'], '%Y-%m-%d %H:%M')
        diff = datetime.now() - date
        return divmod(diff.seconds, 3600)[0] > hours
