# cool led

# warm led
from time import sleep
import utime

import machine
import ds18x20
import onewire

import uasyncio

class Sidra:
    """
    Class Sidra

    Fermentation management and alerting engine for Apple cider.  Reads temperature from a digital DS18B20 waterproof thermometer
    which should be immersed in the fermentation vat
    """

    LED_PIN_RED = "GP4"
    LED_PIN_GREEN = "GP3"
    LED_PIN_BLUE = "GP2"

    TEMPERATURE_IN = "GP8"

    COOLING_RELAY = "GP6"
    HEATING_RELAY = "GP7"

    HEATING = False
    COOLING = False

    LEVELS = {
        "cold": 13,
        "cool": 16,
        "normal": 20,
        "warm": 22
    }

    last = 100.0

    def red(self):
        """
        Turn on the red led
        :param state:
        :return:
        """
        self.outpin(Sidra.LED_PIN_RED).on()

    def green(self):
        """
        Turn on the green led
        :return:
        """
        self.outpin(Sidra.LED_PIN_GREEN).on()

    def blue(self):
        """
        Turn on the blue led
        :return:
        """
        self.outpin(Sidra.LED_PIN_BLUE).on()

    def outpin(self, id):#
        """
        Returns a reference to gpio digital output pin
        :param id: the id of the pin to reference
        :return: a reference to the pin named by id
        """
        return machine.Pin(id, machine.Pin.OUT)

    def amber(self):
        """
        Light the LED to amber by turning on red and green
        """
        self.red()
        self.green()

    def cyan(self):
        """
        Light the LED to cyan by turning on the green and blue leds
        """
        self.green()
        self.blue()

    def douse(self):
        """
        Turn off the status LED
        :return:
        """
        self.outpin(Sidra.LED_PIN_RED).off()
        self.outpin(Sidra.LED_PIN_GREEN).off()
        self.outpin(Sidra.LED_PIN_BLUE).off()

    def enable_heater(self):
        """
        Turn on the fermentation chamber heating circuit.
        :return:
        """
        self.outpin(Sidra.HEATING_RELAY).on()

    def disable_heater(self):
        """
        Turn off the heating relay circuit.
        :return:
        """
        self.outpin(Sidra.HEATING_RELAY).off()

    def enable_fan(self):
        """
        Turn on the fermentation chamber fan circuit.
        :return:
        """
        self.outpin(Sidra.COOLING_RELAY).on()

    def disable_fan(self):
        """
        Turn off the fermentation chamber fan circuit.
        :return:
        """
        self.outpin(Sidra.COOLING_RELAY).off()

    def visualise(self, val):
        self.douse()

        if val < self.LEVELS["cold"]:
            self.blue()
        elif val < self.LEVELS["cool"]:
            self.cyan()
        elif val < self.LEVELS["normal"]:
            self.green()
        elif val < self.LEVELS["warm"]:
            self.amber()
        else:
            self.red()

    def temperature_control_loop(self, val):
        if val >= self.LEVELS["warm"]:
            # print(".1")
            self.COOLING = True
        else:
            # print(".2")
            self.COOLING = False

        if val < self.LEVELS["cool"]:
            # print(".3")
            self.HEATING = True
        else:
            # print(".4")
            self.HEATING = False

        if self.HEATING:
            self.enable_heater()
        else:
            self.disable_heater()

        if self.COOLING:
            self.enable_fan()
        else:
            self.disable_fan()

    def get_temp(self):
        # print("Getting temperature")

        try:
            sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(self.TEMPERATURE_IN)))
            # print("got sensor, scanning")
            d = ""
            t = 0
            roms = sensor.scan()
            # print("scanned, counting length")
            sensor_count = len(roms)
            # print(str(sensor_count) + " temp sensors found")

            if sensor_count > 0:
                sensor.convert_temp()
                utime.sleep(0.5)
                for rom in roms:
                    d = hex(int.from_bytes(rom, 'little'))
                    t = sensor.read_temp(rom)
                    utime.sleep_ms(100)

            return d, t
        except Exception as e:
            print(f"Error reading temperature sensor %s", e)
            raise e


    def tick(self):
        """
        Perform an interation of the monitoring heartbeat
        :return:
        """
        try:
            self.last = self.get_temp()[1]
            self.visualise(self.last)
            self.temperature_control_loop(self.last)
        except Exception as e:
            print(f"Error reading temperature sensor %s", e)
            raise e

    def boot_test(self):
        self.douse()
        sleep(0.2)

        self.red()
        sleep(0.5)
        self.douse()

        self.amber()
        sleep(0.5)
        self.douse()

        self.green()
        sleep(0.5)
        self.douse()

        self.cyan()
        sleep(0.5)
        self.douse()

        self.blue()
        sleep(0.5)
        self.douse()

        self.disable_heater()
        self.disable_fan()

    async def monitor(self):
        while True:
            self.tick()
            await uasyncio.sleep(5)
