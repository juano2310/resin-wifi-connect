from sense_hat import SenseHat
import paho.mqtt.client as mqtt

sense = SenseHat()
sense.set_imu_config(True, True, True)

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
	client.loop_start()

	while True:
            client.publish("sense/temp", round(sense.get_temperature(),1))
            client.publish("sense/humidity", round(sense.get_humidity(),0))
            client.publish("sense/pressure", round(sense.get_pressure(),0))
            accel_only = sense.get_accelerometer()
            client.publish("sense/pitch", "{pitch}".format(**accel_only))
            client.publish("sense/roll", "{roll}".format(**accel_only))
            client.publish("sense/yaw", "{yaw}".format(**accel_only))

except Exception, e:
    print e
