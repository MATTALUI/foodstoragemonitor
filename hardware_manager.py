from datetime import datetime
from threading import Thread
from multiprocessing import Process
from time import sleep

# We wrap this guy in an import check because gpiozero is an rpi-specific
# package, so it doesn't really make sense to install on non-rpi machines
try:
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
            self._magical_process = None
            # self._start_thread(self._start_general_button)

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

        def _set_led_yellow(self):
            self._clear_led()
            self._led_red.on()
            self._led_green.on()

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
                self._btn.wait_for_press()
                self._btn.wait_for_release()
                # If we're awaiting specific feedback we don't care about
                #general button presses.
                if self._awaiting_button_press:
                    continue
                self._led_test()

        def _await_button_press(self):
            self._btn.wait_for_press()
            self._btn.wait_for_release()
            self._clear_led()
            sleep(1)
            self._awaiting_button_press = False

        def _start_button_press_thread(self):
            if self._awaiting_button_press:
                return
            self._start_thread(self._await_button_press)

        def _start_thread(self, action, args=()):
            self._magical_process = Process(target = action, args=args)
            self._magical_process.start()

        def run_test(self):
            self._start_thread(self._led_test)

        def reset(self):
            if self._magical_process is not None:
                self._magical_process.terminate()
                self._magical_process = None
            self._clear_led()

        def accept_report(self, expiry_report):
            await_cancel = False
            if expiry_report['expired'] > 0:
                self._set_led_red()
                await_cancel = True
            elif expiry_report['warning'] > 0:
                self._set_led_yellow()
                await_cancel = True
            elif expiry_report['highlight'] > 0:
                self._set_led_blue()
                await_cancel = True
            if await_cancel:
                self._awaiting_button_press = True
                self._start_thread(self._await_button_press)


except ImportError:
    class HardwareManager:
        def run_test(self):
            pass

        def accept_report(self, expiry_report):
            pass

        def reset(self):
            pass

hardware_manager = HardwareManager()
