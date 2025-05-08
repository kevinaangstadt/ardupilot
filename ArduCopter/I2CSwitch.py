import smbus

class I2CSwitch(object):
    """Helper class to handle switching between two controllers"""
    def __init__(self):
        # Magic number comes from i2cswitch firmware
        self.__address = 0x26
        # On the upboard, this is on i2cbus 1
        self.__bus = smbus.SMBus(1)

        # read the current value from the switch
        # self._current = self.__bus.read_byte_data(self.__address, 0x0)
        self._current = self.get_current()

    def get_current(self):
        # built-in read apparently has a bug
        # self._current = self.__bus.read_byte_data(self.__address, 0x0)

        # just write the address as a byte, and then gread a byte
        self.__bus.write_byte(self.__address, 0x0)
        self._current = self.__bus.read_byte(self.__address)
        return self._current

    def switch(self):
        to_write = 0
        if self._current == 0:
            to_write = 1

        self.__bus.write_byte_data(self.__address, 0x0, to_write)
        return self.get_current()

    def choose_device(self, dev):
        if not isinstance(dev, int):
            raise InvalidDeviceError("dev must be an integer")
        if dev < 0 or dev > 1:
            raise InvalidDeviceError("dev must be either 0 or 1")
        #print(dev)
        while dev != self.get_current():
            print(self._current)
            self.switch()

class InvalidDeviceError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(InvalidDeviceError, self).__init__(message)
