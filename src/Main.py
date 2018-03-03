import shotgun_api3
import json
import time
import glob
import os
import sys
import os.path
import logging
from watchdog.observers import Observer
from events import JobEventHandler
from os.path import basename
from utils import ShotgunUtil


class Main:

    def __init__(self):
        self.shotgun = shotgun_api3.Shotgun('https://juicewro.shotgunstudio.com',
                                            'job-version-daemon',
                                            '3819096b36111394a58a2d7280059e1951eafcaba663b53ba2fe546cd3cab6f7')
        self.jobs_count = 10

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
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

    def on_created_job(self, event):
        self.jobs_count = len(filter(os.path.isfile, glob.glob('S:/jobs/*')))
        self.check_jobs()

        logging.info('Job %s - created, total jobs %s', basename(event.src_path), str(self.jobs_count))

    def on_deleted_job(self, event):
        self.jobs_count = len(filter(os.path.isfile, glob.glob('S:/jobs/*')))

        logging.info('Job %s - removed, total jobs %s', basename(event.src_path), str(self.jobs_count))

    def check_jobs(self):
        jobs = filter(os.path.isfile, glob.glob('S:/jobs/*'))
        for job in jobs:
            data = json.load(open(job, 'r'))
            if os.path.isfile(data['movie']):
                try:
                    logging.info('Job %s - movie exist', basename(job))

                    version = ShotgunUtil.create_version(self.shotgun, data)
                    logging.info('Job %s - version %s created', basename(job), version['id'])

                    entity = ShotgunUtil.upload_version(self.shotgun, version)
                    logging.info('Job %s - entity %s uploaded', basename(job), entity)

                    os.remove(job)
                    logging.info('Job %s - removed', basename(job))
                except Exception as exception:
                    print(exception)


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    Main()
