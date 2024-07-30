import json
import boto3

def lambda_handler(event, context):
    
    client = boto3.client('glue')
    
    response = client.start_job_run(
        JobName="B3_ETL",
    )
    
    # Obtém o ID do job run
    job_run_id = response['JobRunId']

    print(f'Job B3_ETL iniciado com JobRunId: {job_run_id}')

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(job_run_id)
    }
