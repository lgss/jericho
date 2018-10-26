import boto3
import zipfile
import os
import sys
import jericho_config


def extract_s3_library(bucket, key):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).download_file(key, "/tmp/" + key)


def setup(argv):
    jericho_config.load_config(argv)
    bucket = jericho_config.cfg().get("AWS", "BucketName")
    extract_s3_library(bucket, "chrome.zip")
    zipfile.ZipFile("/tmp/chrome.zip").extractall("/tmp/chrome/")
    os.chmod("/tmp/chrome/chromedriver", 0o777)
    os.chmod("/tmp/chrome/chrome", 0o777)
    extract_s3_library(bucket, "lib.zip")
    sys.path.insert(0, "/tmp/lib.zip")


def lambda_handler(event, context):
    setup("")
    import orchestration
    return orchestration.lambda_handler(event, context)
