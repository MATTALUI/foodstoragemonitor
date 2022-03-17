from datetime import datetime
from threading import Thread
from time import sleep
from gpiozero import LED, Button


class HardwareManager:
    # PIN CONSTANTS
    PIN_RED   = 17
    PIN_GREEN = 27
    PIN_BLUE  = 22
    PIN_BTN   = 18

    def __init__(self):
        self._last_maintainance = datetime.now()
        self._awaiting_button_press = False
        self._led_red = LED(HardwareManager.PIN_RED)
        self._led_green = LED(HardwareManager.PIN_GREEN)
        self._led_blue = LED(HardwareManager.PIN_BLUE)
        self._btn = Button(HardwareManager.PIN_BTN)
        self._start_thread(self._start_general_button)

    def _clear_led(self):
        self._led_red.off()
        self._led_green.off()
        self._led_blue.off()

    def _set_led_red(self):
        self._clear_led()
        self._led_red.on()

    def _set_led_green(self):
        self._clear_led()
        self._led_green.on()

    def _set_led_blue(self):
        self._clear_led()
        self._led_blue.on()

    def _led_test(self):
        self._set_led_red()
        sleep(1)
        self._set_led_green()
        sleep(1)
        self._set_led_blue()
        sleep(1)
        self._clear_led()

    def _start_general_button(self):
        while True:
            # If we're awaiting specific feedback we don't care about
            #general button presses.
            if self._awaiting_button_press:
                continue
            self._btn.wait_for_press()
            self._led_test()
            self._btn.wait_for_release()

    def _await_button_press(self):
        # TODO: Wait for button press
        self._awaiting_button_press = True
        self._awaiting_button_press = False

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
