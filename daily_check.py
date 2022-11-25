# http://rasp.io/wp-content/uploads/2016/06/RasPiO_Analog_Zero.pdf
# SPI should be enabled. Preferences -> RasPi Config -> Interface tab
import time
import os
from gpiozero import MCP3008
import google_sheet as g
import client as client

Vref = 3.3
# driest
high_value = 300 
# wettest
low_value = 120
interval = (high_value - low_value) / 3
wet = low_value + interval
dry = high_value - interval
plant_pot = MCP3008(channel=0)
daily_check_hum = round(plant_pot.value * Vref * 100,1)
daily_check_run_time = time.strftime('%d/%m/%Y %H:%M:%S')
start = 0
end = 0
watering_duration = 10
pause = 5
buffer = 5

def moisuture_check_and_water():
    try:
        global start
        global end
        start = time.strftime('%d/%m/%Y %H:%M:%S')
        while True:
            hum = round(plant_pot.value * Vref * 100,1)
            print("Moisture check and watering loop starts")
            if (hum > low_value and hum < wet):
                print("Very Wet: " + str(hum))
                # to close the socket on server. no need to turn the water pump on
                client.send_message_to_watering_server("VERY WET", 0, 0)
                break
            elif (hum > wet and hum < dry):
                print("Wet: " + str(hum))
                # to close the socket on server. no need to turn the water pump on
                client.send_message_to_watering_server("WET", 0, 0)
                break
            elif (hum < high_value and hum > dry):
                print("Dry: " + str(hum))
                # to triger water pump
                client.send_message_to_watering_server("DRY", watering_duration, pause)
            print(time.strftime('%d/%m/%Y %H:%M:%S') + ': Waiting for ' + str((watering_duration + pause + buffer))+ ' seconds before the next moisture check loop')    
            time.sleep(watering_duration + pause + buffer)
        print("exiting")
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Ctr-C")
    end = time.strftime('%d/%m/%Y %H:%M:%S')
    client.close_socket()
    os.system('clear')
    
def daily_check():
    if (daily_check_hum > low_value and daily_check_hum < wet):
        print("Very Wet: " + str(daily_check_hum))
        daily_check_state = "VERY WET"
    elif (daily_check_hum > wet and daily_check_hum < dry):
        print("Wet: " + str(daily_check_hum))
        daily_check_state = "WET"
    elif (daily_check_hum < high_value and daily_check_hum > dry):
        print("Dry: " + str(daily_check_hum))
        daily_check_state = "DRY"
    return daily_check_state

daily_check_state = daily_check()

if daily_check_state == "DRY":
    print('The state of the soil is: ' + daily_check_state)
    print('Auto moisture check and watering function is being triggered')
    moisuture_check_and_water()
    print('Watering completed')
else:
    # to close the socket on server. no need to turn the water pump on
    client.send_message_to_watering_server(daily_check_state, 0, 0)
    client.close_socket()

g.google_sheet_update(daily_check_run_time, daily_check_hum, daily_check_state, start, end)
print('Google sheet updated')
plant_pot.close()
print('Sensor device shut down')