from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from twisted.internet.defer import inlineCallbacks


class MyComponent(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("session ready")

        counter = 0
        while True:
            self.publish(u'de.yrrgarten.oncounter', counter)
            counter += 1
            yield sleep(1)
