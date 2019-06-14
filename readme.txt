Software for monitoring and managing hardware of the greenhouse and weather
station.
Hardware is defined although effort will be made, perhaps, at some point,
to enable using different sensors and control hardware.


1. Hardware

For now the setup consists of:

- RPi3+
# - 24V car battery

sensors:

- 1w (one wire) temperature sensors
- DHT11 temperature/humidity sensor
- tsl2561 light sensor
- soil humidity sensors
- rain gauge
# - water flow meter

controls:

- RGB LED strip
# - DAC MCP4725 from Adafruit (digital-to-analog converter)(not needed if
we're to use PWM instead)
 - fan or a servo motor (for opening a window)
# - solenoid valve
# - heater: not implementing as I have, for now, no use for it. Perhaps alarm
 would sufice for temperature drop.

2. Software:

Written in Python3 with Qt5 frontend. Consists of: monitor daemon, control
daemon, main program with gui.

prerequisites:
# for DHT11, DHT22 or AM2302:
pip install Adafruit_DHT && cd Adafruit_DHT && python setup.py install
# for tsl2561:
pip install adafruit-circuitpython-tsl2561
# we need this:
pip install schedule


3. Random notes:

- for controling higher voltages we can use one of three solutions: MOSFET, PWM
  or DAC. MOSFET gives us on/of. For our applications (lighting, heating,
  venting) we'd rather use gradual voltage control. Hence PWM or DAC. DAC
  requires extra hardware component. PWM requires us to keep in mind frequency
  and duty cycle. Settling for PWM. 
