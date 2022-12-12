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
    # TODO implement
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Distance')
    
    data = table.scan()
    distance_list = data.get('Items')
    
    current_distance_list = distance_list[0]
    distance = current_distance_list.get('distance')
    
        
    return {
        'statusCode': 200,
        'body': json.dumps(distance, cls=DecimalEncoder)
    }
