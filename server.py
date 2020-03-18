#!/usr/bin/env python3

# Sky Hoffert
# UDP hole punch, server.

import constants
from util import ParsePayload, ip2long

import socket
import sys
import struct

IP = "127.0.0.1"
PORT = 5000
HOST_ADDR = ("0",0)
HOST_CONFIRMED = False

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind( (IP, PORT) )

# SERVER expects a HOST to REQ
data, addr = sock.recvfrom(4096)
print("RX from {}".format(addr))
rd = ParsePayload(data, True)

try:
    if rd["HOST_REQ"]:
        HOST_ADDR = addr
except KeyError:
    print("HOST_REQ not provided. Exiting.")
    sock.sendto(b"", addr)
    sys.exit(0)

resp = bytearray()
resp.append(constants.TYPES["SOURCE_ID"])
resp.append(constants.IDS["SERVER"])
resp.append(constants.TYPES["DEST_ID"])
resp.append(constants.IDS[rd["SOURCE_ID"]])
resp.append(constants.TYPES["HOST_ACK"])

print("Attempt to TX to {}:{}".format(addr[0], addr[1]))
sock.sendto(bytes(resp), addr)

# SERVER expects HOST to ACKACK
data, addr = sock.recvfrom(4096)
print("RX from {}".format(addr))
rd = ParsePayload(data, True)

if HOST_ADDR != addr:
    print("HOST address does not match. Exiting.")
    sys.exit(0)

try:
    if rd["HOST_ACKACK"]:
        pass
except KeyError:
    print("HOST_ACKACK not provided. Exiting.")
    sys.exit(0)

HOST_CONFIRMED = True

# SERVER expects a HOST to REQ
data, addr = sock.recvfrom(4096)
print("RX from {}".format(addr))
rd = ParsePayload(data, True)

try:
    if rd["CLIENT_REQ"]:
        pass
except KeyError:
    print("CLIENT_REQ not provided. Exiting.")
    sock.sendto(b"", addr)
    sys.exit(0)

resp = bytearray()
resp.append(constants.TYPES["SOURCE_ID"])
resp.append(constants.IDS["SERVER"])
resp.append(constants.TYPES["DEST_ID"])
resp.append(constants.IDS[rd["SOURCE_ID"]])
resp.append(constants.TYPES["CLIENT_ACK"])
ipint = ip2long(HOST_ADDR[0])
resp.append((ipint & 0x000000ff)) # TODO
resp.append((ipint & 0x0000ff00) >> 8) # TODO
resp.append((ipint & 0x00ff0000) >> 16) # TODO
resp.append((ipint & 0xff000000) >> 24) # TODO
resp.append((HOST_ADDR[1] & 0x000000ff)) # TODO
resp.append((HOST_ADDR[1] & 0x0000ff00) >> 8) # TODO
resp.append((HOST_ADDR[1] & 0x00ff0000) >> 16) # TODO
resp.append((HOST_ADDR[1] & 0xff000000) >> 24) # TODO

sock.sendto(resp, addr)

print("SERVER COMPLETE!")
