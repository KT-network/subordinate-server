from paho.mqtt.client import Client

mc = Client(client_id="blue-app")
mc.username_pw_set("841369846", "123456")
mc.connect("mqtt.kt-network.cn", 1883)

# mc.subscribe(topic="btest", qos=1)
mc.subscribe(topic="$SYS/brokers/+/clients/+/disconnected")
# mc.subscribe(topic="$SYS/broker/+/clients/+/disconnected")
mc.subscribe(topic="$SYS/brokers/+/clients/+/connected")
# mc.subscribe(topic="$SYS/broker/+/clients/#")
# mc.subscribe(topic="$SYS/broker/clients/connected")
# mc.subscribe(topic="$SYS/#")


def handle_message(a, b, c):
    print(c.topic)
    print(c.payload)


mc.on_message = handle_message

mc.loop_forever()
