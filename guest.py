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

Client = AWSIoTPyMQTT.AWSIoTMQTTClient(Client_ID)
Client.configureEndpoint(Host_Name, 8883)
Client.configureCredentials(Root_CA, Private_key, Cert_File)
Client.configureConnectDisconnectTimeout(10)
Client.configureMQTTOperationTimeout(5)
Client.connect()


#for lamda_get employee list(state:wait)
forEmployeeParams = {'state' : 'wait'}
getEmployeeStateUrl = 'https://wfnmvsj0rl.execute-api.ap-northeast-1.amazonaws.com/default/get/employee/state'


#function request get Employee list(state가 wait인)
async def req():
  response = await requests.get(getEmployeeStateUrl, params= forEmployeeParams)
  waitEmployeeList = json.loads(response.content)
  return waitEmployeeList

# guest (손님)

# 라즈베리파이의 power가 on일때 (가정) => 켜졌을 때
guest_state = "on"
#임의로 1 지정
guest_id = 1

button_clicked = True

#for location with UWB setup

def setLocationUwb():
  for i in range(5):
  print("Connecting...")
  try:
    dev = btle.Peripheral('F1:B4:EF:3F:74:DF')
    print('Connected')
    ble_connect_flag = True
    break
  except:
    time.sleep(1)

  if ble_connect_flag is False:
    print('Failed to connect to peripheral')
    raise

  locuuid = btle.UUID("680c21d9-c946-4c1f-9c11-baa1c21329e7")
  readdata = btle.UUID("003bbdf2-c634-4b3d-ab56-7ec889b89a37")
  locService = dev.getServiceByUUID(locuuid)
  n_id = [0]*3
  n_dis = [0]*3
  return dev

def findLocation(dev):
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


while True:
  # 호출버튼 클릭했을 때
  # 버튼 종류 지정 필요
  if button_clicked:
    # 호출 버튼을 누른다음 바로 자신의 location UWB로 측정
    while True:
      # 버튼이 눌리고 나서부터 
      if(ch.supportsRead):
        ch = setLocationUwb()
        p_array = arrfindLocation(ch)

      #request를 보낸다.
      #/employee/getState로 wait state를 가지는 직원의 list를 받아온다.
      employeelist = asyncio.run(req())

      #손님은 받아온 employeelist에서 wait상태인 employee id와 함께 자신의
      #location 정보를 MQTT로 모두 보내준다. 


    message = {}
    message['']
    # wait상태인 직원의 id에 해당하는 직원을 위해 publish 할때 id와 자신의 location보내준다.
    #employee id에 해당하는 employee에 MQTT publisher가 되어 location publishing
    #동시에 guest 또한 employee id에 해당하는 모든 device에 subscriber가 되어
    #직원쪽에서 매칭수락을 하면 

    #직원이 guest에게 매칭이 된 후부터 MQTT로 매칭이되었다고 알려줌

    # guest는 이제부터 MQTT로 자신의 location 계속 출력
    break




