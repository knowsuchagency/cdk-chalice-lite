import json
import logging
import subprocess as sp
from pathlib import Path
from typing import *

from aws_cdk import core, aws_s3_assets


class Chalice(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        source_directory: Union[Path, str],
        stage_config: Optional[dict] = None,
        lambda_configs: Optional[dict] = None,
        environment: Optional[dict] = None,
        **kwargs,
    ):
        """
        Args:
            scope: cdk stack or construct
            id: identifier
            source_directory: the output directory of `chalice package` or the base path of the
                              chalice codebase
            environment: environment variables to apply across lambdas
            stage_config: stage-level configuration options i.e. `api_gateway_endpoint_type`
                          overwrites `dev`
            lambda_configs: lambda-level configurations, will be passed to `lambda_functions`
                            in `dev`
            **kwargs:
        """

        super().__init__(scope, id, **kwargs)

        stage_config = stage_config if stage_config is not None else {}

        lambda_configs = lambda_configs if lambda_configs is not None else {}

        environment = environment if environment is not None else {}

        source_path = Path(source_directory)

        if Path(source_path, "app.py").exists():

            logging.debug("assuming app has not been packaged")

            config_path = Path(source_path, ".chalice", "config.json")

            original_config_text = config_path.read_text()

            config_data = json.loads(original_config_text)

            config_data["stages"]["dev"].update(stage_config)

            if lambda_configs:

                config_data["stages"]["dev"]["lambda_functions"] = {
                    **config_data["stages"]["dev"].get("lambda_function", {}),
                    **lambda_configs,
                }

            updated_config = json.dumps(config_data, indent=2)

            logging.debug(updated_config)

            config_path.write_text(updated_config)

            output_dir = "chalice.out"

            sp.run(f"chalice package {output_dir}", shell=True, check=True)

            config_path.write_text(original_config_text)

            package_path = Path(output_dir)

        else:

            package_path = Path(source_directory)

        sam_path = Path(package_path, "sam.json")

        text = sam_path.read_text()

        self.template = json.loads(text)

        zip_path = Path(package_path, "deployment.zip")

        s3_asset = aws_s3_assets.Asset(
            self, "chalice-app-s3-object", path=zip_path.__fspath__()
        )

        for resource_name, resource in self.template["Resources"].items():

            if resource["Type"] == "AWS::Serverless::Function":

                properties = resource["Properties"]

                properties["CodeUri"] = {
                    "Bucket": s3_asset.s3_bucket_name,
                    "Key": s3_asset.s3_object_key,
                }

                properties.setdefault("Environment", {}).setdefault(
                    "Variables", {}
                ).update(environment)

        core.CfnInclude(self, "chalice-app", template=self.template)
