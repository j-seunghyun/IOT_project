import time
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

second = 0

mylcd.lcd_display_string("WEL-COME TO OUR",1,0)
mylcd.lcd_display_string("MARKET",2,5)

time.sleep(3)
    
mylcd.lcd_clear()

while True:

    mylcd.lcd_display_string("FIND FIND  EMER",1,0)
    mylcd.lcd_display_string("PROD PLACE GENCY",2,0)

    button = input("원하시는 버튼을 누르세요: ")
    print(button)
    button = int(button)
    mylcd.lcd_clear()

    if button == 1:
        mylcd.lcd_display_string("FINDING FOR HELP",1,0)
        mylcd.lcd_display_string("CHOICE: PRODUCT",2,0)
        time.sleep(3)
        mylcd.lcd_clear()

        dist = 500 ###여기서 mqtt로 거리 정보 가져오기

        mylcd.lcd_display_string("STAFF IS COMING",1,0)
        mylcd.lcd_display_string("FINDING PRODUCT",2,0)


    elif button == 2:
        mylcd.lcd_display_string("FINDING FOR HELP",1,0)
        mylcd.lcd_display_string("CHOICE: PLACE",2,1)
        time.sleep(3)
        mylcd.lcd_clear()

        dist = 500 ###여기서 mqtt로 거리 정보 가져오기

        mylcd.lcd_display_string("STAFF IS COMING",1,0)
        mylcd.lcd_display_string("FINDING PLACE",2,1)

    elif button == 3:
        mylcd.lcd_display_string("FINDING FOR HELP",1,0)
        mylcd.lcd_display_string("EMERGENCY CALL",2,1)
        time.sleep(3)
        mylcd.lcd_clear()

        dist = 500 ###여기서 mqtt로 거리 정보 가져오기

        mylcd.lcd_display_string("STAFF IS COMING",1,0)
        mylcd.lcd_display_string("EMERGENCY CALL",2,1)

    time.sleep(3)

    mylcd.lcd_clear()
