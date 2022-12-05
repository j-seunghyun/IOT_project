import json
import boto3
import json
from boto3.dynamodb.conditions import (Key, Attr)
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self,obj)

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Employee')
    sortdict = event.get('queryStringParameters')
    sortstate = sortdict['state']
    
    data = table.scan(
        FilterExpression=Attr("state").eq('wait')
    )
    
    
    # TODO implement
    response = {
        'statusCode': 200,
        'body': json.dumps(data.get('Items'), cls=DecimalEncoder)
    }
    return response
