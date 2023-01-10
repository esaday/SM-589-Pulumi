import pulumi
import pulumi_aws as aws
import json

from main.dynamo import dynamodb_table


def generate_inline_dynamo_policy(dynamodb_table_arn):
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": ["logs:*"],
                    "Effect": "Allow",
                    "Resource": ["arn:aws:logs:*:*:*"]
                },
                {
                    "Action": ["dynamodb:BatchGetItem",
                               "dynamodb:GetItem",
                               "dynamodb:GetRecords",
                               "dynamodb:Scan",
                               "dynamodb:Query",
                               "dynamodb:GetShardIterator",
                               "dynamodb:DescribeStream",
                               "dynamodb:ListStreams"],
                    "Effect": "Allow",
                    "Resource": [
                        dynamodb_table_arn,
                        f"{dynamodb_table_arn}/*"
                    ]
                }
            ]
        }
    )


lambda_exec_role = aws.iam.Role(
    "lambda_execution_role",
    assume_role_policy="""{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
""",
    inline_policies=[
        aws.iam.RoleInlinePolicyArgs(
            name="DynamoAccess",
            policy=dynamodb_table.arn.apply(
                lambda arn: generate_inline_dynamo_policy(arn)
            ),
        )
    ],
)
