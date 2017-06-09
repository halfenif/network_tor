from stem import Signal
from stem.control import Controller
import time
import z_utils #stackoverflow copy



def display_state():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()

        bytes_read = int(controller.get_info('traffic/read'))
        bytes_written = int(controller.get_info('traffic/written'))

        print('[%s] R %s / W %s' % (time.strftime("%x %X") ,z_utils.humanbytes(bytes_read), z_utils.humanbytes(bytes_written)))

#---------------------------------
# Main
if __name__ == "__main__":
    while(True):
        display_state()
        time.sleep(10)
