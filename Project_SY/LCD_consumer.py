import time
import I2C_LCD_driver

"""
import random
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

Client_ID = "IoT_System_Client"
Thing_Name = "IOT_pi"
Host_Name = "a2c74zzj6idicr-ats.iot.ap-northeast-2.amazonaws.com"
Root_CA = "/home/pi/AWS/CA1/AmazonRootCA1.crt"
Private_Key = "/home/pi/AWS/private_key_file/37f5e195fcd74650f14d953498b202a8d0f314f84c788c4a619a9c5287777ff3-private.pem.key"
Cert_File = "/home/pi/AWS/device_certi/37f5e195fcd74650f14d953498b202a8d0f314f84c788c4a619a9c5287777ff3-certificate.pem.crt"

Client = AWSIoTPyMQTT.AWSIoTMQTTClient(Client_ID)
Client.configureEndpoint(Host_Name, 8883)
Client.configureCredentials(Root_CA, Private_Key, Cert_File)
Client.configureConnectDisconnectTimeout(10)
Client.configureMQTTOperationTimeout(5)
Client.connect()

def customCallack(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("-----------\n\n")
"""

mylcd = I2C_LCD_driver.lcd()

second = 0
mint = 2 ###임의의 값

mylcd.lcd_display_string("WEL-COME TO OUR",1,0)
mylcd.lcd_display_string("MARKET",2,5)

time.sleep(3)
    
mylcd.lcd_clear()

while True:

    mylcd.lcd_display_string("FIND FIND  EMER",1,0)
    mylcd.lcd_display_string("PROD PLACE GENCY",2,0)

    ### 1, 2, 3 번의 선택지 중 하나로 받아서 그에 해당하는 상황 부여
    button = input("원하시는 버튼을 누르세요: ")
    print(button)
    button = int(button)
    mylcd.lcd_clear()

    ### 1 - FIND PRODUCT를 선택했을때
    if button == 1:
        mylcd.lcd_display_string("FINDING FOR HELP",1,0)
        mylcd.lcd_display_string("CHOICE: PRODUCT",2,0)
        time.sleep(3)
        mylcd.lcd_clear()

        mylcd.lcd_display_string("STAFF IS COMING",1,0)
        mylcd.lcd_display_string("WAIT FOR " + str(mint) + " MIN",2,0)


        #mylcd.lcd_display_string("STAFF IS COMING",1,0)
        #mylcd.lcd_display_string("FINDING PRODUCT",2,0)

        #여기서 mqtt로 회귀분석을 통해 직원이 손님한테 오는데 걸리는 시간에 대한 정보를 가져온다.

    elif button == 2:
        mylcd.lcd_display_string("FINDING FOR HELP",1,0)
        mylcd.lcd_display_string("CHOICE: PLACE",2,1)
        time.sleep(3)
        mylcd.lcd_clear()

        ###여기서 mqtt로 회귀분석을 통해 직원이 손님한테 오는데 걸리는 시간에 대한 정보를 가져온다.

        mylcd.lcd_display_string("STAFF IS COMING",1,0)
        mylcd.lcd_display_string("FINDING PLACE",2,1)

    elif button == 3:
        mylcd.lcd_display_string("FINDING FOR HELP",1,0)
        mylcd.lcd_display_string("EMERGENCY CALL",2,1)
        time.sleep(3)
        mylcd.lcd_clear()

        ###여기서 mqtt로 회귀분석을 통해 직원이 손님한테 오는데 걸리는 시간에 대한 정보를 가져온다.

        mylcd.lcd_display_string("STAFF IS COMING",1,0)
        mylcd.lcd_display_string("EMERGENCY CALL",2,1)

    time.sleep(3)

    mylcd.lcd_clear()
