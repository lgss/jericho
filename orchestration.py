import unittest
import boto3
import json
import datetime
import time
import HtmlTestRunner
import urllib3
from jericho_config import config
import os
import zipfile
import test_bootstrap
import shutil


def run_html_tests():
    tests = unittest.TestLoader().discover(config.tests_root)
    os.chdir(config.working_dir) # HtmlTestRunner is annoying; it relies on cwd but AWS Lambda only allows writing to /tmp/
    runner = HtmlTestRunner.HTMLTestRunner("", report_title="Jericho Test Report", template= config.function_root + "/report_template.html")
    res = runner.run(tests)
    return res


def lambda_handler(event, context):
    res_dst = os.path.join(config.working_dir, "resource.zip")
    t = event.resource.type
    if t == "url":
        http = urllib3.PoolManager()
        with http.request('GET', event.resource.location, preload_content=False) as resp, open(res_dst, 'wb') as out_file:
            shutil.copyfileobj(resp, out_file)
    elif t == "s3":
        s3 = boto3.resource(
            's3',
            aws_access_key_id=event.resource.key_id,
            aws_secret_access_key=event.resource.key)
        s3.Bucket(event.resource.bucket).download_file(event.resource.file_key, res_dst)
    else:
        raise Exception("Invalid resource type")

    zipfile.ZipFile(res_dst).extractall(path=config.tests_root)

    test_bootstrap.setenv(event.environment)
    tests_result = run_html_tests()

    path = save_test_log()
    slack = do_slack_message(tests_result, path)

    return {
        "succeeded": len(tests_result.successes),
        "failed": len(tests_result.failures),
        "errors": len(tests_result.errors),
        "slack": slack}


def do_slack_message(results, path):
    root = "https://s3.{}.amazonaws.com/{}/".format(
        config.out_region,
        config.out_bucket_name)
    url = root + path.replace(" ", "+")
    all_good = len(results.failures) == 0 and len(results.errors) == 0
    if all_good:
        msg = "All tests have finished successfully."
        color = "good"
        errs = ""
        thumb = root + "success.png"
    else:
        msg = "There are failing tests!"
        color = "danger"
        mapf = lambda x: "Failed: " + x[0].test_id
        errs = "\n".join(list(map(mapf, results.failures)) + list(map(mapf, results.errors)))
        thumb = root + "failed.png"

    body_data = json.dumps({
        "text": msg,
        "attachments": [
            {
                "color": color,
                "fallback": "View the test report at " + url,
                "thumb_url": thumb,
                "text": errs,
                "footer": "Jericho Automated Tests by LGSS Digital",
                "ts": int(time.mktime(datetime.datetime.now().timetuple())),
                "actions": [
                    {
                        "type": "button",
                        "text": "View test report",
                        "url": url
                    }
                ]
            }
        ]
    })

    if config.use_slack:
        http = urllib3.PoolManager()
        r = http.request("POST", config.slack_endpoint,
                         headers={'Content-Type': 'application/json'},
                         body=body_data)
    return body_data


def save_test_log():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config.out_bucket_key_id,
        aws_secret_access_key=config.out_bucket_key)
    key = datetime.datetime.now().strftime("output/%Y-%m/test %Y-%m-%d %H%M.html")
    dir_list = os.listdir(config.working_dir + "reports/") # this is a nasty hack to deal with the HTMLTestRunner component
    try:
        with open(config.working_dir + 'reports/' + dir_list[0], "r", encoding='utf-8') as f:
            body_data = f.read()

        if config.out_bucket_name:
            s3_client.put_object(Body=body_data, Bucket=config.out_bucket_name, Key=key, ACL='public-read', ContentType="text/html")
    finally:
        os.remove(config.working_dir + 'reports/' + dir_list[0])
    return key


def build_test_suite(root, configfile):
    return 1


if __name__ == '__main__':
    lambda_handler(type('obj', (object,), {
        "resource": type('obj', (object,), {
            "type": "url",
            "location": "https://s3.eu-west-2.amazonaws.com/jerichotest/NoCC.zip"
        }),
        "environment": {

        }
    }), None)
    #tests = unittest.TestLoader().discover(config.tests_root, "test*.py")
    #runner = HtmlTestRunner.HTMLTestRunner(config.working_dir, report_title="test_report", template="./report_template.html")
    #res = runner.run(tests)
    #print(res)
