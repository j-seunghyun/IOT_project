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
from bluepy.btle import Scanner, DefaultDelegate

id=1
#for MQTT publish in guest
Client_ID = f"guest:{id}"
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

# ble 로 scan을 하기 위한 코드
class ScanDelegate(DefaultDelegate):
  def __init__(self):
    DefaultDelegate.__init__(self)

def scanNearEmployee(employee_id_list):

  scanner = Scanner().withDelegate(ScanDelegate())
  devices = scanner.scan(10.0)
  #device의 Mac 주소
  dev_addr_list = []
  #device의 신호 세기
  dev_rssi_list = []
  for dev in devices:
    dev_addr_list.append(dev.addr)
    dev_rssi_list.append(dev.rssi)
  
  print(dev_addr_list)
  print(dev_rssi_list)
  tag_list = ["f1:b4:ef:3f:74:df","de:16:db:ba:11:a1"]
  dev_index_list = []
  # tag들의 addr list index를 찾는다.
  for dev_addr in dev_addr_list:
    if dev_addr in tag_list:
      dev_index_list.append(dev_addr_list.index(dev_addr))

  rssi_list = []
  for rssi_index in dev_index_list:
    rssi_list.append(dev_rssi_list[rssi_index])

  print(rssi_list)

  #각 tag에서의 rssi 값을 찾았으니 그 중 가장 신호가 센 것을 고른다.
  # 신호가 가장 세다는 것이 가장 가깝다는 의미

  max_rssi = max(rssi_list)
  
  #max_rssi를 표현한 tag와 employee_id_list와 index는 같다.(가정)
  tmp = dev_rssi_list.index(max_rssi)
  employee_id = 1

  return employee_id




#for location with UWB setup

def setLocationUwb():
  ble_connect_flag = False;
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
  return dev

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
  dev.disconnect()
  return position_array

def subscribeLocation(employee_id, p_array):
  message = {}
  message['employee_id'] = employee_id
  message['location'] = p_array
  messageJson = json.dumps(message)
  print(messageJson);

  Client.publish(Guest_Thing_Name, messageJson, 1)
  time.sleep(1)

def main():
  # 호출버튼 클릭했을 때
  # 버튼 종류 지정 필요
  if button_clicked:
    #request를 보낸다.
      #/employee/getState로 wait state를 가지는 직원의 list를 받아온다.
      employeelist = asyncio.run(req())

      employee_id_list =[]
      #list에서 employee_id값만 추출
      for employee in employeelist:
        employee_id_list.append(employee['id'])

      #wait중인 employee중 현재 손님과 가장 가까운 employee_id
      employee_id = scanNearEmployee(employee_id_list)
      
      while True:
      
        #가장 가까운 employee에게 자신의 위치 계속 mqtt로 publishing
        dev = setLocationUwb()
        p_array = findLocation(dev)

        #손님은 받아온 employeelist에서 wait상태인 employee id와 함께 자신의
        #변경되는 location 정보를 MQTT로 모두 보내준다.
        subscribeLocation(employee_id, p_array)


        ##get/time필요!!
        ##led 코드 삽입 되야함

        time.sleep(10)

main()




