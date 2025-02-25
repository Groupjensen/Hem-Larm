import time

def mqtt_publisher(client, topics_messages):
    for topic, message in topics_messages.items():
        client.publish(topic, message, qos=0)
        print(f"Published message: {message} to topic: {topic}")
        time.sleep(2)
