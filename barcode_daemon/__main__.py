#!/usr/bin/python
import struct
from time import sleep
import sys
import socket
import queue
from threading import Thread
import logging



class InputEventWrapper:
    def __init__(self, filepath:str = None):
        if filepath is None:
            filepath = "/dev/input/event0" 
       
        self.input_fh = open(filepath, "rb")
        logging.info("started event wrapper on file "+str(filepath))
    
        self.event_format = 'llHHI'
        self.event_size = \
            struct.calcsize(self.event_format)
    
        self.char_table = {
            2: "1", 3: "2", 4: "3",
            5: "4", 6: "5", 7: "6",
            8: "7", 9: "8", 10: "9",
            11: "0", 28: "\n"
        }
        
    def unpack_event(self, event:bytes) -> dict:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(self.event_format, event)
        return {
            'type':type,
            'code':code,
            'value':value
            }

    #careful - blocking functions ahead
    def get_event(self) -> dict:
        event = self.input_fh.read(self.event_size)
        return self.unpack_event(event)
        
    def get_letter(self) -> str:
        event_dict = self.get_event()
        if event_dict['type'] == 1 and event_dict['value'] == 1:
            return self.char_table.get(event_dict['code'],"")

    def get_barcode(self) -> str:
        barcode = ""
        while True:
            c = self.get_letter()
            if c is '\n':
                return barcode
            if c is not None:
                barcode +=c


barcode_queue = queue.Queue()

def input_reader() -> None:
    wrap = InputEventWrapper()
    while True:
        barcode_queue.put(wrap.get_barcode())

def barcode_emitter() -> None:
    while True:
        while not barcode_queue.empty():
            print("barcode: " + str(barcode_queue.get()))
        sleep(0.1)

t_emmiter = Thread(target=barcode_emitter)
t_emmiter.daemon = True
t_emmiter.start()

t_event_reader = Thread(target=input_reader)
t_event_reader.daemon=True
t_event_reader.start()

logging.info("entring eternal slumber.")
while True:
    sleep(10000)
