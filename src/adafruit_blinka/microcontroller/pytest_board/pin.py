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

IO00 = Pin(0)
IO01 = Pin(1)
IO02 = Pin(2)
IO03 = Pin(3)
IO04 = Pin(4)
IO05 = Pin(5)
IO06 = Pin(6)
IO07 = Pin(7)
IO08 = Pin(8)
IO09 = Pin(9)
IO10 = Pin(10)
IO11 = Pin(11)
IO12 = Pin(12)
IO13 = Pin(13)
IO14 = Pin(14)
IO15 = Pin(15)
IO16 = Pin(16)
IO17 = Pin(17)
IO18 = Pin(18)
IO19 = Pin(19)
IO20 = Pin(20)
IO21 = Pin(21)
IO22 = Pin(22)
IO23 = Pin(23)
IO24 = Pin(24)
IO25 = Pin(25)
IO26 = Pin(26)
IO27 = Pin(27)
IO28 = Pin(28)
IO29 = Pin(29)
IO30 = Pin(30)
IO31 = Pin(31)
IO32 = Pin(32)
IO33 = Pin(33)
IO34 = Pin(34)
IO35 = Pin(35)
IO36 = Pin(36)
IO37 = Pin(37)
IO38 = Pin(38)
IO39 = Pin(39)
IO40 = Pin(40)
IO41 = Pin(41)
IO42 = Pin(42)
IO43 = Pin(43)
IO44 = Pin(44)
IO45 = Pin(45)
IO46 = Pin(46)
IO47 = Pin(47)
IO48 = Pin(48)
IO49 = Pin(49)

A0 = Pin(50)
A1 = Pin(51)
A2 = Pin(52)
A3 = Pin(53)
A4 = Pin(54)

# SPI pins
SCLK = SCK = Pin(60)
MOSI = Pin(61)
MISO = Pin(62)
CS = Pin(63)

spiPorts = ((0, SCK, MOSI, MISO), )
