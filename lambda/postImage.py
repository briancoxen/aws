import urllib2
from StringIO import StringIO
import boto3
import json
import datetime
import os

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
    fileName = os.path.basename(event['url'])
    file = urllib2.urlopen(event['url'])
    fileBuffer = StringIO(file.read())
    s3 = boto3.client('s3')
    resp = s3.put_object(ACL="public-read",
                         Bucket="briancoxen.me",
                         Body=fileBuffer,
                         Key="photos/thumbnails/%s" % fileName);
    
    return response(resp, 200)
