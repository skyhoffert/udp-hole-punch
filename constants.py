# Constants used in udp-hole-punching

# Messages are sent to be read in BYTE BY BYTE format. Format below:
# First BYTE: ALWAYS 0xff
# 1     BYTE: TYPE - Describes following data
# 2     BYTE: DATA - Depends on previous byte
# 3     BYTE: DATA/TYPE - Could be data or type depening on previous type
# ...   BYTE:
# Final BYTE: ALWAYS 0xff

# Possibly types.
TYPES = {
    "SOURCE_ID": 0,
    "DEST_ID": 1,
    "HOST_REQ": 2, # Including this signifies that a peer is requesting host priviliges
    "HOST_DENY": 3, # A server can deny host priv
    "HOST_ACK": 4, # A server will send an ack to confirm host priv
    "HOST_ACKACK": 5, # A host will finally confirm that it is a host
    "CLIENT_REQ": 6, # Clients will request host information from server
    "CLIENT_ACK": 7, # A server will respond with host information
    "CLIENT_ACKACK": 8, # A client confirms it is a client to server
    "HOST_PING": 9, # A client will attempt to ping a server
    "HOST_PONG": 10, # a host will respond to a client ping
    "HOST_CLIENT_ADDR": 11, # server provides host the client addr
    "CLIENT_PING": 12, # A host will attempt to ping a client with this - NO pong
}

# Length of data, in bytes.
DATA_LEN = {
    "SOURCE_ID": 1,
    "DEST_ID": 1,
    "HOST_REQ": 0,
    "HOST_DENY": 0,
    "HOST_ACK": 0,
    "HOST_ACKACK": 0,
    "CLIENT_REQ": 0,
    "CLIENT_ACK": 8, # Contains host IP and PORT in that order
    "CLIENT_ACKACK": 0,
    "HOST_PING": 0,
    "HOST_PONG": 0,
    "HOST_CLIENT_ADDR": 8,
}

# Identities. Could be a SOURCE_ID or DEST_ID
IDS = {
    "SERVER": 0,
    "HOST": 1,
    "CLIENT": 2,
}
