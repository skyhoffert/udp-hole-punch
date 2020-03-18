#!/usr/bin/env python3

# Sky Hoffert
# UDP hole punch, client.

import constants
from util import ParsePayload, ba2ip, ba2int

import socket
import sys

IP = "127.0.0.1"
PORT = 5000
HOST_ADDR = ("0",0)
HOST_READY = False

print("Starting.")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

resp = bytearray()
resp.append(constants.TYPES["SOURCE_ID"])
resp.append(constants.IDS["CLIENT"])
resp.append(constants.TYPES["DEST_ID"])
resp.append(constants.IDS["SERVER"])
resp.append(constants.TYPES["CLIENT_REQ"])

print("Attempt to TX to {}:{}".format(IP, PORT))
sock.sendto(bytes(resp), (IP, PORT))

data, addr = sock.recvfrom(4096)
print("RX from {}".format(addr))
rd = ParsePayload(data, True)

try:
    if rd["CLIENT_ACK"]:
        HOST_ADDR = (ba2ip(rd["HOST_ADDR"][0:4]), ba2int(rd["HOST_ADDR"][4:8]))
        HOST_READY = True
except KeyError:
    print("CLIENT_ACK not provided. Exiting.")
    sys.exit(0)

resp = bytearray()
resp.append(constants.TYPES["SOURCE_ID"])
resp.append(constants.IDS["CLIENT"])
resp.append(constants.TYPES["DEST_ID"])
resp.append(constants.IDS["SERVER"])
resp.append(constants.TYPES["HOST_PING"])

if HOST_READY:
    sock.sendto(resp, HOST_ADDR)

data, addr = sock.recvfrom(4096)
print("RX from {}".format(addr))
rd = ParsePayload(data, True)

try:
    if rd["HOST_PONG"]:
        pass
except KeyError:
    print("HOST_PONG not provided. Exiting.")

print("CLIENT COMPLETE!")
