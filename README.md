# AS5600
Micropython library for the AS5600 magntic encoder using I2C.

## Goals
- Get the amount of rotation between calls
- Get the current speed of rotation
   - Need to decide on a rational amount of time to default the capture window to, as well as make it configurable
   - Decide what unit of measurement is to be used by default (probably RPM) and if we need any additional options (such as rad/s or °/s)

### Out of scope
- I have no use case for burning configurations at this time, so these will not be implemented.
- Likewise, I'm only interested in using this chip via I2C so have no plans to support PWM etc.
