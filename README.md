# Barcode scanner daemon

This flask-socketIO-based daemon has been created to allow multiple apps to work with barcode scanners. The cheap, PS2-based ones. They enumerate as a basic keyboard, which may be a little annoying to work with.

It is meant to run on a headless system (Raspberry Pi). The keyboard strokes are simply read straight from `/dev/input/event*`, not intercepted. By default, they will still become registered by linux kernel, and passed to the current active terminal.

My current solution to this problem is disabling terminal on tty1 completely:

```
systemctl disable getty@tty1.service
```

This way:
1. After booting, by default, the keyboard input is ignored
2. If ssh access is lost, one may still acces the device by switching to another tty (alt+Fn)
3. Monitor may still be used, for example to view images by `fim`

## The app structure

The single, monolithic app would be the easiest way out, but I have a couple, distinct usages for the barcode scanner on my mind:

* The library system - most of the books have barcodes with their ISBNs
* Taking care of our soft-drink stock
* Scanning printed barcodes to trigger specific actions in space (who doesn't want `play despacito` barcode!?)
* Maybe more...

The apps making use of this daemon may connect via socketIO - as can be seen in `example_client.py`.
