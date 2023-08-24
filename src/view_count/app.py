import json
import boto3
import requests
import os

def lambda_handler(event, context):
    table_name = os.environ.get("VIEW_COUNT_TABLE")

    client = boto3.client('dynamodb')
    db_response = client.get_item(
        TableName=table_name, 
        Key={
            'id': {
                "S":"portfolio-count"
            }
        }
    )

    current_count = int(db_response["Item"]["count"]["N"])
    current_count+=1
    new_item = {
        'id': {
            "S":"portfolio-count"
        },
        'count': {
            "N": str(current_count)
        }
    }

    put_response = client.put_item(
        TableName=table_name,
        Item=new_item
    )

    response = {
        'statusCode': 200,
        'body': json.dumps({'view-count':current_count}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }
    
    return response
