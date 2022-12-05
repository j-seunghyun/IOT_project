import time
import random
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

id=1
Client_ID = f"guest:{id}"
Thing_Name = f"guest:{id}"
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

loopCount =0
while True:
  message = {}
  message['client_id'] = id
  print(message)
  message['location'] = '(170.2, 342.3)'
  messageJson = json.dumps(message)

  Client.publish(Thing_Name,messageJson,1)
  print('published topic %s : %s\n' % (Thing_Name, messageJson))
  loopCount += 1
  time.sleep(1)