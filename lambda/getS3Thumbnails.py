import boto3
import datetime
import json

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def response(body, status):
    response = {
        "isBase64Encoded": "false",
        "statusCode": status,
        "headers": { "Content-Type": "text/json", "Access-Control-Allow-Origin": "*" },
        "body": json.dumps(body, default=datetime_handler)
    }
    return response

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    data = s3.list_objects_v2(Bucket="briancoxen.me", Prefix="photos/thumbnails")
    return response(data['Contents'], 200)
