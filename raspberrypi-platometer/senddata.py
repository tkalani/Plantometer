import requests
import readus
import readdht
import rfa
import readus2
import actuator
import actuator2


url = 'http://plantometer.pythonanywhere.com/sensors/logdata/'

dhtdat = readdht.dht11()
ard = rfa.read()
data1 = {
        'humidity' :dhtdat[0],
        'temp' :dhtdat[1],
        'distance' : readus.distance(),
        'soilmoist' : ard[0],
        'pressure' : str(100067.0938457),
        'altitude' : str(67),
        'seapressure': str(100052.48578),
        'rain': ard[2],
        'user_id': 5,
        'plant_id': 70,
        }
data2 = {
        'humidity' :dhtdat[0],
        'temp' :dhtdat[1],
	'distance':readus2.distance(),
	'soilmoist':ard[1],
        'pressure' : str(100067.0938457),
        'altitude' : str(67),
        'seapressure': str(100052.48578),
        'rain': ard[2],
        'user_id': 5,
        'plant_id': 71,
        }
print(data1)
print(data2)
try:
	r1 = requests.post(url, data=data1)
	r2 = requests.post(url, data=data2)
	print(list(r1)[:5], list(r2)[:5])
except:
	print('failed')
