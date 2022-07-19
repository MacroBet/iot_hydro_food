import paho.mqtt.client as mqtt


class MqttClient:

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("status")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
    
    def mqtt_client(self):
        
        print("Mqtt client starting")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            print("dio porco")
            print(str(e))
        self.client.loop_forever()