#!/usr/bin/python

import socket
import os
import redis
import time
from struct import unpack


def writeRedisSensorDescription():
  "write the redis description of the sensors"
  baseKey = "sensordata.shackspace." + sensorID + ".config.sensors"
  value = "{ \"Light1.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + " \"Light2.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + \
          "  \"Light3.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + " \"Light4.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + \
          "  \"Light5.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + " \"Light6.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + \
          "  \"Light7.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + " \"Light8.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + \
          "  \"Light9.state\": { \"unit\": \"none\", \"type\": \"boolean\"}, " + " \"Light10.state\": { \"unit\": \"none\", \"type\": \"boolean\"}}"

  redisConnection.set(baseKey, value) 
  return

def updateRedisDB(lightID, status, timestamp):
  "write a sample to the redis db"
  channelName = "Light" + str(lightID) + ".state"
  baseKey = "sensordata.shackspace." + str(sensorID) + ".data." + channelName
  value = "[" + str(timestamp) + "," + str(status)  + "]";
  redisConnection.rpush(baseKey, value)

  return;


# define sensor id
sensorID = "0000000001"


# generate a socket to recieve the broadcasts from the light hardware
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 2342))

# connect to the redis database.
redisConnection = redis.Redis("glados.shack")
writeRedisSensorDescription();

# loop and read the socket to get the information on changes in the lights.
while True:
  # recieve 2 bytes.
  packet = sock.recv(2);
  
  # unpack light id and status from those two bytes
  lightID, status = unpack("BB", packet); 
  
  # write to REDIS-DB
  updateRedisDB(lightID, status, int(time.time()))
  print "Light " + str(lightID) + " set to " + str(status);


