import time
import I2C_LCD_driver

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
