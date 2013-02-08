#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket
import sys
import re
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening

regexPower = re.compile("[+][0-9]+[*]")
regexEpochTime = re.compile("\w[0-9]+\w{8,}")
server_address = ('powerraw.shack', 11111)
epochtime_old = 0
while True:

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
        #print >>sys.stderr, 'received "%s"' % data

    finally:
        sock.close()
    epochTime = regexEpochTime.findall(data_received)
    if epochtime_old != epochTime[0]:
        epochtime_old = epochTime[0]
        r = regexPower.findall(data_received)
        #TODO: Update redis for every phase
        for results in r:
            print results.strip('+*')

    time.sleep(1)

