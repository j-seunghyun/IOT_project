from bluepy import btle
import binascii
import struct
import time

MAC_array = ['E1:75:93:A0:B3:E0', 'E9:15:4A:CB:C0:80', 'E8:67:EA:81:5A:6B',
'F1:B4:EF:3F:74:DF', 'DE:16:DB:BA:11:A1']

pos_x = [0,1000,500]
pos_y = [0,0,500]
pos_z = [0,0,0]

count = 0
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
    print("Failed to connect to peripheral ", (MAC))
    raise

  locuuid = btle.UUID("680c21d9-c946-4c1f-9c11-baa1c21329e7")
  panuuid = btle.UUID("80f9d8bc-3bff-45bb-a181-2d6a37991208")
  opuuid = btle.UUID("3f0afd88-7770-46b0-b5e7-9fc099598964")
  posuuid = btle.UUID("f0f26c9b-2c8c-49ac-ab60-fe03def1b40c")

  locService = dev.getServiceByUUID(locuuid)
  if count == 0:
    opcode = struct.pack(">H", 0b1101110110000000)
    poscode = struct.pack("<iiib", pos_x[count], pos_y[count], pos_z[count], 100)

  elif count == 3:
    opcode = struct.pack(">H", 0b0101110100100000)
  
  elif count == 4:
    opcode = struct.pack(">H", 0b0101110100100000)
  else:
    opcode = struct.pack(">H", 0b1101110100000000)
    poscode = struct.pack("<iiib", pos_x[count], pos_y[count], pos_z[count], 100)

  print(poscode)
  try:
    if count != 3:
      ch = locService.getCharacteristics(opuuid)[0]
      dev.writeCharacteristic(ch.valHandle, opcode)
      print((MAC_array[i]), 's opcode : ', (opcode))
      ch1 = locService.getCharacteristics(posuuid)[0]
      dev.writeCharacteristic(ch1.valHandle, poscode)
    else:
      ch = locService.getCharacteristics(opuuid)[0]
      dev.writeCharacteristic(ch.valHandle, opcode)
      print((MAC_array[i]), 's opcode : ', (opcode))
  finally:
    dev.disconnect()
    print((MAC), 'is disconnected')
  count = count+1