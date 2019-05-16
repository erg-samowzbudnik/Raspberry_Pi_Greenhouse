[water]
trigers_sensors = False
trigers_clock = False
trigers_off = True
soil_moisture_treschold_min = 0
soil_moisture_treschold_max = 0
time_of_watering = 05:00
bool_period = True
time_watering_duration = 6:30
bool_amount = True
amount = 0
bool_normalise = False
bool_alert = True
bool_manual = True

[temperature]
trigers_sensors = False
trigers_clock = False
trigers_off = True
temp_max = 40
temp_min = 5
time_heating_on = 5:00
time_heating_off = 5:30
time_venting_on = 11:00
time_venting_off = 14:00
bool_normalise = True
bool_alert = True
bool_heating_manual = True
bool_venting_manual = True

[humidity]
trigers_sensors = False
trigers_off = True
humidity_max = 0
humidity_min = 0
bool_vent = False
bool_restrict_water = False
bool_normalise = True
bool_alert = True

[light]
trigers_sensors = False
trigers_clock = False
trigers_off = True
light_min = 112
light_max = 200
rgb_red = 250
rgb_green = 255
rgb_blue = 255
bool_normalise = True
bool_alert = True
time_on = 05:00
time_off = 20:20
bool_manual_on = False
bool_manual_off = True

[hardware_settings]
read_frequency = 55
kp = 1.0
ki = 0.0
kd = 0.0

