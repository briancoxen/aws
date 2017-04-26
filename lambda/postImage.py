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
    
def responseBody(body, status):
    return {
        "isBase64Encoded": "false",
        "statusCode": status,
        "headers": { "Access-Control-Allow-Origin": "*",
                     "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"},
        "body": json.dumps(body, default=datetime_handler)
    }
    
def postImage(url):
    try:
        fileName = os.path.basename(url)
        file = urllib2.urlopen(url)
        fileBuffer = StringIO(file.read())
        s3 = boto3.client('s3')
        body = s3.put_object(ACL="public-read",
                         Bucket="briancoxen.me",
                         Body=fileBuffer,
                         Key="photos/thumbnails/%s" % fileName);
    except:
        return {"body": {"error": "Internal server error!"}, "status":500}
        
    if body['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {"body":body, "status":200}
    else:
        return {"body":body, "status":500}

def response(event):
    if event['httpMethod'] == 'OPTIONS':
        return responseBody({}, 200)
    elif event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        pI = postImage(body['url'])
        return responseBody(pI['body'], pI['status'])
    else:
        return responseBody({}, 401)

def lambda_handler(event, context):
    return response(event)
