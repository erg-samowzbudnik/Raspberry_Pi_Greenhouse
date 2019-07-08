[water]
trigers_sensors = False
trigers_clock = False
trigers_off = True
soil_moisture_min = 25
soil_moisture_max = 40
time_of_watering = 01:00
bool_period = True
time_watering_duration = 03:30
bool_amount = True
amount = 5
bool_normalise = False
bool_alert = True
bool_manual = True

[temperature]
trigers_sensors = False
trigers_clock = False
trigers_off = True
temp_max = 37
temp_min = 23
time_heating_on = 5:00
time_heating_off = 5:30
time_venting_on = 11:00
time_venting_off = 14:00
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
humidity_max = 35
humidity_min = 20
bool_vent = False
bool_restrict_water = False
bool_alert = True

[light]
trigers_sensors = False
trigers_clock = False
trigers_off = True
light_min = 2500
light_max = 4336
rgb_red = 250
rgb_green = 255
rgb_blue = 255
bool_alert = True
time_on = 05:00
time_off = 20:20
bool_manual = False
control_onof = False
control_pid = True
kp = 0.95
ki = 0.0
kd = 0.0
light_rgb_red = 249
light_time_on = 23:00
light_time_off = 23:22
light_kp = 2.0

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

