from time import sleep

from microdot import Microdot

import uasyncio
import machine
import network

import sidra

name = "Ciderhouse"
version = "0.1-alpha"

cfg = {
    "name": "Ciderhouse",
    "version": "0.1-alpha",
    "wlan": {
        "max_wait": 10,
        "ssid": "SKYEMWQE",
        "passwd": "wmK8cvxUu8Ak"
    },
    "server": {
        "port": 5000
    }
}

def app_string():
    return f"{cfg["name"]} [{cfg["version"]}]: "

app = Microdot()
monitor = sidra.Sidra()

def init_led():
    led = machine.Pin("LED", mode=machine.Pin.OUT)
    led.off()
    return led

def boot_test_routine():
    led = init_led()
    print(f"{app_string()} Settting pico LED state to off, then blinking...", end='')
    led.on()
    sleep(1)
    led.off()
    print(f"{app_string()} boot rest routine complete")

def connect_wlan(config):
    led = init_led()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print(f"{app_string()} Attempting to connect to WLAN %s" % config["wlan"]["ssid"])
    wlan.connect(config["wlan"]["ssid"], config["wlan"]["passwd"])

    max_wait = config["wlan"]["max_wait"]
    print(f"{app_string()} Max waiting time: approx {max_wait}s")

    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        flash(led, 0.5, 0.5)
        sleep(1)

    stat = wlan.status()

    # Handle connection error
    if stat == network.STAT_GOT_IP:
        post_connect(wlan)
    else:
        print(f"\n{app_string()} Unknown error condition: {wlan.status()}, {explain_wlan(wlan)}")

#
def flash(led, period=0.5, duty=0.5):
    """
    flash the onboard LED with a full cycle time of *period*, lighting the led for *duty* * *period*

    :param led: the led to flash, generally retrieved from machine.Pin
    :param period: the period (in seconds) for this flash iteration
    :param duty: the fraction of the period that the LED is to be lit

    """
    led.on()
    sleep(period*duty)
    led.off()
    sleep(period*(1.0-duty))

def post_connect(wlan):
    """
    Carry out post-wlan connection logging and any other checks
    :param wlan: the wlan object
    :return:
    """
    led = init_led()
    i = 0

    while i < 3:
        i += 1
        flash(led, period=1.0, duty=0.2)

    status = wlan.ifconfig()
    print(f"{app_string()} IP assigned as {status[0]}")

    led.on() # mark us as connected
    print(f"{app_string()} Ready to receive requests.")

def explain_wlan(wlan):
    if wlan.status() == network.STAT_CONNECT_FAIL:
        return "STAT_CONNECT_FAIL: unable to connect to WLAN"
    if wlan.status() == network.STAT_WRONG_PASSWORD:
        return "STAT_WRONG_PASSWORD: wrong password - check your credentials"
    if wlan.status() == network.STAT_NO_AP_FOUND:
        return "STAT_NO_AP_FOUND: no access point found"
    else:
        return "Unknown connection error."

#------------------------------------------------------------------------------
# Microdot application configuration

@app.route('/')
async def index(request):
    return f"""
    <!doctype html>
    <title>{name}</title>
    <body>
        <h4>{app_string()}</h4>
        <div>
        Making delicious cidery nom-noms since 2025.
        </div>
    </body>
    """, {"Content-Type": "text/html"}

@app.route('/metrics')
async def metrics(request):
    appname="ciderhouse"
    relaytype="HL8SL-DC5V-S-C"

    return f"""
    # HELP {appname}_led_status Status gauge for pico onboard led
    # TYPE {appname}_led_status gauge
    {appname}_led_status{{led="LED"}} {machine.Pin("LED", mode=machine.Pin.OUT).value()}
    {appname}_led_status{{led="RED",pin="{monitor.LED_PIN_RED}"}} {machine.Pin(monitor.LED_PIN_RED, mode=machine.Pin.OUT).value()}
    {appname}_led_status{{led="GREEN",pin="{monitor.LED_PIN_GREEN}"}} {machine.Pin(monitor.LED_PIN_GREEN, mode=machine.Pin.OUT).value()}
    {appname}_led_status{{led="BLUE",pin="{monitor.LED_PIN_BLUE}"}} {machine.Pin(monitor.LED_PIN_BLUE, mode=machine.Pin.OUT).value()}
    
    # HELP {appname}_sensor_temperature Temperature gauge for DS18B20 sensor which should be in the fermentation vessel
    # TYPE {appname}_sensor_temperature gauge
    {appname}_sensor_temperature{{type="digital",model="ds18b20",pin="{monitor.TEMPERATURE_IN}"}} {monitor.last}
    
    # HELP {appname}_relay_state State of a relay on the fermentation chamber control circuit
    # TYPE {appname}_relay_state gauge
    {appname}_relay_state{{model="{relaytype}",pin="{monitor.COOLING_RELAY}"}} {machine.Pin(monitor.COOLING_RELAY, mode=machine.Pin.OUT).value()}
    {appname}_relay_state{{model="{relaytype}",pin="{monitor.HEATING_RELAY}"}} {machine.Pin(monitor.HEATING_RELAY, mode=machine.Pin.OUT).value()}
    
    """, {"Content-Type": "text/plain"}

async def main():
    # start the server in a background task
    uasyncio.create_task(monitor.monitor())
    uasyncio.create_task(app.run(port=cfg["server"]["port"]))
    while(True):
        await uasyncio.sleep(100)


if __name__ == '__main__':

    monitor.boot_test()
    boot_test_routine()

    connect_wlan(cfg)
    uasyncio.run(main())

