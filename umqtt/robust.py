import utime
from . import simple
import gwlogging

class MQTTClient(simple.MQTTClient):

    DELAY = 2
    DEBUG = True

    def delay(self, i):
        utime.sleep(self.DELAY)

    def disconnect(self):
        super().disconnect()

    def log(self, in_reconnect, e):
        if self.DEBUG:
            if in_reconnect:
                gwlogging.sendLog(gwlogging.DEBUG, ("mqtt reconnect: %r" % e), "MQTT")
                #print("mqtt reconnect: %r" % e)
            else:
                gwlogging.sendLog(gwlogging.DEBUG, ("mqtt: %r" % e), "MQTT")

    def reconnect(self):
        i = 0
        while 1:
            try:
                return super().connect(False)
            except OSError as e:
                self.log(True, e)
                i += 1
                self.delay(i)

    def publish(self, topic, msg, retain=False, qos=0):
        while 1:
            try:
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                self.log(False, e)
            self.reconnect()

    def wait_msg(self):
        while 1:
            try:
                return super().wait_msg()
            except OSError as e:
                self.log(False, e)
            self.reconnect()

    def check_msg(self):
        while 1:
            try:
                return super().check_msg()
            except OSError as e:
                self.log(False, e)
            self.reconnect()
