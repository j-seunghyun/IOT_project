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
    
    max_index = 0
    distance = 0
    
    for current_distance in distance_list:
        if current_distance.get('index') > max_index:
            max_index = current_distance.get('index')
            distance = current_distance.get('distance')
    
    print(distance)
    
        
    return {
        'statusCode': 200,
        'body': json.dumps(distance, cls=DecimalEncoder)
    }