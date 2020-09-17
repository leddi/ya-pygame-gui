import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("vsrv.ledderboge.net", 1883, 60)
client.loop_start()
while True:
   msg=input("Text: ")
   client.publish("counter/down", msg)
