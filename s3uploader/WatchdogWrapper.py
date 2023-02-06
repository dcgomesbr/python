import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import hashlib


class OnMyWatch:
    def __init__(self, fullpath, bucket, profile, awscli):
        self.fullPath = Path(fullpath)
        self.bucket = bucket
        self.watchDirectory = str(self.fullPath.parent)
        self.watchFilename = self.fullPath.name
        self.awsProfile = profile
        self.awscliPath = awscli

    def run(self):
        event_handler = CustomEventHandler(filename=self.watchFilename, bucket=self.bucket, pattern=str(self.fullPath),
                                           profile=self.awsProfile, awscli_path=self.awscliPath)

        observer = Observer()
        observer.schedule(event_handler, self.watchDirectory)
        observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
            print("Observer Stopped")

        observer.join()


class CustomEventHandler(PatternMatchingEventHandler):
    def __init__(self, filename, bucket, pattern, profile, awscli_path, **kwds):
        self.bucket = bucket
        self.file = filename
        self.profile = profile
        self.awscliPath = awscli_path
        self.fileHash = FileHash.md5(filename)  # to detect content changes
        super(CustomEventHandler, self).__init__(patterns=[pattern], ignore_directories=True, **kwds)

    # file creation also leads to a subsequent file modification
    # therefore, no need to trap on_create
    def on_modified(self, event):
        print("Watchdog received modified event - % s." % event.src_path)
        new_file_hash = FileHash.md5(self.file)
        if self.fileHash == new_file_hash:
            print('Change detected but contents has not changed, skipping upload')
        else:
            self.fileHash = new_file_hash  # update stored hash
            result = subprocess.check_output(
                ['/bin/sh', '-c', 'aws s3 sync . s3://' + self.bucket + ' --exclude "*" --include "' + self.file +
                 '"'],
                env={
                    'AWS_PROFILE': self.profile,
                    'PATH': self.awscliPath  # for security reasons, keep the PATH really strict
                }
            )
            print(result.decode("utf-8"))


class FileHash:
    @staticmethod
    def md5(file):
        hash_md5 = hashlib.md5()

        path = Path(file)
        if not path.is_file():
            return ""

        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
