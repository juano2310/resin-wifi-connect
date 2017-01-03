from sense_hat import SenseHat
import time
import paho.mqtt.client as mqtt

sense = SenseHat()

server = "localhost"
port = 1883
vhost = "/"
username = "guest"
password = "guest"

try:
    # set up mqtt client
	client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol="MQTTv31")
	client.username_pw_set(vhost + ":" + username, password)
	client.connect(server, port, keepalive=60, bind_address="") #connect
    	client.loop_forever()

    while True:
            client.publish("sense/temp", sense.get_temperature())
            client.publish("sense/humidity", sense.get_humidity())
            time.sleep(10)

except Exception, e:
    print e
