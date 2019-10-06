import socketio

sio = socketio.Client()

sio.connect('http://localhost:2077', namespaces=['/barcodes'])

@sio.on('connect', namespace='/barcodes')
def on_connect():
    print("Connected to a /barcode namespace. ")

@sio.on('barcodes', namespace='/barcodes')
def on_message(data):
    print('Received a message: '+str(data))