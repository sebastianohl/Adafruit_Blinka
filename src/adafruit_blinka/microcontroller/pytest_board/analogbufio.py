# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`analogio` - Analog input and output control
=================================================
See `CircuitPython:analogio` in CircuitPython for more details.
* Author(s): Sebastian Ohl
"""

from adafruit_blinka.microcontroller.pytest_board.pin import Pin
from adafruit_blinka import ContextManaged

import circuitpython_typing


class BufferedIn(ContextManaged):
    """Analog Input Class via DMA"""

    def __init__(self, pin, sample_rate: int):
        self._pin = Pin(pin.id)
        self._pin.init(mode=Pin.ADC)
        self._sample_rate = sample_rate

    def readinto(self, buffer: circuitpython_typing.WriteableBuffer) -> int:
        data = self._pin.read()
        if data is None:
            return 0
        for i in range(min(len(data), len(buffer))):
            buffer[i] = data[i]
        return min(len(data), len(buffer))

    # pylint: enable=no-self-use

    def deinit(self):
        del self._pin
