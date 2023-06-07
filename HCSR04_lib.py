#!/usr/bin/env python3
"""
"THE DIETCOKE LICENSE" (Revision 01):
uone wrote this code. As long as you retain this notice,
you can do whatever you want with this stuff. If we
meet someday, and you think this stuff is worth it, you can
buy me a bottle of diet coke in return.
Since I don't like beer and sugar, I don't use Beerware License.

uone http://homepages.rpi.edu/~wangy52
"""

import RPi.GPIO as GPIO
import time

class HCSR04:

    def __init__(self, TRIG_pin, ECHO_pin):
        self.TRIG_pin = TRIG_pin
        self.ECHO_pin = ECHO_pin
        self.__initialized = False
        self.SOUND_SPEED = 34300 # cm/sec

    def init_HCSR04(self):
        # set Trig port to be output
        # set Echo port to be input
        GPIO.setup(self.TRIG_pin, GPIO.OUT)
        GPIO.setup(self.ECHO_pin, GPIO.IN)

        # set Trig to be low
        GPIO.output(self.TRIG_pin, False)
        time.sleep(0.080) #
        # print("sensor is ready")
        self.__initialized = True

    def measure_distance(self):
        if self.__initialized == False:
            self.init_HCSR04()

        # send a 10usec gate signal to Trig
        GPIO.output(self.TRIG_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_pin, False)

        # when the wave is sent, ECHO reads 1
        pulse_start = time.time()
        while GPIO.input(self.ECHO_pin) == 0:
            pulse_start = time.time()

        # when the wave is heard, ECHO reads 0
        pulse_end = time.time()
        while GPIO.input(self.ECHO_pin) == 1:
            pulse_end = time.time()

        pulse_travel_time = pulse_end - pulse_start
        distance = pulse_travel_time * self.SOUND_SPEED / 2 # in unit cm
        time.sleep(0.080)
        return distance
