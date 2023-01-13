import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket("sm589-extra-bucket",
    acl="private",
)