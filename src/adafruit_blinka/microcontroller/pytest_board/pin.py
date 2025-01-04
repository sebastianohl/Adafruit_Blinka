# SPDX-FileCopyrightText: 2025 Sebastian Ohl
#
# SPDX-License-Identifier: MIT
"""pytest board pin interface"""

from adafruit_blinka.microcontroller.pytest_board.socket_connection import SocketConnection

sockets = {}


class Pin:
    """A basic Pin class for use with pytest board"""

    # pin modes
    OUT = 0
    IN = 1
    ADC = 2
    DAC = 3
    # pin values
    LOW = 0
    HIGH = 1
    # pin pulls
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    # pylint: disable=no-self-use
    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None
        self._pull = None
        self.current_value = None

        if str(self.id) not in sockets:
            sockets[str(self.id)] = {
                "socket": SocketConnection(f"/tmp/PIN{self.id}"),
                "count": 0
            }
        sockets[str(self.id)]["count"] += 1
        self.socket = sockets[str(self.id)]["socket"]

    def __del__(self):
        if sockets is not None:
            sockets[str(self.id)]["count"] -= 1
            if sockets[str(self.id)]["count"] == 0:
                del sockets[str(self.id)]

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        pull = Pin.PULL_NONE if pull is None else pull
        self._pull = pull
        self._mode = mode

        self.socket._send_packet({
            "type": "config",
            "data": {
                "pull": pull,
                "mode": mode
            }
        })

    def write(self, new_value):
        """Saves the new_value to the pin for subsequent calls to .value"""
        self.socket._send_packet({"type": "data", "value": new_value})
        self.current_value = new_value

    def read(self):
        """Returns the pin's expected value."""
        # perform a lookup on the pin_behavior dict to get the value
        if self.socket._incoming_packet_available():
            self.current_value = self.socket._receive_packet()["value"]
        return self.current_value

    def value(self, val=None):
        """Set or return the Pin Value"""
        # Digital In / Out
        if self._mode in (Pin.IN, Pin.OUT):
            # digital read
            if val is None:
                return self.read()
            # digital write
            if val in (Pin.LOW, Pin.HIGH):
                return self.write(val)
            # nope
            raise ValueError("Invalid value for pin.")
        # Analog In
        if self._mode == Pin.ADC:
            if val is None:
                return self.read()
            # read only
            raise AttributeError("'AnalogIn' object has no attribute 'value'")
        # Analog Out
        if self._mode == Pin.DAC:
            self.write(val)
            return None
        raise RuntimeError("No action for mode {} with value {}".format(
            self._mode, val))

    def __eq__(self, other):
        print([self.id, other.id])
        return self.id == other.id


# create pin instances for each pin
D0 = Pin(0)
D1 = Pin(1)
D2 = Pin(2)
D3 = Pin(3)
D4 = Pin(4)
D5 = Pin(5)
D6 = Pin(6)
D7 = Pin(7)
D8 = Pin(8)
D9 = Pin(9)

A0 = Pin(10)
A1 = Pin(11)
A2 = Pin(12)
A3 = Pin(13)
A4 = Pin(14)

# SPI pins
SCLK = SCK = Pin(20)
MOSI = Pin(21)
MISO = Pin(22)
CS = Pin(23)

spiPorts = ((0, SCK, MOSI, MISO), )
