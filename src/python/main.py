import threading
import time
import roboclaw
import paho.mqtt.client as mqtt
import subprocess
from sense_hat import SenseHat
from signal import pause

server = "localhost"
port = 1883
vhost = "/"
username = "guest"
password = "guest"
topic = "commands/#"

sense = SenseHat()
sense.set_rotation(270)
sense.set_imu_config(False, True, False)

#Windows comport name
#roboclaw.Open("COM3",115200)
#Linux comport name
roboclaw.Open("/dev/ttyAMA0",115200)

address = 0x80

roboclaw.ForwardMixed(address, 0)
roboclaw.TurnRightMixed(address, 0)

def joystick_pushed(event):
    client.publish("commands/joystick", event.direction + "_" + event.action)

def onConnect(client, userdata, rc):    #event on connecting
    client.subscribe([(topic, 1)])  #subscribe
    sense.show_message("Ready", text_colour=[255, 0, 255])
    w = threading.Thread(target=joystick_MQTT)
    w2 = threading.Thread(target=sensors_MQTT)
    w.start()
    w2.start()
    print("Ready")

def onMessage(client, userdata, message):   #event on receiving message
	roboAction = ""
	if message.payload == "38":
		roboclaw.ForwardMixed(address, 64)
		roboAction = "Moving Forward"
	elif message.payload == "40":
		roboclaw.BackwardMixed(address, 64)
		roboAction = "Moving Backward"
	elif message.payload == "37":
		roboclaw.TurnLeftMixed(address, 64)
		roboAction = "Turning Left"
	elif message.payload == "39":
		roboclaw.TurnRightMixed(address, 64)
		roboAction = "Turning Right"
	elif message.payload == "middle_held":
		subprocess.call(["node", "src/app.js", "--clear=true"])
		roboAction = "Reset WiFi"
	elif message.payload == "":
		roboclaw.ForwardMixed(address, 0)
		roboclaw.BackwardMixed(address, 0)
		roboclaw.TurnRightMixed(address, 0)
		roboclaw.TurnLeftMixed(address, 0)
	if roboAction != "":	#Remove this IF to show all MQTT messages
		print("Action: " + roboAction + ", Topic: " + message.topic + ", Message: " + message.payload)

def sensors_MQTT():
	while True:
            client.publish("sense/temp", round(sense.get_temperature(),1))
            client.publish("sense/humidity", round(sense.get_humidity(),0))
            client.publish("sense/pressure", round(sense.get_pressure(),0))
            accel_only = sense.get_accelerometer()
            client.publish("sense/pitch", "{pitch}".format(**accel_only))
            client.publish("sense/roll", "{roll}".format(**accel_only))
            client.publish("sense/yaw", "{yaw}".format(**accel_only))

def joystick_MQTT():
    sense.stick.direction_any = joystick_pushed
    pause()

while True:
    try:
        client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol="MQTTv31")
        client.username_pw_set(vhost + ":" + username, password)
        client.on_connect = onConnect
        client.on_message = onMessage
        client.connect(server, port, keepalive=60, bind_address="") #connect
        client.loop_forever()   #automatically reconnect once loop forever
    except Exception, e:
        #when initialize connection, reconnect on exception
        print "MQTT Server not ready, reconnecting..."
        time.sleep(10)
