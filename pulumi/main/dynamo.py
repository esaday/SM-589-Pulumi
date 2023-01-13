import pulumi
import pulumi_aws as aws

dynamodb_table = aws.dynamodb.Table("lambda-dynamodb-stream",
                                    billing_mode="PAY_PER_REQUEST",
                                    hash_key="id",
                                    stream_enabled=True,
                                    stream_view_type="NEW_IMAGE",
                                    attributes=[{
                                        "name": "id",
                                        "type": "S",
                                    }])

extra_dynamodb_table = aws.dynamodb.Table("extra_table",
                                    billing_mode="PAY_PER_REQUEST",
                                    hash_key="custom",
                                    stream_view_type="NEW_IMAGE",
                                    attributes=[{
                                        "name": "custom",
                                        "type": "S",
                                    }])
                                    