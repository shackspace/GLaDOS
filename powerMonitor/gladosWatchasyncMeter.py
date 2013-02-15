#!/usr/bin/python

import cgi
import redis
import time


now = int(time.time())

channelNameForPulses = "Pulse"
channelNameForPowerReading = "Power"
meterSerial = cgi.FieldStorage()['meter'].value
baseKeyData = "sensordata.shackspace." + meterSerial + ".data."
baseKeyConf = "sensordata.shackspace." + meterSerial + ".config.sensors"
PULSES_PER_KWH = 800; # the energy meter does things like this


def storeSensorValueInRedis(baseKeyData, channelName, timestamp, value):
  "stores a sensor reading in redis"
  value = "[" + str(timestamp) + "," + str(value) + "]"
  redisConnection.rpush(baseKeyData + channelName, value)
  return

def storePulseInRedis(baseKeyData, channelName, timestamp):
  "stores a sensor reading in redis"
  value = "["+ str(timestamp) +"]"
  redisConnection.rpush(baseKeyData + channelName, value)
  return

def storeSensorConfigurationInRedis(baseKeyConf, powerChannelName, pulseChannelName):
  "stores the configuration for the power meter in redis"
  value = "{ \""+ powerChannelName +"\": { \"unit\": \"W\", \"type\": \"actual\"}, \""+ pulseChannelName +"\": { \"unit\": \"s\", \"type\": \"event\" }}";
  redisConnection.set(baseKeyConf, value)
  return

# connect to the redis server
redisConnection = redis.Redis("localhost")
storeSensorConfigurationInRedis(baseKeyConf, channelNameForPowerReading, channelNameForPulses)

# we got a pulse now, check when the last pulses were.
storePulseInRedis(baseKeyData, channelNameForPulses, now)

# get the last samples from redis
data = redisConnection.lrange(baseKeyData + channelNameForPulses, -8, -1);

# calculate the average pulse time.
sample = 0
for key in range(1,8):
   value = ( int(data[key].strip("[]")) - int(data[key-1].strip("[]")) );
   sample += value
averagePulseTime = sample / 7.0
measurementTime = int(data[7].strip("[]")) - int(data[0].strip("[]"));

# calculate the aprox power consumption
pulsesPerHour = 3600 / averagePulseTime
powerConsumption = int((1000 * pulsesPerHour) / PULSES_PER_KWH);

# store the power consumption data.
storeSensorValueInRedis(baseKeyData, channelNameForPowerReading, now, powerConsumption);

