#### Defining a few variables

username = "idesigns17bc@gmail.com"
password = "hydroponics"
from_address = "idesigns17bc@gmail.com"
to_address = "digicosmos@gmail.com"

def send_gmail(msg_content)  # define a function for easy accesss

    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(msg_content)
    msg['subject'] = 'Alert from SenseHAT'
    msg['from'] = from_address
    msg['to'] = to_address

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(username, password)
    smtp.send_message(msg)
    smtp.quit()

#### SenseHAT Code

from sense_hat import SenseHat
import time
sense = SenseHat()

r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 255)

t = sense.get_temperature()
h = sense.get_humidity()
p = sense.get_pressure()

t = round(t, 1)
h = round(h, 1)
p = round(p, 1)

last_alert = None

if t > 30:
    now = time.time()
    if last_alert is None or now - last_alert > 1 * 60:  # 1 minute
        send_gmail("Temperature is too high!!!")
        last_alert = now
    sense.show_message("Temperature: " + str(t) + "degrees C", text_colour = r)
else:
    sense.show_message("Temperature: " + str(t) + "degrees C", text_colour = g)
    
sense.show_message("Humidity: " + str(h) + "%", text_colour = g)
sense.show_message("Pressure: " + str(p) + "hPa", text_colour = b)
