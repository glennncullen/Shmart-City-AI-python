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
            'update-vehicle-position',
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
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            self.failed = True
            self.subscribed = False
            # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            self.subscribed = True
            self.failed = False
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            self.subscribed = True
            self.failed = False
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.

    def message(self, pubnub, message):
        print message.channel, ": ", message.message
        if message.channel == 'all-roads':  # {num: {road details}, num {road details} ... }
            main.build_city(message.message)
        if message.channel == 'update-congestion':  # message: {road: name, congestion: congestion}
            if not self.fire_in_progress:
                main.update_congestion(message.message)
        if message.channel == 'fire-in-progress':  # message: {start: road, end: road}
            self.fire_in_progress = True
            response = main.calculate_best_route(message.message)
            pubnub.publish().channel('route-to-fire').message(response).async(my_publish_callback)
            aws.publish(response, '/shmartcity/route/')
        if message.channel == 'update-ambulance-position':
            aws.publish(message.message, '/shmartcity/nextroad/')
        if message.channel == 'fire-extinguished':  # message: {extinguished: true}
            aws.publish(message.message, '/shmartcity/extinguished/')
            self.fire_in_progress = False


PubNubHandler()
