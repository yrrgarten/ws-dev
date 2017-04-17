from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from twisted.internet.defer import inlineCallbacks
import get_temp

class MyComponent(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("session ready")

        temp, temp_t  = get_temp.read_temperature('/sys/bus/w1/devices/28-031600954bff/w1_slave')
        temp_act = temp
        self.publish(u'de.yrrgarten.temp_act', temp_act)
        # select max(metered_temp), min(metered_temp) from metered_values where time_of_measurement >= now() - '1 day'::INTERVAL;

        while True:
            temp, temp_t  = get_temp.read_temperature('/sys/bus/w1/devices/28-031600954bff/w1_slave')
            try:
                if (abs(temp - temp_act) > 0.01):
                    temp_act = temp
                    self.publish(u'de.yrrgarten.temp_act', temp_act)
            except:
                temp_act = temp
                self.publish(u'de.yrrgarten.temp_act', temp_act)

            #self.publish(u'de.yrrgarten.temp_act', temp)
            yield sleep(1)
