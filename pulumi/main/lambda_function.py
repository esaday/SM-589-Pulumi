import pulumi
import pulumi_aws as aws
import hashlib
from base64 import b64encode

from main.iam import lambda_exec_role
from main.dynamo import dynamodb_table
from main.package_lambda import install_lambda_deps, copy_files, copy_gcp_creds


def get_file_hash(bytes):
    return b64encode(hashlib.sha256(bytes).digest()).decode()


lambda_function = aws.lambda_.Function(
    "process-dynamodb-records",
    code=pulumi.FileArchive("main/lambda/package/"),
    handler="handler.handler",
    role=lambda_exec_role.arn,
    runtime="python3.8",
    source_code_hash=get_file_hash(
        open('main/lambda/src/handler.py', 'rb').read()),
    opts=pulumi.ResourceOptions(depends_on=[
        install_lambda_deps,
        copy_files,
        copy_gcp_creds
    ],
    ),
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "GOOGLE_APPLICATION_CREDENTIALS": "gcp_creds.json",
        },
    ),
)

log_event_mapping = aws.lambda_.EventSourceMapping("log_event_mapping",
    event_source_arn=dynamodb_table.stream_arn,
    function_name=lambda_function.arn,
    starting_position="LATEST")