from machine import I2C, Pin
import ustruct
import time
import sh1106

class I2C_Virtual_Multiplexor():
    
    def __init__(self):
        pass

class AS5600_I2C():
    
    ZPOS = const(0x01)
    AGC = const(0x1A)
    RAWANGLE = const(0x0C)
    ANGLE = const(0x0E)
    STATUS = const(0x08)
    
    def _check_sensor_connected(self):
        devices = self.i2c.scan()
        return (self.sensor_address in devices)
    
    def _reg_read(self, i2c, addr, reg, nbytes=1):
        """
        Read number of bytes from register.  If nbytes>1 then read from consecutive registers.
        """
        
        self.i2c = i2c
        
        if nbytes < 1:
            return bytearray()
        
        data = i2c.readfrom_mem(addr, reg, nbytes)
        return data
    
    def __init__(self, i2c, sensor_address=0x36):
        self.sensor_address = sensor_address
        self.i2c = i2c
        
        if(not self._check_sensor_connected()):
            raise Exception(f'No sensor found on { hex(sensor_address) }')

    def get_raw_angle(self):
        data = self._reg_read(self.i2c, self.sensor_address, RAWANGLE, 2)
        angle = ustruct.unpack_from(">h", data, 0)[0]
        return angle
    
    def get_status(self):
        data = self._reg_read(self.i2c, self.sensor_address, AGC, 1)
        status = ustruct.unpack_from(">B", data, 0)[0]
        return status
    
    def set_zero_position(self):
        pass

def initialize_oled():
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(0), freq=400_000)
    oled_width = 128
    oled_height = 64
    oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c0, rotate=180)
    oled.fill(0)
    oled.show()
    return oled

oled = initialize_oled()

i2c1a = I2C(1, scl=Pin(3), sda=Pin(2), freq=400_000)
sensor1 = AS5600_I2C(i2c1a, sensor_address=0x36)

i2c1b = I2C(1, scl=Pin(7), sda=Pin(2), freq=400_000)
sensor2 = AS5600_I2C(i2c1b, sensor_address=0x36)

DEGREES_PER_STEP = 360 / 4096

while True:
    
    i2c1a = I2C(1, scl=Pin(3), sda=Pin(2), freq=400_000)
    raw_angle1 = sensor1.get_raw_angle()
    machine.Pin(3, machine.Pin.IN)
  
    i2c1b = I2C(1, scl=Pin(7), sda=Pin(2), freq=400_000)
    raw_angle2 = sensor2.get_raw_angle()
    machine.Pin(7, machine.Pin.IN)
    
    oled.fill(0)
    oled.text(f'{( raw_angle1 * DEGREES_PER_STEP ):>3.2f}', 0, 0)
    oled.text(f'{( raw_angle2 * DEGREES_PER_STEP ):>3.2f}', 0, 10)
    oled.show()

    time.sleep(0.001)