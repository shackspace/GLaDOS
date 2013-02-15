#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket
import sys
import re
import time
import redis


def storeSensorValueInRedis(meterSerial, timestamp, channelName, value):
    "stores a sensor reading in redis."
    baseKey = "sensordata.shackspace." + meterSerial + ".data." + channelName
    score = timestamp
    value = "[" + timestamp + "," + re.sub("^0*", "", value) + "]";
    redisConnection.rpush(baseKey, value)
    return

def storeSensorConfigurationInRedis(meterSerial):
    "stores the sensor configuration in redis."
    baseKey = "sensordata.shackspace." + meterSerial + ".config.sensors"
    value = "{\"L1.Voltage\": {\"unit\": \"V\", \"type\":\"actual\"},\"L2.Voltage\": {\"unit\": \"V\", \"type\":\"actual\"},\"L3.Voltage\": {\"unit\": \"V\", \"type\":\"actual\"},\"L1.Current\": {\"unit\": \"A\", \"type\":\"actual\"},\"L2.Current\": {\"unit\": \"A\", \"type\":\"actual\"},\"L3.Current\": {\"unit\": \"A\", \"type\":\"actual\"},\"L1.Power\": {\"unit\": \"W\", \"type\":\"actual\"},\"L2.Power\": {\"unit\": \"W\", \"type\":\"actual\"},\"L3.Power\": {\"unit\": \"W\", \"type\":\"actual\"},\"Total\": {\"unit\": \"W\", \"type\":\"cummulative\"}}";

    redisConnection.set(baseKey, value)
    return

def readPowerMeterValue(server_adress):
    # Connect the socket to the port where the server is listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    
    try:
        # Look for the response
        amount_received = 0
        amount_expected = 23 # dirty hack but its okay since the powerraw device will close the connection for us
        data_received = ""
        while amount_received < amount_expected:
            data = sock.recv(25000)
            amount_received += len(data)
            data_received += data
        #    print >>sys.stderr, 'received "%s"' % data
    
    finally:
        sock.close()
    
    return data_received;


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to redis.
redisConnection = redis.Redis("glados.shack")

# define regex for parsing.
regexPower = re.compile("[+][0-9]+[*]")
regexCurrent = re.compile("[0-9.]+[*]A")
regexVoltage = re.compile("[0-9.]+[*]V")
regexReading = re.compile("1-0:1\.8\..\*255\(([0-9.]+)\)")
regexSerial = re.compile("1-0:0\.0\.0\*255\(([0-9]+)\)")
regexEpochTime = re.compile("\w[0-9]+\w{8,}")
server_address = ('powerraw.shack', 11111)
epochtime_old = 0

# read one sample to extract the serial of the 
data_received = readPowerMeterValue(server_address)
meterId = regexSerial.search(data_received).group(1)
storeSensorConfigurationInRedis(meterId);

# read the redis value
while True:
    # read a data sample.
    data_received = readPowerMeterValue(server_address)

    # check if it's a new value
    epochTime = regexEpochTime.findall(data_received)
    if epochtime_old != epochTime[0]:
        epochtime_old = epochTime[0]
        currents = regexCurrent.findall(data_received)
        voltages = regexVoltage.findall(data_received)
        powerUsage = regexPower.findall(data_received)
        totalReading = regexReading.search(data_received).groups()

        # create a json object with the data.
        for i in range(0,3):
          storeSensorValueInRedis(meterId, epochTime[0], "L"+str(1+i)+".Voltage", voltages[i].strip("*V"));
          storeSensorValueInRedis(meterId, epochTime[0], "L"+str(1+i)+".Current", currents[i].strip("*A"));
          storeSensorValueInRedis(meterId, epochTime[0], "L"+str(1+i)+".Power",   powerUsage[i].strip("+*"));

        storeSensorValueInRedis(meterId, epochTime[0], "Total", totalReading[0]);

        #TODO: Update redis for every phase
        print "Meter   : " + meterId 
        print "Time    : " + epochTime[0]
        print "Voltage : " + voltages[0].strip("*V") + " / " + voltages[1].strip("*V") + " / " + voltages[2].strip("*V")
        print "Current : " + currents[0].strip("*A") + " / " + currents[1].strip("*A") + " / " + currents[2].strip("*A")
        print "Power   : " + powerUsage[0].strip("+*") + " / " + powerUsage[1].strip("+*") + " / " + powerUsage[2].strip("+*")
        print "Consumed: " + totalReading[0]
        print "=="

    time.sleep(1)

