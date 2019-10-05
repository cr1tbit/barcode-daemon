#!/usr/bin/python
import struct
import time
import sys
import socket

char_table = {
    2: "1",
    3: "2",
    4: "3",
    5: "4",
    6: "5",
    7: "6",
    8: "7",
    9: "8",
    10: "9",
    11: "0",
    28: "\n"
    }

infile_path = "/dev/input/event" + (sys.argv[1] if len(sys.argv) > 1 else "0")

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

#open event handler file in binary mode
in_file = open(infile_path, "rb")

#read the scanner in loop
event = in_file.read(EVENT_SIZE)

sock = socket.socket(socket.AF_INET, 
                     socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
   
    #these events represent virtual keypress coming from the scanner
    if type == 1 and value == 1:
        c = char_table.get(code,"")
        print(c,end = '')
        sock.sendto(c.encode('utf8'),('<broadcast>',2137))

    event = in_file.read(EVENT_SIZE)

in_file.close()



