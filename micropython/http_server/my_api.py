class DHTHandler:
    d = None

    def __init__(self):
        from machine import Pin
        from dht import DHT11

        self.d = DHT11(Pin(5))

    def get(self, api_request):
        self.d.measure()
        return {
                "temperature": self.d.temperature(),
                "humidity": self.d.humidity()
                }

class WaterTempHandler:
    ds = None    
    dat = None

    def __init__(self):
        from machine import Pin
        from ds18x20 import DS18X20
        import onewire
        import time
        
        # the device is on GPIO12
        self.dat = Pin(12)

        # create the onewire object
        self.ds = DS18X20(onewire.OneWire(self.dat))

    def get(self, api_request):
        import time
        roms = self.ds.scan()
        self.ds.convert_temp()
        time.sleep_ms(750)
        result = ""
        for rom in roms:
            result += str(self.ds.read_temp(rom))
        return {
                "water_temp": float(result)
                }


class WaterLevelHandler:
    adc = None
    
    def __init__(self):
        from machine import ADC
        self.adc = ADC(0)

    def get(self, api_request):
        return {
                "water_level": self.adc.read()
                }

class RainDropHandler:
    p4 = None
    
    def __init__(self):
        from machine import Pin
        self.p4 = Pin(4, Pin.IN)

    def get(self, api_request):
        return {
                "rain_drop": self.p4.value()
                }