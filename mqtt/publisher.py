from umqtt.simple import MQTTClient
import time

SERVER = '127.0.0.1'
CLIENT_ID = 'PYESPCAR_A0' # 客户端的ID
TOPIC = b'pyespcar_basic_control' # TOPIC的ID

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()

while True:
    client.publish(TOPIC, 'helloworld')
    time.sleep(1)
