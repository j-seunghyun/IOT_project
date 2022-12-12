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
import I2C_LCD_driver
from threading import Thread

id = 1
mylcd = I2C_LCD_driver.lcd()

#for MQTT
Client_ID = "employee:id"
Guest_Thing_Name = f"guest:{id}"
Host_Name = "a1xvayn1nylqw4-ats.iot.ap-northeast-1.amazonaws.com"
Root_CA = "/home/pi/project/root_CA1/AmazonRootCA1.crt"
Private_key = "/home/pi/project/private_key/1ec7bb53fbf4890b391e5d0af3a3a2ffb7e579ac172d8bcc7bb8f4d04b627af0-private.pem.key"
Cert_File = "/home/pi/project/device_authentication/1ec7bb53fbf4890b391e5d0af3a3a2ffb7e579ac172d8bcc7bb8f4d04b627af0-certificate.pem.crt"

Client = AWSIoTPyMQTT.AWSIoTMQTTClient(Client_ID)
Client.configureEndpoint(Host_Name, 8883)
Client.configureCredentials(Root_CA, Private_key, Cert_File)
Client.configureConnectDisconnectTimeout(10)
Client.configureMQTTOperationTimeout(5)
Client.connect()


postHostUrl = "https://vj0cs4f7o9.execute-api.ap-northeast-1.amazonaws.com/default"

client_location = []


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
  dev.disconnect()
  position_array = [x_pos, y_pos]

  return position_array


async def post_distance(distance,current_index):
  #calc 함수에서 계산한 distance를 post
  datas = dict(index = current_index, distance = 200)
  response = await requests.post(postHostUrl, data=datas, headers=None)
  data = json.loads(response.content)
  return data

def customCallback(Client, userdata, message):
  messages = json.loads(message.payload)
  client_location.append(messages['location'])
  
  print("----------------------")
  print("CLIENT IS AT")
  print("[X,Y] = " + str(client_location)) #
  print("----------------------")
  

async def calcDistance(client_location, p_array):
  # client_location list가 비어 있을때는 0return
  # 거리는 root(a^2+b^2)

  if not client_location:
    return 0
  else:
    current_client_location = client_location[-1]
    a = current_client_location[0]- p_array[0]
    b = current_client_location[1]-p_array[1]
    distance = math.sqrt(a**2+b**2)
    return distance

"""
def LCD(situation):
  if situation == 0:
        #mylcd.lcd_display_string("CONSUMER  NEED",1,1)
        #mylcd.lcd_display_string("PRODUCT HELP ",2,2)
      print("CONSUMER  NEED")
      print("PRODUCT HELP")

  elif situation == 1:
      #mylcd.lcd_display_string("CONSUMER NEED",1,0)
      #mylcd.lcd_display_string("PLACE HELP ",2,0)
      print("CONSUMER NEED")
      print("PLACE HELP")

  elif situation == 2:
      #mylcd.lcd_display_string("EMERGENCY CALL",1,1)
      print("EMERGENCY CALL")
"""

def main(): #raspberrypi 하나로만 해야하니까 lcd는 화면으로 대체

  client_location_x = 0
  client_location_y = 0
  current_index = 0
  #mylcd.lcd_display_string("WAITING THE CALL",1,0)
  #mylcd.lcd_display_string("STAFF ID: " + str(id) ,2,3)
  print("----------------------")
  print("WAITING THE CALL")
  print("STAFF ID: " + str(id))
  print("----------------------")
  Client.subscribe(Guest_Thing_Name, 1, customCallback) #guest 주소 알수있음 (이것이 진행을 안해서 distance가 들어오지 않는 것)

  while True:
    start = time.time()
    
    dev = setLocationUwb()
    p_array = findLocation(dev)

    print("----------------------")
    print("EMPLOYEE IS AT")
    print("[X,Y] = " + str(p_array)) #
    print("----------------------")
    

    #distance계산이 된 다음에 post시킬 수 있도록 async
    distance = asyncio.run(calcDistance(client_location, p_array)) #client location = null이면 0

    #distance post시키는 함수
    if distance != 0:
      response = asyncio.run(post_distance(distance, current_index))
      current_index = current_index+1
      print(response)
    
    ###lcd화면에 예상 시간과 손님 위치 출력
    """
    situation = 0 # 임의의 상황 부여
    LCD(situation)
    time.sleep(2)
    """

    #mylcd.lcd_display_string("TIME TO CONSUMER",1,0)
    #mylcd.lcd_display_string("IS " + str(mint) + " MIN",2,4)

    """
    button = input("마무리 버튼(1)을 누르세요: \n")

    if button == 1:
      end = time.time()
      thetime = end - start
      sys.exit(0)
    """


    time.sleep(3)

main()
          
    #끝나는 시간 보내주면 Lambda post to dynamodb -> linearRegression
