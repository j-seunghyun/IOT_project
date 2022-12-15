import boto3
import json
import numpy as np 
from boto3.dynamodb.conditions import (Key, Attr)
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self,obj)

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('LinearRegression')
    
    data = table.scan(
        #FilterExpression=Attr("staff_id").eq(3)
    )
    
    
    item = data.get('Items')
    x_train = []
    y_train = []
    datas = [x_train, y_train]

    for i in item:
        x_train.append(i['distance'])
        y_train.append(i['time'])
    
    response = {
        'statusCode': 200,
        'body': json.dumps(datas,cls=DecimalEncoder)
    }
    return response