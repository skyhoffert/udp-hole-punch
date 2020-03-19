#!/usr/bin/env python3

# Sky Hoffert
# UDP hole punch, host.

import constants
from util import ParsePayload, ba2int, ba2ip

import socket
import sys

IP = "127.0.0.1"
PORT = 5000
CLIENT_ADDR = ("0",0)
CLIENT_CONFIRMED = False

if len(sys.argv) == 3:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])

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

# Here, a HOST_CLIENT_ADDR should arrive from client
data, addr = sock.recvfrom(4096)
print("RX from {}".format(addr))
rd = ParsePayload(data, True)

try:
    if rd["HOST_CLIENT_ADDR"]:
        CLIENT_CONFIRMED = True
        CLIENT_ADDR = (ba2ip(rd["CLIENT_ADDR"][0:4]), ba2int(rd["CLIENT_ADDR"][4:8]))
except KeyError:
    print("HOST_CLIENT_ADDR not provided. Exiting.")
    sys.exit(0)

print("Got Client addr: {}".format(CLIENT_ADDR))
sys.stdout.flush()

resp = bytearray()
resp.append(constants.TYPES["SOURCE_ID"])
resp.append(constants.IDS["HOST"])
resp.append(constants.TYPES["DEST_ID"])
resp.append(constants.IDS["CLIENT"])
resp.append(constants.TYPES["CLIENT_PING"])

# Send 10 messages to client.
for i in range(0,10):
    sock.sendto(resp, CLIENT_ADDR)

# Here, a HOST_PING should arrive from client
# Block waiting for one.
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
resp.append(constants.IDS["CLIENT"])
resp.append(constants.TYPES["HOST_PONG"])

print("Attempt to TX to {}:{}".format(addr[0], addr[1]))
sock.sendto(resp, addr)

# Now, capture as many pings from client as you can before timeout
nPings = 1
sock.settimeout(1)

while True:
    # Here, a HOST_PING should arrive from client
    try:
        data, addr = sock.recvfrom(4096)
    except socket.timeout:
        print("Socket timed out. Exiting.")
        break
    print("RX from {}".format(addr))
    rd = ParsePayload(data, True)

    try:
        if rd["HOST_PING"]:
            nPings += 1
    except KeyError:
        print("HOST_PING not provided. Exiting.")
        sys.exit(0)

    resp = bytearray()
    resp.append(constants.TYPES["SOURCE_ID"])
    resp.append(constants.IDS["HOST"])
    resp.append(constants.TYPES["DEST_ID"])
    resp.append(constants.IDS["CLIENT"])
    resp.append(constants.TYPES["HOST_PONG"])

    print("Attempt to TX to {}:{}".format(addr[0], addr[1]))
    sock.sendto(resp, addr)

print("Got {} pings from client.".format(nPings))

print("HOST COMPLETE!")
