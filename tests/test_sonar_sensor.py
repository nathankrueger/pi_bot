import sys
sys.path.append('../sensor/')
sys.path.append('../common/')

import time
import sonar_sensor

def main():
	msgr = message.print_messager()
	ss = sonar_sensor.sonar_sensor('/dev/ttyAMA0', 'test sonar sensor', .01, msgr)
	ss.init()
	ss.start()

	try:
		while True:
			print ss.value
			time.sleep(.1)
	except KeyboardInterrupt:
		ss.stop()

if __name__ == '__main__':
	main()
