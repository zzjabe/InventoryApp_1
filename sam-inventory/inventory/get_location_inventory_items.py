import boto3
import json
import os

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = os.getenv('TABLE_NAME', 'SAM-Inventory')
    index_name = "GSI_Location_id"

    # Check path param
    if 'pathParameters' not in event or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' path parameter")
        }

    location_value = event['pathParameters']['location_id']

    try:
        response = dynamo_client.query(
            TableName=table_name,
            IndexName=index_name,
            KeyConditionExpression="#loc = :loc",
            ExpressionAttributeNames={
                "#loc": "location_id"
            },
            ExpressionAttributeValues={
                ":loc": {"S": location_value}
            }
        )

        items = response.get("Items", [])

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }