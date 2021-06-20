import paho.mqtt.client as mqtt
import json
import struct
import requests

username = "leisure-guardian-api"
password = "NNSXS.WPYYTTVGJCF3QVV24AUXNQROZWBIOHW62J4RGGY.HCBUYEGVDP62DHMPCREMWXVXYN2DFPJBW3K23FH2FWND2YJVYLUA"

print("started")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('#')


def zeroTodoubleZero(string):
    if str(hex(string))[2:] == "0":
        return "00"
    else:
        return str(hex(string))[2:]


def on_message(client, userdata, msg):
    dict_string = msg.payload
    diction = json.loads(dict_string)
    try:
        device_serial = diction["end_device_ids"]["device_id"]
        device_serial = int(device_serial)
        diction = diction["uplink_message"]["decoded_payload"]["bytes"]
    except KeyError:
        print("join??")
        return
    string = ""
    iter = 0
    try:
        string = zeroTodoubleZero(diction[3])
        string = string + zeroTodoubleZero(diction[2])
        string = string + zeroTodoubleZero(diction[1])
        string = string + zeroTodoubleZero(diction[0])
        try:
            ax = struct.unpack('!f', bytes.fromhex(string))[0]
        except ValueError:
            ax = 0.0
        print("ax : " + str(ax))
        string = zeroTodoubleZero(diction[7])
        string = string + zeroTodoubleZero(diction[6])
        string = string + zeroTodoubleZero(diction[5])
        string = string + zeroTodoubleZero(diction[4])
        try:
            ay = struct.unpack('!f', bytes.fromhex(string))[0]
        except ValueError:
            ay = 0.0
        print("ay : " + str(ay))
        string = zeroTodoubleZero(diction[11])
        string = string + zeroTodoubleZero(diction[10])
        string = string + zeroTodoubleZero(diction[9])
        string = string + zeroTodoubleZero(diction[8])
        try:
            az = struct.unpack('!f', bytes.fromhex(string))[0]
        except ValueError:
            az = 0.0
        print("az : " + str(az))
        string = zeroTodoubleZero(diction[15])
        string = string + zeroTodoubleZero(diction[14])
        string = string + zeroTodoubleZero(diction[13])
        string = string + zeroTodoubleZero(diction[12])
        try:
            lat = struct.unpack('!f', bytes.fromhex(string))[0]
        except ValueError:
            lat = float(string)
        print("lat : " + str(lat))
        string = zeroTodoubleZero(diction[19])
        string = string + zeroTodoubleZero(diction[18])
        string = string + zeroTodoubleZero(diction[17])
        string = string + zeroTodoubleZero(diction[16])
        try:
            lon = struct.unpack('!f', bytes.fromhex(string))[0]
        except ValueError:
            lon = float(string)
        print("lon : " + str(lon))
        string = zeroTodoubleZero(diction[23])
        string = string + zeroTodoubleZero(diction[22])
        string = string + zeroTodoubleZero(diction[21])
        string = string + zeroTodoubleZero(diction[20])
        try:
            pulse = struct.unpack('!i', bytes.fromhex(string))[0]
        except ValueError:
            pulse = 60
        print("pulse : " + str(pulse))
        string = zeroTodoubleZero(diction[27])
        string = string + zeroTodoubleZero(diction[26])
        string = string + zeroTodoubleZero(diction[25])
        string = string + zeroTodoubleZero(diction[24])
        try:
            temperature = struct.unpack('!i', bytes.fromhex(string))[0]
        except ValueError:
            temperature = int(string)
        print("temperature : " + str(temperature))
        string = zeroTodoubleZero(diction[31])
        string = string + zeroTodoubleZero(diction[30])
        string = string + zeroTodoubleZero(diction[29])
        string = string + zeroTodoubleZero(diction[28])
        try:
            state = struct.unpack('!i', bytes.fromhex(string))[0]
        except ValueError:
            state = int(string)

        string = zeroTodoubleZero(diction[35])
        string = string + zeroTodoubleZero(diction[34])
        string = string + zeroTodoubleZero(diction[33])
        string = string + zeroTodoubleZero(diction[32])
        try:
            emergent = struct.unpack('!i', bytes.fromhex(string))[0]
        except ValueError:
            emergent = int(string)

        string = zeroTodoubleZero(diction[39])
        string = string + zeroTodoubleZero(diction[38])
        string = string + zeroTodoubleZero(diction[37])
        string = string + zeroTodoubleZero(diction[36])
        try:
            battery = struct.unpack('!i', bytes.fromhex(string))[0]
        except ValueError:
            battery = int(string)
        battery = int((battery - 3000) / 1135 * 100)
        print("battery : " + str(battery))
        accel = abs(ax) + abs(ay) + abs(az)
        print("eccel: " + str(accel))

        if pulse < 20 or pulse > 120:
            state = 2

        if accel > 13:
            state = 2

        print("state : " + str(state))
        print("emergent : " + str(emergent))
        deviceDataPost(device_serial, lon, lat, temperature,
                       accel, pulse, battery, state, emergent)
    except ValueError:
        deviceDataPost(device_serial, 0, 0, 0,
                       0, 0, 0, 0, 0)
        print("value error")
    except struct.error:
        print("struct err")


def deviceDataPost(deviceSerial, longitude, latitude, temp, accelMax, heartRate, batteryLevel, critical, button):
    baseurl = "http://mmyu.synology.me:8000/deviceData"
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}
    datas = {"deviceSerial": deviceSerial,
             "longitude": longitude,
             "latitude": latitude,
             "temp": temp,
             "accelMax": accelMax,
             "heartRate": heartRate,
             "batteryLevel": batteryLevel,
             "critical": critical,
             "button": button}
    res = requests.post(baseurl, headers=headers, json=datas)
    try:
        res.raise_for_status()
        print("post success")
    except:
        print(res.content)
        print(res.status_code)
        print("post error")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect("mmyu.synology.me", 1883)


client.loop_forever()
