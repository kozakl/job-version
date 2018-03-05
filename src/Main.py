import json
import logging
import sys
import os
import time
import shotgun_api3

from glob import glob
from os import path
from watchdog.observers import Observer
from events import JobEventHandler
from utils import JobUtil
from utils import ShotgunUtil


class Main:

    def __init__(self):
        self.shotgun = shotgun_api3.Shotgun('https://juicewro.shotgunstudio.com',
                                            'job-version-daemon',
                                            '3819096b36111394a58a2d7280059e1951eafcaba663b53ba2fe546cd3cab6f7')
        self.total_jobs = JobUtil.get_total_jobs()

        logging.basicConfig(
            filename='S:/log/job-version.log',
            format='%(asctime)s %(levelname)-6s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG
        )

        job_event_handler = JobEventHandler()
        job_event_handler.on_created = self.on_created_job
        job_event_handler.on_deleted = self.on_deleted_job
        observer = Observer()
        observer.schedule(job_event_handler, 'S:/jobs')
        observer.start()

        try:
            while True:
                if self.total_jobs > 0:
                    self.check_jobs()
                time.sleep(10)
        except KeyboardInterrupt:
            observer.stop()

    def on_created_job(self, event):
        self.total_jobs = JobUtil.get_total_jobs()
        logging.info('Job %s - created, total jobs %s', path.basename(event.src_path), str(self.total_jobs))

    def on_deleted_job(self, event):
        self.total_jobs = JobUtil.get_total_jobs()
        logging.info('Job %s - removed, total jobs %s', path.basename(event.src_path), str(self.total_jobs))

    def check_jobs(self):
        jobs = filter(path.isfile, glob('S:/jobs/*'))
        for job in jobs:
            data = json.load(open(job, 'r'))
            if JobUtil.is_expired(data, 5):
                JobUtil.move_to_log(job)
                logging.info('Job %s - expired and move to logs', path.basename(job))
            elif path.isfile(data['movie']):
                try:
                    logging.info('Job %s - movie exist', path.basename(job))

                    version = ShotgunUtil.create_version(self.shotgun, data)
                    logging.info('Job %s - version %s created', path.basename(job), version['id'])

                    entity = ShotgunUtil.upload_version(self.shotgun, version)
                    logging.info('Job %s - entity %s uploaded', path.basename(job), entity)

                    JobUtil.move_to_log(job)
                    logging.info('Job %s - complete and move to logs', path.basename(job))
                except Exception as exception:
                    print(exception)


if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stderr = open('S:/log/job-version-err.log', 'w')
    Main()
