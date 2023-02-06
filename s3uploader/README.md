# Requirements:
 - aws cli v2 (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
 - pipenv (https://pypi.org/project/pipenv/)
 - An AWS profile configured with the access key and secret, the code defaults to `daniel`, e.g.:

   ``` aws configure --profile daniel```

The code uses aws s3 sync to push files to S3. Python Watchdog library is used, and it doesn't work well with network
mapped filesystems such as NFS. Such volumes need polling instead of Kernel calls supported solutions.

# Running:
## Install Python dependencies:
```
pipenv install
```

## Run:
```
pipenv run python main.py bucket-name file-name
```

A shell scrip wrapper is named `s3uploader`, provided for your convenience.

# Why on Earth didn't you use boto3??
I was expecting it to be smarter about the file contents but, guess what,
it's not. So, last minute, I added the MD5 hash check there and I didn't want to put more effort in it.