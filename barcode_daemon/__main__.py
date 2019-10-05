#!/usr/bin/python
import struct
import time
import sys

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

#long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

#open file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)

while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

    #if type != 0 or code != 0 or value != 0:
    #    print("Event type %u, code %u, value %u at %d.%d" % \
    #        (type, code, value, tv_sec, tv_usec))
    if type == 1 and value == 1:
        print(char_table[code],end = '')
        #if value > 2137:
        #    print('key is: ' + str(value - 458781))
    #else:
    #    # Events with code, type and value == 0 are "separator" events
    #    print("===========================================")

    event = in_file.read(EVENT_SIZE)

in_file.close()



