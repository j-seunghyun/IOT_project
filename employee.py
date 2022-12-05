#from bluepy import btle
import binascii
import struct
import time
import json
#import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from datetime import datetime
import asyncio
import requests_async as requests
import base64

#date는 
now = datetime.now()
print(now.date())
print(now.hour, now.minute, now.second)

#for MQTT 
Client_ID = "guest:${id}"
Thing_Name = "pi"
Host_Name = "a1xvayn1nylqw4-ats.iot.ap-northeast-1.amazonaws.com"
Root_CA = "/home/pi/IOT/root_CA1/AmazonRootCA1.crt"
Private_key = "/home/pi/IOT/private_key/1ec7bb53fbf4890b391e5d0af3a3a2ffb7e579ac172d8bcc7bb8f4d04b627af0-private.pem.key"
Cert_File = "/home/pi/IOT/device_authentication/1ec7bb53fbf4890b391e5d0af3a3a2ffb7e579ac172d8bcc7bb8f4d04b627af0-certificate.pem.crt"


# Employee (직원)
# 직원에게는 호출 승인 , 호출 거절 버튼 2개 존재

employee_id = 1
employee_state = "wait"

while employee_state == "wait":
  #직원은 wait상태일때 자신이 subscribe하는 손님 location 주제에 대해 subscribe하고 있는 상태

  #MQTT로 손님이 publish한 message에 자신의 id가 있다면
  if 