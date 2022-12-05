import time
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string("WAITING FOR THE",1,0)
mylcd.lcd_display_string("CALL",2,3)

time.sleep(3)
    
mylcd.lcd_clear()

#mqtt input
situation = 0

while True:
    if situation == 0:
        mylcd.lcd_display_string("CONSUMER NEED",1,0)
        mylcd.lcd_display_string("PRODUCT HELP Y/N",2,0)

        button = input("원하시는 버튼을 누르세요: 0:yes 1:no")
        print(button)
        button = int(button)

        mylcd.lcd_clear()

        if button == 0:
            #mqtt agree
        else:
            #mqtt disagree

    elif situation == 1:
        mylcd.lcd_display_string("CONSUMER NEED",1,0)
        mylcd.lcd_display_string("PLACE HELP Y/N",2,0)

        button = input("원하시는 버튼을 누르세요: 0:yes 1:no")
        print(button)
        button = int(button)

        mylcd.lcd_clear()

        if button == 0:
            #mqtt agree
        else:
            #mqtt disagree

    elif situation == 2:
        mylcd.lcd_display_string("EMERGENCY CALL",1,1)

        time.sleep(5)

        mylcd.lcd_clear()

        #mqtt disagree
    
    dist = 500

    mylcd.lcd_display_string("DISTANCE TO",1,0)
    mylcd.lcd_display_string("CONSUMER" + str(dist) + "m",2,0)

    button = input("마무리 버튼을 누르세요: 9:Fin")
    print(button)
    button = int(button)

    if button == 9:
        mylcd.lcd_clear()