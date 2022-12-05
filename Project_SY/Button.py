import time
import RPi.GPIO as gpio

button_prod = 17
button_place = 20

gpio.setmode(gpio.BCM)
gpio.setup(button_prod, gpio.IN)
gpio.setup(button_place, gpio.IN)
i = 0

while True:
    voltage_prod = gpio.input(button_prod)
    voltage_place = gpio.input(button_place)
    
    print(i)
    if voltage_prod == 1:
        print("Button1 is up")
    if voltage_place == 1:
        print("Button2 is up")
    
    i = i + 1
    time.sleep(0.2)
