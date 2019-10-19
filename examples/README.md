## How to connect to the scanner daemon

1. Connect via socketio, as can be seen in the example
2. The API is trivial - every barcode scan on the server pushes a message with the numbers from the barcode.

#### Protips:
* socketIO has libraries all around the programming landscape - no need to use python on the client side. In fact, it's JS-native library. Take a look: https://socket.io/docs/
* For now the barcode scanner sends only numbers. I think barcode may contain letters. But for now they're simply ignored. This might need to be fixed.
