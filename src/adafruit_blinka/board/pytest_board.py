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

IO00 = pin.IO00
IO01 = pin.IO01
IO02 = pin.IO02
IO03 = pin.IO03
IO04 = pin.IO04
IO05 = pin.IO05
IO06 = pin.IO06
IO07 = pin.IO07
IO08 = pin.IO08
IO09 = pin.IO09
IO10 = pin.IO10
IO11 = pin.IO11
IO12 = pin.IO12
IO13 = pin.IO13
IO14 = pin.IO14
IO15 = pin.IO15
IO16 = pin.IO16
IO17 = pin.IO17
IO18 = pin.IO18
IO19 = pin.IO19
IO20 = pin.IO20
IO21 = pin.IO21
IO22 = pin.IO22
IO23 = pin.IO23
IO24 = pin.IO24
IO25 = pin.IO25
IO26 = pin.IO26
IO27 = pin.IO27
IO28 = pin.IO28
IO29 = pin.IO29
IO30 = pin.IO30
IO31 = pin.IO31
IO32 = pin.IO32
IO33 = pin.IO33
IO34 = pin.IO34
IO35 = pin.IO35
IO36 = pin.IO36
IO37 = pin.IO37
IO38 = pin.IO38
IO39 = pin.IO39
IO40 = pin.IO40
IO41 = pin.IO41
IO42 = pin.IO42
IO43 = pin.IO43
IO44 = pin.IO44
IO45 = pin.IO45
IO46 = pin.IO46
IO47 = pin.IO47
IO48 = pin.IO48
IO49 = pin.IO49

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
