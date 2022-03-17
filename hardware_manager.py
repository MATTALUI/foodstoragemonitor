from datetime import datetime
from threading import Thread
from time import sleep


class HardwareManager:
    # PIN CONSTANTS
    PIN_RED = 17
    PIN_GREEN = 27
    PIN_BLUE = 22

    def __init__(self):
        self._last_maintainance = datetime.now()
        self._awaiting_button_press = False

    def _led_test(self):
        print("running led test")
        print("done testing leds")

    def _await_button_press(self):
        # TODO: Wait for button press
        self._awaiting_button_press = True
        print("Waiting for button press...")
        self._awaiting_button_press = False
        print("All done!")

    def _start_button_press_thread(self):
        if self._awaiting_button_press:
            return
        self._start_thread(self._await_button_press)

    def _start_thread(self, action, args=()):
        Thread(target = action, args=args).start()

    def run_test(self):
        self._start_thread(self._led_test)

    def accept_report(self, expiry_report):
        self._start_button_press_thread()
        if expiry_report['expired'] > 0:
            print('expired')
        elif expiry_report['warning'] > 0:
            print('warning')
        elif expiry_report['highlight'] > 0:
            print('highlight')

hardware_manager = HardwareManager()
