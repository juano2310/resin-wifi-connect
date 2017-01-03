import threading
import time
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
import paho.mqtt.client as mqtt

server = "localhost"
port = 1883
vhost = "/"
username = "guest"
password = "guest"

sense = SenseHat()
sense.set_imu_config(False, True, False)

try:
    	# set up mqtt client
	client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol="MQTTv31")
	client.username_pw_set(vhost + ":" + username, password)
	client.connect(server, port, keepalive=60, bind_address="") #connect
    	client.loop_start()
except Exception, e:
	print e

def joystick_pushed(event):
    client.publish("commands/joystick", event.direction + "_" + event.action)

def joystick_MQTT():
    print threading.currentThread().getName(), 'Starting'
    sense.stick.direction_any = joystick_pushed
    pause()
    print threading.currentThread().getName(), 'Exiting'

def sense_MQTT():
	while True:
            client.publish("sense/temp", round(sense.get_temperature(),1))
            client.publish("sense/humidity", round(sense.get_humidity(),0))
            client.publish("sense/pressure", round(sense.get_pressure(),0))
            accel_only = sense.get_accelerometer()
            client.publish("sense/pitch", "{pitch}".format(**accel_only))
            client.publish("sense/roll", "{roll}".format(**accel_only))
            client.publish("sense/yaw", "{yaw}".format(**accel_only))

w = threading.Thread(target=joystick_MQTT)
w2 = threading.Thread(target=sense_MQTT)

w.start()
w2.start()
