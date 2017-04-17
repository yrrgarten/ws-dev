from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.twisted.util import sleep
from twisted.internet.defer import inlineCallbacks
import get_temp, config

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

if __name__ == '__main__':
    runner = ApplicationRunner(
        url=u"ws://" + config.mycrossbar['host'] + ":8080/ws",
        realm=u"aquarasp",
        extra=dict(
            max_events=5000,  # [A] pass in additional configuration
        ),
    )
    print(runner.log)
    runner.run(MyComponent)
