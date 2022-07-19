from pydoc import cli
from mqttNetwork.mqtt_collector import MqttClient

if __name__ == "__main__":

    client = MqttClient()
    client.mqtt_client()
    
