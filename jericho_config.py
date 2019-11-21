import os


class JerichoConfig():
    @property
    def src_bucket_name(self):
        return os.getenv("JER_SRC_BUCKET")

    @property
    def src_bucket_key_id(self):
        return os.getenv("JER_SRC_KEY_ID", os.getenv("AWS_ACCESS_KEY_ID"))

    @property
    def src_bucket_key(self):
        return os.getenv("JER_SRC_KEY", os.getenv("AWS_SECRET_ACCESS_KEY"))

    @property
    def out_region(self):
        return os.getenv("JER_OUT_REGION", os.getenv("AWS_REGION"))

    @property
    def out_bucket_name(self):
        return os.getenv("JER_OUT_BUCKET")

    @property
    def out_bucket_key_id(self):
        return os.getenv("JER_OUT_KEY_ID", os.getenv("AWS_ACCESS_KEY_ID"))

    @property
    def out_bucket_key(self):
        return os.getenv("JER_OUT_KEY", os.getenv("AWS_SECRET_ACCESS_KEY"))

    @property
    def use_slack(self):
        enable = os.getenv("JER_ENABLE_SLACK")
        return (enable is None or enable.lower() == "true") and os.getenv("JER_SLACK_ENDPOINT") is not None

    @property
    def slack_endpoint(self):
        return os.getenv("JER_SLACK_ENDPOINT")

    @property
    def use_system_chrome(self):
        return os.getenv("JER_USE_SYSTEM_CHROME", os.getenv("AWS_EXECUTION_ENV") is None)

    @property
    def function_root(self):
        return os.getenv("LAMBDA_TASK_ROOT", os.path.dirname(__file__))

    @property
    def working_dir(self):
        return "/tmp/"

    @property
    def tests_root(self):
        return self.working_dir + "tests/"

    @property
    def chromium_dir(self):
        return self.working_dir + "chrome/"


config = JerichoConfig()