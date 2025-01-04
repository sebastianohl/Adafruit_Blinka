# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""SPI class for a generic agnostic board."""

# from .rp2040_u2if import rp2040_u2if

import base64
from adafruit_blinka.microcontroller.pytest_board.socket_connection import SocketConnection


# pylint: disable=protected-access, no-self-use
class SPI(SocketConnection):
    """SPI Base Class for a testing board."""

    MSB = 0

    def __init__(self, index, *, baudrate=100000):
        self._index = index
        self._frequency = baudrate
        super().__init__(f'/tmp/SPI{index}')

    def __del__(self):
        super().__del__()

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=1000000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize the Port"""
        self._frequency = baudrate

    # pylint: enable=too-many-arguments

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._frequency

    # pylint: disable=unnecessary-pass
    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        if buf is None or len(buf) < 1:
            return
        if end is None:
            end = len(buf)

        self._send_packet({"data": base64.b64encode(buf[start:end]).decode()})

    # pylint: disable=unnecessary-pass
    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""

        if buf is None or len(buf) < 1:
            return
        if end is None:
            end = len(buf)

        self._send_packet(
            {"data": base64.b64encode([write_value] * (end - start)).decode()})
        data = base64.b64decode(self._receive_packet()["data"])
        for i in range(end - start):  # 'readinto' the given buffer
            buf[start + i] = data[i]

    # pylint: disable=too-many-arguments, unnecessary-pass
    def write_readinto(self,
                       buffer_out,
                       buffer_in,
                       out_start=0,
                       out_end=None,
                       in_start=0,
                       in_end=None):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """

        if buffer_out is None or buffer_in is None:
            return
        if len(buffer_out) < 1 or len(buffer_in) < 1:
            return
        if out_end is None:
            out_end = len(buffer_out)
        if in_end is None:
            in_end = len(buffer_in)
        if out_end - out_start != in_end - in_start:
            raise RuntimeError("Buffer slices must be of equal length.")

        self._send_packet({
            "data":
            base64.b64encode(list(buffer_out[out_start:out_end + 1])).decode()
        })
        data = base64.b64decode(self._receive_packet()["data"])
        data = self._incoming.get()
        for i in range((in_end - in_start)):
            buffer_in[i + in_start] = data[i]
