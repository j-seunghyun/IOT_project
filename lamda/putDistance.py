import json
import boto3
import base64
import binascii
from binascii import unhexlify

def lambda_handler(event, context):
    # TODO implement
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Distance')
    
    result = base64.b64decode(event.get('body')).decode('utf-8')
    data_list = result.split("&")
    
    keys = []
    values = []
    
    for data in data_list:
        pair = data.split("=")
        keys.append(pair[0])
        values.append(pair[1])
    
    my_dict = dict(zip(keys, values))
    
    index = my_dict['index']
    distance = my_dict['distance']
        
    
    data = table.put_item(
        Item={
            'index': int(index),
            'distance': int(distance)
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(my_dict)
    }
