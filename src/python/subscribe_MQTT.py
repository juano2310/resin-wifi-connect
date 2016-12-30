import time
import roboclaw
import paho.mqtt.client as mqtt

#Windows comport name
#roboclaw.Open("COM3",115200)
#Linux comport name
roboclaw.Open("/dev/ttyAMA0",115200)

address = 0x80

roboclaw.ForwardMixed(address, 0)
roboclaw.TurnRightMixed(address, 0)

server = "localhost"
port = 1883
vhost = "/"
username = "guest"
password = "guest"
topic = "robot/commands/#"

"""
 * This method is the callback on connecting to broker.
 * @ It subscribes the target topic.
"""
def onConnect(client, userdata, rc):    #event on connecting
    client.subscribe([(topic, 1)])  #subscribe

"""
 * This method is the callback on receiving messages.
 * @ It prints the message topic and payload on console.
"""

def onMessage(client, userdata, message):   #event on receiving message
	if message.payload == "38":
			roboclaw.ForwardMixed(address, 64)
	elif message.payload == "40":
		roboclaw.BackwardMixed(address, 64)
	elif message.payload == "37":
		roboclaw.TurnLeftMixed(address, 64)
	elif message.payload == "39":
		roboclaw.TurnRightMixed(address, 64)
	elif message.payload == "":
		roboclaw.ForwardMixed(address, 0)
		roboclaw.BackwardMixed(address, 0)
		roboclaw.TurnRightMixed(address, 0)
		roboclaw.TurnLeftMixed(address, 0)
	print("Topic: " + message.topic + ", Message: " + message.payload)

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
        print "Exception handled, reconnecting...\nDetail:\n%s" % e
        time.sleep(5)
