from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()
# These values are hard-coded for the sake of simplicity.
table_id = "sm589-project.ds_sample_for_load.sample_table"


def put_to_bigquery(rows_to_insert):
    # Make an API request.
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

# Basic Sample Data
# rows_to_insert = [
#     {"id": "1", "action_name": "Phred Phlyntstone", "process_time": 32},
#     {"id": "2", "action_name": "Wylma Phlyntstone", "process_time": 29},
# ]
