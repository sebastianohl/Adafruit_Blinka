# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`analogbufio` - Analog input and output control via DMA
============================================
See `CircuitPython:analogbufio` in CircuitPython for more details.
Not supported by all boards.

* Author(s): Sebastian Ohl
"""
import sys

from adafruit_blinka.agnostic import detector

# pylint: disable=ungrouped-imports,wrong-import-position,unused-import

if detector.board.PYTEST_BOARD:
    from adafruit_blinka.microcontroller.pytest_board.analogbufio import BufferedIn
else:
    raise NotImplementedError("analogio not supported for this board.")
