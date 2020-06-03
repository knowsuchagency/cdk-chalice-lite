from aws_cdk import core

from cdk_chalice_lite import Chalice


class TestChalice(core.Stack):

    def __init__(self, scope, id, source_dir, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.chalice = Chalice(
            self,
            "derp",
            source_dir,
            lambda_configs={"sqs_handler": {"lambda_timeout": 30}},
        )


app = core.App()

testing_chalice = TestChalice(app, "testing-chalice-1", ".")

# testing_chalice_2 = TestChalice(app, "testing-chalice-2", "chalice.out")


app.synth()
