from bluepy import btle
import binascii
import struct
import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from datetime import datetime
import asyncio
import requests_async as requests
import base64

id = 1
#for MQTT
Client_ID = "employee:id"
Guest_Thing_Name = f"guest:{id}"
Host_Name = "a1xvayn1nylqw4-ats.iot.ap-northeast-1.amazonaws.com"
Root_CA = "/home/pi/IOT/root_CA1/AmazonRootCA1.crt"
Private_key = "/home/pi/IOT/private_key/1ec7bb53fbf4890b391e5d0af3a3a2ffb7e579ac172d8bcc7bb8f4d04b627af0-private.pem.key"
Cert_File = "/home/pi/IOT/device_authentication/1ec7bb53fbf4890b391e5d0af3a3a2ffb7e579ac172d8bcc7bb8f4d04b627af0-certificate.pem.crt"

Client = AWSIoTPyMQTT.AWSIoTMQTTClient(Client_ID)
Client.configureEndpoint(Host_Name, 8883)
Client.configureCredentials(Root_CA, Private_key, Cert_File)
Client.configureConnectDisconnectTimeout(10)
Client.configureMQTTOperationTimeout(5)
Client.connect()


#employee에서의 uwb setup
def setLocationUwb():
  ble_connect_flag = False;
  for i in range(5):
    print("Connecting...")
    try:
      dev = btle.Peripheral('DE:16:DB:BA:11:A1')
      print('Connected')
      ble_connect_flag = True
      break
    except:
      time.sleep(1)

  if ble_connect_flag is False:
    print('Failed to connect to peripheral')
    raise
  return dev

#employee에서의 find location
def findLocation(dev):

  locuuid = btle.UUID("680c21d9-c946-4c1f-9c11-baa1c21329e7")
  readdata = btle.UUID("003bbdf2-c634-4b3d-ab56-7ec889b89a37")
  locService = dev.getServiceByUUID(locuuid)
  n_id = [0]*3
  n_dis = [0]*3

  ch = locService.getCharacteristics(readdata)[0]
  val = binascii.b2a_hex(ch.read())
  x_pos = bytearray(ch.read()[1:5])
  y_pos = bytearray(ch.read()[5:9])
  z_pos = bytearray(ch.read()[9:13])

  x_pos = struct.unpack('<i', x_pos)[0]
  x_pos = x_pos/1000
  y_pos = struct.unpack('<i', y_pos)[0]
  y_post = y_pos/1000
  z_pos = struct.unpack('<i', z_pos)[0]
  z_pos = z_pos/1000

  position_array = [x_pos, y_pos]
  return position_array

def calcDistance(client_location, p_array):
  # client_location list가 비어 있을때는 0return
  # 거리는 root(a^2+b^2)
  if not client_location:
    return 0
  else:
    a = client_location[0]- p_array[0]
    b = client_location[1]-p_array[1]
    distance = math.sqrt(a**2+b**2)
    return distance



client_location = []

def customCallback(Client, userdata, message):
  messages = json.loads(message.payload)
  print(messages['employee_id'])
  print(messages['location'])
  client_location = messages['location']

def main():
  Client.subscribe(Guest_Thing_Name, 1, customCallback)
  while True:
    dev = setLocationUwb()
    p_array = findLocation(dev)
    distance = calcDistance(client_location, p_array)

    #distance를 회귀분석이 담긴 dynamodb에 request해서
    #response로 예상 time을 받아온다.
    
    #led화면에 예상 시간과 손님 위치 출력

    time.sleep(10)

main()