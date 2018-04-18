import pygatt.backends

# The BGAPI backend will attemt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.backends.BGAPIBackend()
device = adapter.connect('01:23:45:67:89:ab')
value = device.char_read("a1e8f5b1-696b-4e4c-87c6-69dfe0b0093b")