#!/usr/bin/env python3

# Sky Hoffert
# UDP hole punch, host.

import constants
from util import ParsePayload

import socket
import sys

IP = "127.0.0.1"
PORT = 5000

print("Host.")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

resp = bytearray()
resp.append(constants.TYPES["SOURCE_ID"])
resp.append(constants.IDS["HOST"])
resp.append(constants.TYPES["DEST_ID"])
resp.append(constants.IDS["SERVER"])
resp.append(constants.TYPES["HOST_REQ"])

print("Attempt to TX to {}:{}".format(IP, PORT))
sock.sendto(bytes(resp), (IP, PORT))

data, addr = sock.recvfrom(4096)
print("RX from {}".format(addr))
rd = ParsePayload(data, True)

try:
    if rd["HOST_ACK"]:
        pass
except KeyError:
    print("HOST_ACK not provided. Exiting.")
    sock.sendto(b"", addr)
    sys.exit(0)

resp = bytearray()
resp.append(constants.TYPES["SOURCE_ID"])
resp.append(constants.IDS["HOST"])
resp.append(constants.TYPES["DEST_ID"])
resp.append(constants.IDS["SERVER"])
resp.append(constants.TYPES["HOST_ACKACK"])

print("Attempt to TX to {}:{}".format(IP, PORT))
sock.sendto(bytes(resp), (IP, PORT))

data, addr = sock.recvfrom(4096)
print("RX from {}".format(addr))
rd = ParsePayload(data, True)

try:
    if rd["HOST_PING"]:
        pass
except KeyError:
    print("HOST_PING not provided. Exiting.")
    sys.exit(0)

resp = bytearray()
resp.append(constants.TYPES["SOURCE_ID"])
resp.append(constants.IDS["HOST"])
resp.append(constants.TYPES["DEST_ID"])
resp.append(constants.IDS["SERVER"])
resp.append(constants.TYPES["HOST_PONG"])

print("Attempt to TX to {}:{}".format(addr[0], addr[1]))
sock.sendto(resp, addr)

print("HOST COMPLETE!")
