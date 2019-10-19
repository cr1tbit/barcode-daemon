#!/usr/bin/python
from time import sleep
import queue
from threading import Thread
import logging
from .input_event_wrapper import InputEventWrapper
from flask import Flask
from flask_socketio import SocketIO, emit


logging.basicConfig(level=logging.WARNING)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) #stop spamming dude

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return 'I\'m a barode scanner daemon. Connect to me via socketIO, will you?'

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':    
    barcode_queue = queue.Queue(maxsize=20)
    
    def input_reader() -> None:
        wrap = InputEventWrapper("/dev/input/event3")
        while True:
            try:
                barcode_queue.put(wrap.get_barcode())
            except queue.Full:
                logging.error("barcode queue full! Dropping scanned barcode.")
    
    def barcode_emitter() -> None:
        logging.info("Starting barcode emitter thread")
        while True:
            barcode = barcode_queue.get()
            logging.info("emmiting barcode: " + str(barcode))
            socketio.emit('barcodes', 
                {'data': barcode},
                namespace='/barcodes')
    
    t_emmiter = Thread(target=barcode_emitter)
    t_emmiter.daemon = True
    t_emmiter.start()
    
    t_event_reader = Thread(target=input_reader)
    t_event_reader.daemon = True
    t_event_reader.start()
    
    socketio.run(app,host='0.0.0.0', port=2077)
