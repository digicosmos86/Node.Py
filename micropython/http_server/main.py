import my_api
import http_api_handler
api_handler = http_api_handler.Handler([(['temp_hum'], my_api.DHTHandler()),
                                        (['water_temp'], my_api.WaterTempHandler()),
                                        (['water_level'], my_api.WaterLevelHandler()),
                                        (['rain_drop'], my_api.RainDropHandler())
                                       ])
import uhttpd
server = uhttpd.Server([('/api', api_handler)])
server.run()