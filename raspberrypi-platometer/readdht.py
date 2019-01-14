
#!/usr/bin/python
import sys
import Adafruit_DHT
import os
import glob
import time
import requests

def dht11():
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	return humidity, temperature
