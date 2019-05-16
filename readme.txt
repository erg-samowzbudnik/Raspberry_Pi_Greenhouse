Software for managing and monitoring hardware of the greenhouse and weather
station.
Hardware is defined although effort will be made, perhaps, at some point,
to enable using different sensors and control hardware.

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
# - DAC MCP4725 from Adafruit (digital-to-analog converter)
# - solenoid valve
# - servo motor (for opening a window) or fan
# - heater: should be easy to add, I'm not implementing as I have, for now, no use
#   for it.

Software:

Written in Python3 with Qt5 frontend. Consists of: monitor daemon, control
daemon, main program with gui.

prerequisites:
pip install schedule
