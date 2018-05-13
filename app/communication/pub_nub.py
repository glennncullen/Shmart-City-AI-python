from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from app import main
from app.communication import aws


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():  # Message successfully published to specified channel
        return True
    else:
        print("failed to publish to %s" % status.category)
        return False
        # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


class PubNubHandler:
    def __init__(self):
        self.pnconfig = PNConfiguration()
        self.pnconfig.subscribe_key = 'sub-c-ec33873a-53d1-11e8-84ad-b20235bcb09b'
        self.pnconfig.publish_key = 'pub-c-56bfd71d-e6e9-479d-9c08-b2c719d6a4c7'
        self.pnconfig.secret_key = 'sec-c-OWY1ZDU0NGUtN2IyZC00YmJmLWFmNTEtOTc3NDFkYWE0YjUw'
        self.pubnub = PubNub(self.pnconfig)
        self.my_channels = [
            'all-roads',
            'update-congestion',
            'fire-in-progress',
            'update-position',
            'fire-extinguished'
        ]
        self.connected = False
        self.Subscribe()

    def Subscribe(self):
        callback = SCSubscribeCallback()
        self.pubnub.add_listener(callback)
        self.pubnub.subscribe().channels(self.my_channels).execute()
        while not callback.subscribed:
            if callback.failed:
                break
        self.connected = callback.subscribed

    def Publish(self, message, channel):
        if self.connected:
            if self.pubnub.publish().channel(channel).message(message).async(my_publish_callback):
                print("pubbed %s to %s" % message, channel)
        else:
            print("cannot publish while not connection -- trying to reconnect")
            self.pubnub.reconnect()


class SCSubscribeCallback(SubscribeCallback):

    def __init__(self):
        self.subscribed = False
        self.failed = False
        self.fire_in_progress = False

    def presence(self, pubnub, presence):
        pass  # must implement abstract method

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            self.failed = True
            self.subscribed = False

        elif status.category == PNStatusCategory.PNConnectedCategory:
            self.subscribed = True
            self.failed = False
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            self.subscribed = True
            self.failed = False

    def message(self, pubnub, message):
        # receive all roads
        if message.channel == 'all-roads':  # {num: {road details}, num {road details} ... }
            print message.channel, ": ", message.message
            main.build_city(message.message)
        # receive updated congestion
        if message.channel == 'update-congestion':  # message: {road: name, congestion: congestion}
            if not self.fire_in_progress:
                print message.channel, ": ", message.message
                main.update_congestion(message.message)
        # alert that a fire is in progress
        if message.channel == 'fire-in-progress':  # message: {start: road, end: road}
            print message.channel, ": ", message.message
            self.fire_in_progress = True
            response = main.calculate_best_route(message.message)
            for element in response:
                print element
            pubnub.publish().channel('route-to-fire').message(response).async(my_publish_callback)
            aws.publish(response, '/shmartcity/route/')
        # ambulance position has been updated
        if message.channel == 'update-position':  # message: {next: true}
            print message.channel, ": ", message.message
            aws.publish(message.message, '/shmartcity/nextroad/')
        # fire has been extinguished
        if message.channel == 'fire-extinguished':  # message: {extinguished: true}
            print message.channel, ": ", message.message
            aws.publish(message.message, '/shmartcity/extinguished/')
            self.fire_in_progress = False


PubNubHandler()
