# SPDX-FileCopyrightText: 2024 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""generic_agnostic_board pin interface"""


class Pin:
    """A basic Pin class for use with generic_agnostic_board"""

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

    def return_toggle(self):
        """Returns the pin's expected value, toggling between True and False"""
        toggle_state = not self.previous_value
        return toggle_state

    def return_false(self):
        """Returns the pin's expected value, False"""
        return False

    def return_true(self):
        """Returns the pin's expected value, True"""
        return True

    def return_random_int(self):
        """Returns a random integer"""
        return random.randint(0, 65535)

    def return_fixed_int_pi(self):
        """Returns the first five digits of Pi, 31415"""
        return 31415

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None
        self._pull = None
        self.previous_value = False
        self.current_value = None
        self._wave_idx = None

        # mapping of pin definition names to expected behavior
        self.pin_behavior = {
            0: self.return_true,  # Dx_INPUT_TRUE
            1: self.return_false,  # Dx_INPUT_FALSE
            2: self.return_true,  # Dx_INPUT_TRUE_PULL_UP
            3: self.return_true,  # Dx_INPUT_TRUE_PULL_DOWN
            4: self.return_true,  # Dx_OUTPUT
            7: self.return_random_int,  # Ax_INPUT_RAND_INT
            8: self.return_fixed_int_pi,  # Ax_INPUT_FIXED_INT_PI
            11: self.return_toggle,  # Dx_INPUT_TOGGLE
        }

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        pull = Pin.PULL_NONE if pull is None else pull
        self._pull = pull
        self._mode = mode

    def write(self, new_value):
        """Saves the new_value to the pin for subsequent calls to .value"""
        self.previous_value = self.current_value
        self.current_value = new_value

    def read(self):
        """Returns the pin's expected value."""
        self.previous_value = self.current_value
        # perform a lookup on the pin_behavior dict to get the value
        self.current_value = self.pin_behavior.get(self.id)()

        # is pin a pull up and pin is LOW?
        if self._pull == Pin.PULL_UP and self.current_value is False:
            self.current_value = False
        # is pin a pull down and pin is HIGH?
        if self._pull == Pin.PULL_DOWN and self.current_value is True:
            self.current_value = False
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
            if val is None:
                self.previous_value = self.current_value
                return self.current_value
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
# Special "digital" pins
D6 = Pin(6)
# Analog pins
A0 = Pin(7)
A1 = Pin(8)
A4 = Pin(12)

# Special digital pins for pixels
D7 = Pin(11)
D8 = Pin(13)
D9 = Pin(14)

# SPI pins
SCLK = SCK = Pin(15)
MOSI = Pin(16)
MISO = Pin(17)
CS = Pin(18)

spiPorts = ((0, SCK, MOSI, MISO), )
