import pulumi
import pulumi_gcp as gcp
import json
# bqowner = gcp.service_account.Account("bqowner", account_id="bqowner")


def get_schema():
    return json.load(open("data/tbl_sample_schema.json", 'r'))

main_dataset = gcp.bigquery.Dataset("main_dataset",
                                    dataset_id="main_dataset",
                                    friendly_name="friendly name for dataset",
                                    description="Main dataset",
                                    location="EU",
                                    delete_contents_on_destroy=True,
                                    )

sample_table = gcp.bigquery.Table("sample_table",
                                  dataset_id=main_dataset.dataset_id,
                                  table_id="sample_table",
                                  deletion_protection=False,
                                  time_partitioning=gcp.bigquery.TableTimePartitioningArgs(
                                      type="DAY",
                                  ),
                                    schema=json.dumps(get_schema())

                                  )