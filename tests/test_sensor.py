import sys
sys.path.append("../common")
sys.path.append("../sensor")
import sensor
import message

import time

pm = message.print_messager()
foo = sensor.sensor("Test sensor", .01, pm)
foo.init()
foo.start()
time.sleep(1)
foo.stop()
