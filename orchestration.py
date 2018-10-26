import unittest
import boto3
import sys
import json
import io
import datetime
import time
import HtmlTestRunner
import urllib3
import jericho_config
import os


def run_html_tests():
    tests = unittest.TestLoader().discover('tests', "testL*.py")
    os.chdir('/tmp') #HtmlTestRunner sucks and relies on cwd but AWS Lambda only allows writing to /tmp/
    runner = HtmlTestRunner.HTMLTestRunner("", report_title="Jericho Test Report", template="/var/task/report_template.html")
    res = runner.run(tests)
    return res


def lambda_handler(event, context):
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
        jericho_config.cfg().get("AWS", "Region"),
        jericho_config.cfg().get("AWS", "BucketName"))
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
                "footer": "Jericho Automated Tests",
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

    if jericho_config.cfg().getboolean("Slack", "Enable", fallback=False):
        http = urllib3.PoolManager()
        r = http.request("POST", jericho_config.cfg().get("Slack", "WebhookEndpoint"),
                         headers={'Content-Type': 'application/json'},
                         body=body_data)
    return body_data


def save_test_log():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=jericho_config.cfg().get("AWS", "AccessKeyID"),
        aws_secret_access_key=jericho_config.cfg().get("AWS", "AccessKeySecret"))
    key = datetime.datetime.now().strftime("output/%Y-%m/test %Y-%m-%d %H%M.html")
    dir_list = os.listdir("/tmp/reports/") # this is a nasty hack to deal with the crappy HTMLTestRunner component
    try:
        with open('/tmp/reports/' + dir_list[0], "r", encoding='utf-8') as f:
            body_data = f.read()
        s3_client.put_object(Body=body_data, Bucket=jericho_config.cfg().get("AWS", "BucketName"), Key=key, ACL='public-read', ContentType="text/html")
    finally:
        os.remove('/tmp/reports/' + dir_list[0])
    return key


if __name__ == '__main__':
    jericho_config.load_config(sys.argv[1:])
    tests = unittest.TestLoader().discover('tests', "test*.py")
    runner = HtmlTestRunner.HTMLTestRunner("tmp", report_title="test_report", template="./report_template.html")
    res = runner.run(tests)
    print(res)
