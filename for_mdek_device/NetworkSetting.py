from bluepy import btle
import binascii
import struct
import time

MAC_array = ['E1:75:93:A0:B3:E0', 'E9:15:4A:CB:C0:80', 'E8:67:EA:81:5A:6B',
'F1:B4:EF:3F:74:DF', 'DE:16:DB:BA:11:A1']

for MAC in MAC_array:
  ble_connect_flag = False
  for i in range(5):
    print("Connect to ", (MAC))
    try:
      dev = btle.Peripheral(MAC)
      print("Connected")
      ble_connect_flag = True
      break
    except:
      time.sleep(1)

  if ble_connect_flag is False:
    print('Failed to connect to peripheral ', (MAC))
    raise

  locuuid = btle.UUID("680c21d9-c946-4c1f-9c11-baa1c21329e7")
  panuuid = btle.UUID("80f9d8bc-3bff-45bb-a181-2d6a37991208")
  locService = dev.getServiceByUUID(locuuid)

  panid = struct.pack(">H", 239)

  try:
    ch = locService.getCharacteristics(panuuid)[0]
    dev.writeCharacteristic(28, panid)
    print((MAC), 's panid : ', (panid))
  finally:
    dev.disconnect()
    print((MAC), 'is disconnected')