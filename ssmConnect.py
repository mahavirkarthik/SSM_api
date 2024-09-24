import json
import boto3
from botocore.exceptions import ClientError
 
def lambda_handler(event, context):
    instance_id = event.get('instance_id')
 
    if not instance_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Instance ID is required'})
        }
 
    try:
        ssm_client = boto3.client('ssm')
        response = ssm_client.start_session(Target=instance_id)
        session_id = response['SessionId']
        # Construct the session URL in the desired format
        region = context.invoked_function_arn.split(":")[3]  # Get the region from the ARN
        session_url = f"https://{region}.console.aws.amazon.com/systems-manager/session-manager/{instance_id}?region={region}"
 
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Connection established',
                'session_id': session_id,
                'session_url': session_url
            })
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }