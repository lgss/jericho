# Jericho Automated Test harness
The software is written in Python 3.x, uses Selenium, and runs on AWS Lambda. To run properly on Lambda, it uses [Lambdium](https://github.com/smithclay/lambdium).

## Setup
 1. Setup a new S3 bucket to contain chrome and library files as well as receiving testing output. Insert these files into the root of the bucket, they need to be publicly accessible:
	 - Lambdium (chrome + chromedriver), in a zip file named chrome.zip
	 - The python modules Selenium, HtmlTestRunner, jinja2, markupsafe, and urllib3 in a zip file named lib.zip
2. Create a new AWS Lambda function that uses Python 3.6, upload the project files, and set the Handler to `bootstrap.lambda_handler`
3. Configure the environmental variables
## Environmental Variables
| Variable Name           | Description                                                                                                                |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------|
| `JER_SRC_BUCKET`        | (_Mandatory_) Name of the source S3 bucket that contains Lambdium and the Jericho library files.                           |
| `JER_SRC_KEY_ID`        | Source S3 bucket access key ID. Defaults to the Lambda function credentials.                                               |
| `JER_SRC_KEY`           | Source S3 bucket access key. Defaults to the Lambda function credentials.                                                  |
| `JER_OUT_REGION`        | Output S3 bucket region name, required for the Slack integration to work. Defaults to the Lambda function's region.        |
| `JER_OUT_BUCKET`        | (_Mandatory_) Name of the output S3 bucket where test reports will be saved.                                               |
| `JER_OUT_KEY_ID`        | Output S3 bucket access key ID. Defaults to the Lambda function credentials.                                               |
| `JER_OUT_KEY`           | Output S3 bucket access key. Defaults to the Lambda function credentials.                                                  |
| `JER_ENABLE_SLACK`      | Enable the Slack integration, also requires the Slack endpoint to be set. Defaults to True.                                |
| `JER_SLACK_ENDPOINT`    | The Slack Incoming Webhooks endpoint.                                                                                      |
| `JER_USE_SYSTEM_CHROME` | Use this setting in the debugger to use the system installed Chrome. Enabling this option in Lambda will cause it to fail. |
