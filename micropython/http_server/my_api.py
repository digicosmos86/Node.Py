class Handler:
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

