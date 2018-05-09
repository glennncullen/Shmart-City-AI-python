import json
import traceback
import uuid
import sys
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception import AWSIoTExceptions

# set up AWS IoT MQTT
myMQTTClient = AWSIoTMQTTClient(str(uuid.uuid1()))  # Add client ID
myMQTTClient.configureEndpoint("a3oazwlb9g85vu.iot.us-east-2.amazonaws.com", 8883)  # endpoint
myMQTTClient.configureCredentials("/Users/glennncullen/PycharmProjects/ShmartCity/app/communication/credentials/root.pem",
                                  "/Users/glennncullen/PycharmProjects/ShmartCity/app/communication/credentials/cdbd424344-private.pem.key",
                                  "/Users/glennncullen/PycharmProjects/ShmartCity/app/communication/credentials/cdbd424344-certificate.pem.crt")  # Add paths (CA, private key, cert)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # Disconnect at 10 seconds
myMQTTClient.configureMQTTOperationTimeout(5)  # Operation timeout 5 seconds
# connect to AWS IoT MQTT
try:
    myMQTTClient.connect()
except AWSIoTExceptions:
    print("unable to connect MQTT")
    traceback.print_exc()


def subscribe_callback(client, userdata, message):
    try:
        json_message = json.loads(message.payload)
        print message.payload
    except ValueError:
        print "Unable to decode json for subscribe_callback\n\tIncoming Message:%s" % message.payload


if myMQTTClient.subscribe("/shmartcity/#", 1, subscribe_callback):
    print("subscribed to /shmartcity/#")

while True:
    try:
        time.sleep(2)
        sending = {"test": "this"}
        myMQTTClient.publish("/shmartcity/test/", json.dumps(sending), 1)
    except KeyboardInterrupt:
        sys.exit()
