import my_api
import http_api_handler
api_handler = http_api_handler.Handler([(['test'], my_api.Handler())])
import uhttpd
server = uhttpd.Server([('/api', api_handler)])
server.run()