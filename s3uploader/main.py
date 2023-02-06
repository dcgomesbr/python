#!/usr/bin/env python
import sys
from pathlib import Path
from WatchdogWrapper import OnMyWatch
import subprocess

if __name__ == '__main__':
    bucket_name = sys.argv[1]
    observed_file = sys.argv[2]

    if not bucket_name or not observed_file:
        print("Both bucket name and file name (including path) must be provided")
        exit(-1)

    # try to figure out where aws cli is
    try:
        result = subprocess.check_output(
            ['/bin/sh', '-c', 'which aws']
        )
    except BaseException as e:
        print("Execution failed, couldn't find aws cli:", e, file=sys.stderr)
        exit(-1)

    aws_cli_path = str(Path(result.decode("utf-8")).parent)

    print('Watching ' + observed_file + '. Hit CTRL-C to end the execution.')
    watch = OnMyWatch(observed_file,
                      bucket_name,
                      'daniel',
                      aws_cli_path)
    watch.run()
