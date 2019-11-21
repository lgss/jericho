import boto3
import zipfile
import os
import sys
import json
from jericho_config import config


def setup():
    s3 = boto3.resource(
        's3')

    s3.Bucket(config.src_bucket_name).download_file("chrome.zip", config.working_dir + "chrome.zip")
    s3.Bucket(config.src_bucket_name).download_file("lib.zip", config.working_dir + "lib.zip")

    zipfile.ZipFile("/tmp/chrome.zip").extractall("/tmp/chrome/")
    os.chmod(config.chromium_dir + "chromedriver", 0o777)
    os.chmod(config.chromium_dir + "chrome", 0o777)

    sys.path.insert(0, "/tmp/lib.zip")


def lambda_handler(event, context):
    setup()
    import orchestration
    if isinstance(event, str):
        event = json.loads(event)
    return orchestration.lambda_handler(event, context)
