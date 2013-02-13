#!/usr/bin/python

import socket
import sys
from struct import unpack

def printUsage():
  "prints usage information for this scrip"
  print "Usage: setlight.py <lightID> <state>"
  print "    lightID: 0..10"
  print "    state: 0,1"
  return

def prepareLightMessage(lightID, status):
  "generates a light packet to be sent to the controller in the lounge"
  return chr(0xA5) + chr(0x5A) + chr(lightID) + chr(status);


# check if the application was called correctly.
if len(sys.argv) != 3: 
  printUsage();
  sys.exit();

lightID = int(sys.argv[1]);
status = int(sys.argv[2]);

if lightID > 10 or lightID < 0:
  printUsage();
  sys.exit();

if status != 1 and status != 0:
  printUsage();
  sys.exit();

# prepare a socket and send data to the light control.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setblocking(1);
sock.connect(("licht.shack", 1337));
sock.send(prepareLightMessage(lightID, status))
sock.shutdown(2)
sock.close()

