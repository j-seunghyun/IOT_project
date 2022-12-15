import time
import I2C_LCD_driver
from threading import Thread

mylcd = I2C_LCD_driver.lcd()
staff_id = 1 #직원 id = 1

#매칭이 되는 과정 추가 필요

situation = 0 # 임의의 상황 부여


while True:
    mylcd.lcd_display_string("WAITING THE CALL",1,0)
    mylcd.lcd_display_string("STAFF ID: " + str(staff_id) ,2,3)

    time.sleep(3)

    check_id = input("현재 직원번호 1 \n check_id를 누르세요: ")
    print(check_id)
    check_id = int(check_id)
    #check_id = 1
    mylcd.lcd_clear()

    if staff_id == check_id: #호출이 시작 보내고
        start = time.time()
        if situation == 0:
            mylcd.lcd_display_string("CONSUMER  NEED",1,1)
            mylcd.lcd_display_string("PRODUCT HELP ",2,2)

            time.sleep(5)
            mylcd.lcd_clear()

        elif situation == 1:
            mylcd.lcd_display_string("CONSUMER NEED",1,0)
            mylcd.lcd_display_string("PLACE HELP ",2,0)

            time.sleep(5)
            mylcd.lcd_clear()

        elif situation == 2:
            mylcd.lcd_display_string("EMERGENCY CALL",1,1)

            time.sleep(5)
            mylcd.lcd_clear()

        #mqtt로 시간 계산 들어와서 알려주기
        mint = 1 #분 단위

        mylcd.lcd_display_string("TIME TO CONSUMER",1,0)
        mylcd.lcd_display_string("IS " + str(mint) + " MIN",2,4)

        #timeout 시스템
        arrive_time = int(mint) * 60
        button = None

        def check():
            time.sleep(arrive_time)
            if button != None:
                return
            mylcd.lcd_clear()
            mylcd.lcd_display_string("NOW YOU SHOULD ",1,1)
            mylcd.lcd_display_string("BE ARRIVED",2,3)
                
        Thread(target = check).start()

        button = input("마무리 버튼을 누르세요: ")
        print(button)
        Button = int(button)
        
        end = time.time()
        thetime = end - start
        print(f"{thetime:.5f} sec")
        #끝나는 시간 보내주면