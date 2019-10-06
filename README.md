## Barcode scanner daemon

This python flask-socketIO-based daemon has been created to allow multiple apps to work with barcode scanners. The cheap, PS2-based ones. They enumerate as a basic keyboard, which may be a little annoying.

The single, monolithic app would be the easiest way out, but I have a couple, distinct usages for the barcode scanner on my mind:

* The library system - most of the books have barcodes with their ISBNs
* Taking care of our soft-drink stock
* Scanning printed barcodes to trigger specific actions in space (who doesn't want `play despacito` barcode!?)
* Maybe more?

The apps making use of this daemon should connect via socketIO - as can be seen in `example_client.py`.
