import sys
import time
import client
import controller

initial_time = time.time()

def get_current_time():
    return (time.time() - initial_time) * 1000
def client_main(args):

    print("initializing controllers...")
    controller_instance = controller.Controller()
    client_instance = client.Client(1, 8080, 2, controller_instance)

    print("connection successful")

    loop_time = int(args[1])
    position_threshold = int(args[2])
    prev_time = 0
    print("starting runtime loop, with loop time {}".format(loop_time))

    while 1:
        cur_time = get_current_time()
        dt = cur_time - prev_time

        if dt >= loop_time:
            client_instance.update()
            controller_instance.update()
            if controller_instance.error <= position_threshold:
                client_instance.send_data('complete')

            prev_time = cur_time

if __name__ == "__main__":
    client_main(sys.argv)