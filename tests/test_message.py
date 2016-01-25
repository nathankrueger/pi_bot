import sys
sys.path.append("../common")
import message

pm = message.print_messager()
pm.warning("Test warning!")
pm.info("Test info!")
pm.debug("Test debug!")
pm.error("Test error!")
