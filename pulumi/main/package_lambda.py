import pulumi
from pulumi_command import local
import hashlib
import json
from base64 import b64encode

config = pulumi.Config()
creds_path = config.require('gcp_creds_path')


def get_file_hash(bytes):
    return b64encode(hashlib.sha256(bytes).digest()).decode()


install_lambda_deps = local.Command("install reqs",
                                    triggers=[get_file_hash(
                                        open('main/lambda/requirements.txt', 'rb').read())],
                                    create="pip install -r main/lambda/requirements.txt  -t main/lambda/package/"
                                    )

copy_files = local.Command("Copy Files",
                           triggers=[get_file_hash(
                               open('main/lambda/src/handler.py', 'rb').read())],
                           create="cp -r main/lambda/src/* main/lambda/package/"
                           )

copy_gcp_creds = local.Command("Copy GCP Creds",
                               create=f"cp {creds_path} main/lambda/package/gcp_creds.json"
                               )
