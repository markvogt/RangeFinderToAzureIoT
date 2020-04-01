# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time

# 2020 03 23 MV: IMPORTED the following libraries for accessing RaspberryPi4 GPIO pins...
import RPi.GPIO as GPIO

# 2020 03 24 MV: IMPORTED (and installed before that) the following libraries from ADAFRUIT for easily interfacing with DHT-series sensors like the AM2302...
import board

#INITIALIZE some settings on the RPi4's GPIO...
GPIO.setwarnings(False)

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
# TYPE IN the following command using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
# CONNECTION_STRING = "{Your IoT hub device connection string}"
CONNECTION_STRING = "HostName=FactoryOfTheFutureSC.azure-devices.net;DeviceId=thing1;SharedAccessKey=+B0cnSCQZnmiw2UxvFvA0hgQv3kzp35gkf6DpmXkHuo="


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client



def ping():
	#Get reading from HC-SR04...
	GPIO.setmode(GPIO.BCM)
	 
	TRIG = 23 
	ECHO = 18
	 
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	 
	GPIO.output(TRIG, False)
	time.sleep(1)
	 
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	 
	while GPIO.input(ECHO)==0:
	  pulse_start = time.time()
	 
	while GPIO.input(ECHO)==1:
	  pulse_end = time.time()
	 
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)
	print( "Distance:",distance,"cm" )
	GPIO.cleanup()
    return distance



def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            #CAPTURE a sensor reading...
            newDistance = ping()
            
            #COMPOSE the JSON-formatted message to send to IoT Hub...
            MSG_TXT = '{{"distance": {distance}}}'
            msg_txt_formatted = MSG_TXT.format(distance=newDistance)
            message = Message(msg_txt_formatted)


            #SEND the message...
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print( "Message successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print( "IoT Hub Quickstart #1 - Simulated device" )
    print( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()