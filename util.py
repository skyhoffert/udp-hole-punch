# Sky Hoffert
# Utility functions for udp-hole-punching.

import constants

import struct
import socket

def RevDict(d, value):
    for k in d:
        if d[k] == value:
            return k

def ba2int(ba):
    return ba[0] + (ba[1]<<8) + (ba[2]<<16) + (ba[3]<<24)

def ba2ip(ba):
    l = ba2int(ba)
    return socket.inet_ntoa(struct.pack("!L", l))

def ip2long(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

def ParsePayload(bar, p=False):
    if p:
        print(bar)
    
    rd = {}
    i = 0

    while i < len(bar):
        if bar[i] == constants.TYPES["SOURCE_ID"]:
            fromId = RevDict(constants.IDS, bar[i+1])
            rd["SOURCE_ID"] = fromId
            i += constants.DATA_LEN["SOURCE_ID"]
            if p:
                print("  From: {}".format(fromId))
        elif bar[i] == constants.TYPES["DEST_ID"]:
            toId = RevDict(constants.IDS, bar[i+1])
            rd["DEST_ID"] = toId
            i += constants.DATA_LEN["DEST_ID"]
            if p:
                print("  To: {}".format(toId))
        elif bar[i] == constants.TYPES["HOST_REQ"]:
            rd["HOST_REQ"] = True
            if p:
                print("  HOST_REQ")
        elif bar[i] == constants.TYPES["HOST_ACK"]:
            rd["HOST_ACK"] = True
            if p:
                print("  HOST_ACK")
        elif bar[i] == constants.TYPES["HOST_ACKACK"]:
            rd["HOST_ACKACK"] = True
            if p:
                print("  HOST_ACKACK")
        elif bar[i] == constants.TYPES["CLIENT_REQ"]:
            rd["CLIENT_REQ"] = True
            if p:
                print("  CLIENT_REQ")
        elif bar[i] == constants.TYPES["CLIENT_ACK"]:
            rd["CLIENT_ACK"] = True
            if p:
                print("  CLIENT_ACK")
            rd["HOST_ADDR"] = bar[i+1:i+1+constants.DATA_LEN["CLIENT_ACK"]]
            i += constants.DATA_LEN["CLIENT_ACK"]
        elif bar[i] == constants.TYPES["HOST_PING"]:
            rd["HOST_PING"] = True
            if p:
                print("  HOST_PING")
        elif bar[i] == constants.TYPES["HOST_PONG"]:
            rd["HOST_PONG"] = True
            if p:
                print("  HOST_PONG")
        else:
            print("  CNP")
        i += 1
    
    return rd
