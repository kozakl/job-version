import shutil
import os

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
