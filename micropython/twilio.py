sid = "AC208feaac67bbeff816b27f29f2ce212f"
token = "f2af1b1bca1b61fa771b3cf7521c054d"
from_number = "%2B14252306480"
to_number = "%2B16159263608"

import urllib.urequests
import ubinascii

data = "From=%2B14252306480&To=%2B16159263608&Body=This+is+a+test"

url = "https://api.twilio.com/2010-04-01/Accounts/{0}/Messages.json".format(sid)

twilio_data = "From:+14252306480"

r = urllib.urequests.post(url, data=data, json=None, stream=True, headers={
    "Authorization": "Basic " + ubinascii.b2a_base64("{0}:{1}".format(sid, token)).decode("ascii"),
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    "WWW-Authenticate": 'Basic realm = "Twilio API"'
})
print(r.text)
r.close()