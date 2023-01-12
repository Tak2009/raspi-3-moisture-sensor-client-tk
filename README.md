# raspi-3-moisture-sensor-client

Developed as a work-in-progress IoT project. A soil moisture sensor client checks the soil moisture on a daily basis and sends a signal to the water pump server to turn the pump on if the state of the soil is dry. Also all the daily check results are logged onto Google sheet via Google App Script (GAS). 

* GPIO programming using Python 3 on Raspberry Pi 4.
* 2 Raspberry Pis are used:a moisture sensor (client) and a water pump server connected to (server). Both client and server communicate via UDP sockets. 
* Cron runs soil moisture check functions on a daily basis and it returns the soil moisture state. If the state of the soil is “dry”, it sends signals to the water pump server to water plants.  
* Daily check keeps a daily log: the check time; the moisture level when checked; watering start time if applicable ; watering end time if applicable.

# raspi-3-water-pump-server

https://github.com/Tak2009/raspi-3-water-pump-server-tk
