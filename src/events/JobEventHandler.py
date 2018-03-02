import logging

from os.path import basename
from watchdog.events import FileSystemEventHandler


class JobEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.debug('Job created: %s', basename(event.src_path))
