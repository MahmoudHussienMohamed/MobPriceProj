import requests
URL = 'http://localhost:9292/MobPriceCls/api'
DEVICES_URL = URL + '/devices'
PREDICTION_URL = URL + '/predict'

def get_all_devices():
    response = requests.get(DEVICES_URL)
    return response.json()

def get_device(id):
    response = requests.get(f'{DEVICES_URL}/{id}')
    return response.json()

def add_device(device):
    response = requests.post(DEVICES_URL, json=device)
    return response.json()

def predict_device(id):
    response = requests.post(f'{PREDICTION_URL}/{id}')
    return response.json()

payload = {'battery_power': 842.0, 'blue': 0.0, 'clock_speed': 2.2, 'dual_sim': 0.0, 'fc': 1.0, 'four_g': 0.0, 'int_memory': 7.0, 'm_dep': 0.6, 'mobile_wt': 188.0, 'n_cores': 2.0, 'pc': 2.0, 'px_height': 20.0, 'px_width': 756.0, 'ram': 2549.0, 'sc_h': 9.0, 'sc_w': 7.0, 'talk_time': 19.0, 'three_g': 0.0, 'touch_screen': 0.0, 'wifi': 1.0}
device_id = '663507d63ad75c336e8a3567'

print(add_device(payload))
print(get_all_devices())
print(get_device(device_id))
print(predict_device(device_id))


