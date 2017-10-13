# Setting up Eduroam and AP in Raspbian Stretch

This tutorial demonstrates how to set up a Raspberry Pi 3 running Raspbian Stretch to connect to Eduroam and share the Eduroam network by using the Raspberry Pi as an AP.  Here's what you'll need:

* A working eduroam account from your school
* A Raspberry Pi 3
* An extra USB wifi dongle
* Keyboard, mouse, and monitor for the Raspberry Pi.  Will also work if you can use VNC or SSH to remotely access the Raspberry Pi
* [Optional] a USB stick if you don't want to use the browser on the Raspberry Pi

## PART 1. Setting up Eduroam

### Step 1. Getting an automatic set up script

The website [CAT Installer](https://cat.eduroam.org/) offers script for all operating systems to set up an Eduroam connection.  You can select school and your OS for instructions to set up your Eduroam connection. Go to the website, choose your school, and choose Linux as your operating system.  You will download a shell script.  If you are not using the browser on your Raspberry Pi, you can use VNC or SSH or a USB stick to copy the script to your Raspberry Pi.

### Step 2. Run the setup script

Run the setup script with bash

```bash
sudo bash /path/to/your-script
```

The script will end with an error.  Don't worry.  It will write this file `/root/.cat_installer/cat_installer.txt`.  Open this file, and copy its content to `/etc/wpa_supplicant/wpa_supplicant.conf`:

```bash
sudo nano /root/.cat_installer/cat_installer.txt
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

This will set up the eduroam connection.  Reboot the Raspberry Pi and you should be able to connect to Eduroam.

## PART 2. Setting up the Raspberry Pi as an AP

In this part we assume that we will use the Raspberry Pi built-in Wifi adapter to connect to Eduroam and the USB dongle to accept incoming connections.  If you are running an earlier version of Raspbian than Stretch, please follow this very nicely written tutorial.  This tutorial is for Stretch only.

### Step 1. Update your system and install necessary services

Before proceeding, update your Raspbian to the latest version.

```bash
sudo apt-get update
sudo apt-get upgrade
```

Then install `hostapd` and `dnsmasq`:

```bash
sudo apt-get install hostapd dnsmasq -y
```

Also, use `ifconfig` to find out the names of the wireless connections.  They are usually in the form of `wlanXXXXXXX`, if not `wlan0` or `wlan1`.

### Step 2. Set up dhcpcd

Edit the dhcpcd config file:

```bash
sudo nano /etc/dhcpcd.conf
```

Add the following to the file:

```bash
interface wlan0 # <-- change the interface name to that of the USB wifi dongle
static ip_address=192.168.4.1/24
static routers=192.168.4.1
static domain_name_servers=192.168.4.1
```

Another important thing is to have a set of two `wpa_supplicant.conf` files for the two Wifi adapters, and name them in the format of `wpa_supplicant-interface_name.conf`.  For example, if `wlan0` is the interface name for your built-in adapter, and `wlan1234567` is the interface name for your USB adapter, then you files should be named `wpa_supplicant-wlan0.conf` and `wpa_supplicant-wlan1234567.conf` respectively in the `/etc/wpa_supplicant` directory:

```bash
sudo cp /etc/wpa_supplicant.conf /etc/wpa_supplicant-wlan1234567.conf
sudo nano /etc/wpa_supplicant-wlan1234567.conf # remove the network configuration here
sudo mv /etc/wpa_supplicant.conf /etc/wpa_supplicant-wlan0.conf
```

The content of `wpa_supplicant-wlan0.conf` should have all Eduroam configuration, while `wpa_supplicant-wlan1234567.conf` should only have info without any IP configration:

```bash
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
```

### Step 3. Edit dnsmasq config file

Back up the original copy of `/etc/dnsmasq.conf`, and create a new one with the following content:

```bash
sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf

# Copy the content below into the dnsmasq.conf file
interface=wlan1       # Use interface wlan1
listen-address=192.168.4.1   # Specify the address to listen on
bind-interfaces      # Bind to the interface
server=8.8.8.8       # Use Google DNS
domain-needed        # Don't forward short names
bogus-priv           # Drop the non-routed address spaces
dhcp-range=192.168.4.50,192.168.4.150,12h # IP range and lease time
```

### Step 4. Edit hostapd config files

Edit the `/etc/hostapd/hostapd.conf` file:

```bash
sudo nano /etc/hostapd/hostapd.conf
```

Add the following content to it:

```bash
ssid=RPiNet # The name of the AP
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=mypassphrase # the password for the AP
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

Edit `/etc/default/hostapd` and change this:

```bash
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

### Step 5. Set up IP forwarding

Edit `/etc/sysctl.conf` and uncomment:

```bash
net.ipv4.ip_forward=1
```

And set up IP forwarding with the following command.  You will need to replace the interface names with the ones found on your Raspberry Pi.

```
sudo iptables -t nat -A  POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o wlan1234567 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan1234567 -o wlan0 -j ACCEPT
```

### Step 6. Reboot the Pi

All done.  Now all you need to do is to restart the Pi.

```bash
sudo reboot
```
