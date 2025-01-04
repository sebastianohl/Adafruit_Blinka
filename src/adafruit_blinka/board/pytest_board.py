# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for a pytest, os-agnostic, board."""
from adafruit_blinka.microcontroller.pytest_board import pin

D0 = pin.D0
D1 = pin.D1
D2 = pin.D2
D3 = pin.D3
D4 = pin.D4
D5 = pin.D5
D6 = pin.D6
D7 = pin.D7
D8 = pin.D8
D9 = pin.D9

# Analog pins
A0 = pin.A0
A1 = pin.A1
A2 = pin.A2
A3 = pin.A3
A4 = pin.A4

# SPI pins
SCLK = pin.SCLK
SCK = pin.SCK
MOSI = pin.MOSI
MISO = pin.MISO
CS = pin.D6

# SPI port
spiPorts = ((0, SCK, MOSI, MISO), )
