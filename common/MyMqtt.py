""" Extension of the Mqtt class from flask_mqtt  """

from flask_mqtt import Mqtt


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

class MyMqtt(Mqtt):
    """ Extension of the Mqtt class from flask_mqtt  """

    def __init__(self, app=None):
        Mqtt.__init__(self, app)

    def message_callback_add(self, topic, callback):
        """Register a message callback for a specific topic.
        Messages that match 'sub' will be passed to 'callback'. Any
        non-matching messages will be passed to the default on_message
        callback."""
        self.client.message_callback_add(topic, callback)

    def message_callback_remove(self, topic):
        """Remove a message callback previously registered with
        message_callback_add()."""
        self.client.message_callback_remove(topic)

#
