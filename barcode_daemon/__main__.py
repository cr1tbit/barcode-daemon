#!/usr/bin/python
from time import sleep
import queue
from threading import Thread
import logging
from .input_event_wrapper import InputEventWrapper



if __name__ == '__main__':
    
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
