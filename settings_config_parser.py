[water]
trigers_sensors = False
trigers_clock = False
trigers_off = True
soil_moisture_min = 0
soil_moisture_max = 0
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
temp_max = 6
temp_min = 40
time_heating_on = 5:00
time_heating_off = 5:30
time_venting_on = 11:00
time_venting_off = 14:00
# bool_normalise = True
bool_alert = True
bool_heating_manual = True
bool_venting_manual = True
kp = 1.0
ki = 0.0
kd = 0.0
temp_vent_on = 08:00

[humidity]
trigers_sensors = False
trigers_off = True
humidity_max = 0
humidity_min = 0
bool_vent = False
bool_restrict_water = False
# bool_normalise = True
bool_alert = True

[light]
trigers_sensors = False
trigers_clock = False
trigers_off = True
light_min = 103
light_max = 309
rgb_red = 250
rgb_green = 255
rgb_blue = 255
# bool_normalise = True
bool_alert = True
time_on = 05:00
time_off = 20:20
bool_manual = False
kp = 1.0
ki = 0.0
kd = 0.0
light_rgb_red = 249
light_time_on = 23:00
light_time_off = 23:22

[alerts]
bool_on_screen = True
text_on_screen = 'Danger Will Robinson!'
bool_sound = False
path_sound = './sound/alert.mp3'
bool_sms = False
sms_number = '997'
bool_email = False
email_address = 'your_email@goes.here'

[manual]
bool_light_on = False
bool_light_off = True
bool_water_on = False
bool_water_off = True
bool_heating_on = False
bool_heating_off = True
bool_vent_on = False
bool_vent_off = True

[hardware_settings]
read_frequency = 55
dht_pin_1 = 1
dht_pin_2 = None
tsl2561_pin = None

