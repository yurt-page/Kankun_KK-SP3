# Kankun KK-SP3: Complete Guide
[По-русски](./README.ru.md)

The "Kankun Smart Plug", also known as the "Huafeng WiFi Plug", "Small K WiFi switch" is an inexpensive Wi-Fi controllable electric socket.
It has many models compatible with North American, European, Australian, and British plugs and outlets.

Inside this innocuous looking adapter you will find a Wi-Fi router running firmware based on [OpenWrt](https://openwrt.org).
Its hardware is similar as the [TP-link TL-WR703N](https://openwrt.org/toh/tp-link/tl-wr703n) so you can install the vanilla OpenWrt instead of the original stock EOM firmware.
The router is connected to a 10 Amper relay capable of handling 2,000 Watts.
This device is totally hackable, and it has a full Linux inside!

There was Android and iOS apps to control this plug, but they don't work anymore.
The Android app (in Chinese) could be found here: https://apkcombo.com/es/smartplug/hangzhou.kankun/
The app demo https://www.youtube.com/watch?v=xsVjhS9BROM

So you have to get a shell access and configure it manually.
See the [Automation](#Automation) section below for alteratives to the official apps.


## Features
* Firmware: OpenWrt 14 Barrier Breaker r39365 TARGET="ar71xx/generic".
* SoC: Atheros AR9330 rev 1 at 400MHz. See [datasheet](https://www.openhacks.com/uploadsproductos/ar9331_datasheet.pdf).
* 4 MB flash memory.
* 32 MB RAM Winbond W9425G6JH.
* Wi-Fi 802.11 b/g/n.
* No native ethernet or USB ports.
* Powered via AC line power.
* Relay controlling AC power plug: OMRON HF32F-G/012-H
    * 10 Amperes or 2,200 Watts. **A fire may be caused by exceeding these limits. Especially during heat or summer.**
    * Maximum DC switching voltage: 30V
    * Maximum switching current: 10A
    * Maximum switching power: 300W
    * Nominal coil DC voltage: 12V
    * Maximum coil voltage: -15.6V
    * Coil resistance: 320 Ohms
    * Coil power: 450mW

> [!CAUTION]
> A fire may be caused by exceeding 2,200 W. Especially during heat or summer.
> See Maximum column in the [Power Consumption of Household Appliances](https://www.daftlogic.com/information-appliance-power-consumption.htm).
> Especially don't use it for:
> * Home Air Conditioner, Evaporative Air Conditioner, Space Heater;
> * Boiler, Electric Oven, Hot Tub, Jacuzzi, Hot Water Immersion Heater, Hand Wash Oversink Water Heater, Power Shower;
> * Steam Iron, Hair Dryer, Clothes Dryer;
> * EV Car Charger;


## Photos
<img width="640" height="480" alt="Kankun KK-SP3: back pins" src="https://github.com/user-attachments/assets/c06fec92-c45c-4a27-85ca-e9da46a2f567" />
<details>
  <summary>Detailed photos</summary>

The front panel features a universal socket that accepts all types of plugs.
Indicator lights and a control button are also visible. One indicator lights blue when booting and flashes blue when ready.
The second lights red when the load is on.
The button allows for local control of the load, without internet access.
<img width="640" height="480" alt="Kankun KK-SP3: front with socket" src="https://github.com/user-attachments/assets/34cb52f1-64a0-4f73-aef0-9c0633077a87" />

For disassembly slide something thin like plastic card into the gap between the case and the lid anywhere.
<img width="640" height="480" alt="Kankun KK-SP3: disassembly" src="https://github.com/user-attachments/assets/f8a4329a-2d17-45cb-8da9-a5a2c55106e9" />

The device consists of two main parts: a power outlet with a power supply and a plug, and a WiFi module connected via a six-pin micro connector.
<img width="640" height="480" alt="Kankun KK-SP3: two parts" src="https://github.com/user-attachments/assets/c98a2a20-1401-4bfb-93d4-83ddaf87c070" />
</details>


## Significant safety issue!
> [!CAUTION]
> In the United States/North America version, the switch the *neutral* wire, instead of the *hot*!
> This means that when they are turned off, the plugged-in device is still live and ready to shock you.
> I'm guessing this is because they are a multi-country design, and they always switch the wire on the *left*.
> This is correct for China/Australia but incorrect for North America; see the relevant pinouts:
>
> <img width="640" height="480" alt="Australian Socket-Outlet, Auto Switched" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Australian_Socket-Outlet%2C_Auto_Switched.jpg/1201px-Australian_Socket-Outlet%2C_Auto_Switched.jpg" />


## Factory Reset
You can clear any existing settings and recover the original factory settings.
Press and hold an almost-invisible white button on the surface of the plug for 4 seconds.
If the `OK_SP3` Wi-Fi network didn’t show then additionally make off/on for the socket.


## Connect to the device
Initially the device is preconfigured to act as a Wi-Fi Access Point (AP).
Connect to its Wi-Fi network with `OK_SP3` SSID name, it doesn't have a password (and encryption).
Once connected, see in the connection information the "IPv4 Default Gateway" i.e., an address of the socket's router. It should be `192.168.10.253`.
You may even open it in a browser http://192.168.10.253 but there is no a web admin panel, so you'll see an empty page `Index of /`.


## Getting remote root shell access
You can connect via telnet with user root without a password. But you better use SSH instead.

If you already don't have an RSA key for SSH, then you'll need to generate it with `ssh-keygen -t rsa`.
The device has an old Dropbear SSH server that uses old deprecated ciphers so the `ssh` command will fail:
```
$ ssh root@192.168.10.253
Unable to negotiate with 192.168.10.253 port 22: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,kexguess2@matt.ucc.asn.au
```
The best way is to add to `~/.ssh/config` the config that allows the legacy cipher algorithms:
```
Host 192.168.10.253 kankun
  HostName 192.168.10.253
  KexAlgorithms +diffie-hellman-group1-sha1
  Ciphers +aes128-cbc
  PubkeyAcceptedAlgorithms +ssh-rsa
  HostKeyAlgorithms +ssh-rsa
  User root
  IdentitiesOnly yes
  IdentityFile ~/.ssh/id_rsa
```  

Now you can login remotely by `ssh root@192.168.10.253` or just `ssh kankun`.
The default root password is `p9z34c`, `admin` or `1234`.



### Install SSH key
Once you've gained root shell access, you can set up a key-based authorization to avoid a password prompt next time.
Use `ssh-copy-id -i ~/.ssh/id_rsa kankun` to append your key to Dropbear's `/etc/dropbear/authorized_keys`.

### Change root password
To avoid being hacked, you should change the default password with the `passwd` command:
```
# passwd
Changing password for root
New password:
Retype password:
Password for root changed by root
```

## Configure the stock firmware
### Optional: Changing the hostname
The default host name of the device is `koven`.
Presumably if you have more than one of these, you may want to change the hostname so they're identifiable.
```sh
uci set system.hostname='kankun'
uci commit
```
Or edit the config file directly with `vi /etc/sysconfig/system` this section:
```
config system
    option hostname 'kankun'
```
To exit the Vim editor press `Esc` then type `wq!` and press `Enter`.

### Set up network
You probably want the device to act as a client in your existing Wi-Fi network:
You'll need to change `/etc/config/network` and `/etc/config/wireless` with UCI.

```sh
uci set network.wwan=interface
uci set network.wwan.proto=dhcp
uci commit
```

Check changes with `cat /etc/config/network`:
```sh
config interface 'loopback'
        option ifname 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config globals 'globals'
       option ula_prefix 'fd17:d40d:f634::/48'

config interface 'lan'
        option ifname 'eth0'
        option type 'bridge'
        option proto 'static'
        option ipaddr '192.168.10.253'
        option netmask '255.255.255.0'
        option ip6assign '60'

config interface 'wwan'
        option proto 'dhcp'
```

Edit the `/etc/config/wireless` and set your Wi-Fi network password (replace here `YourWifiSsid` and `YourWifiPassword`):
```sh
uci set wireless.@wifi-iface[0].ssid='YourWifiSsid'
uci set wireless.@wifi-iface[0].key='YourWifiPassword'
uci set wireless.@wifi-iface[0].encryption='psk2'
uci set wireless.@wifi-iface[0].network='wwan'
uci set wireless.@wifi-iface[0].mode='sta'
uci commit
```

Check changes with `cat /etc/config/wireless`:
```sh
config wifi-device 'radio0'
        option type 'mac80211'
        option channel '11'
        option hwmode '11ng'
        option path	'platform/ar933x_wmac'
        option htmode 'HT20'
        list ht_capab 'SHORT-GI-20'
        list ht_capab 'SHORT-GI-40'
        list ht_capab 'RX-STBC1'
        list ht_capab 'DSSS_CCK-40'
        option disabled '0'
        option country 'CN'

config wifi-iface
        option device   'radio0'
        option ssid     'YourWifiSsid'
        option key 'YourWifiPassword'
        option encryption 'psk2'
        option network 'wwan'
        option mode 'sta'
```

**Note:** If you used the `option encryption 'psk'` it means to use the old WPA encryption, so check that your router allows it.
You may also need to set Wi-Fi "Encryption" setting from TKIP or AES to Auto. Similarly, the "Version" setting from WPA2-PSK to Auto.

Once you changed the settings reboot the device with `reboot` and wait until it connects to your Wi-Fi network.
Go to your router admin panel (usually http://192.168.1.1/ or http://192.168.0.1/) and find a new DHCP client in LAN.
That should be the Kankun socket. We need to make its IP address static by its MAC address.
Go to the router DHCP client settings and set the static IP address e.g. `192.168.0.100`.

Now go back to the `~/.ssh/config` and replace the old `192.168.10.253` IP with the new.
Now you can check that you still connect to it with `ssh kankun`.


### Disable Kankun remote service
The stock firmware includes a couple of processes (`kkeps_*`) that phone home to servers in China in order to offer
cloud-based access to the device through your smartphone.
If you're keeping the stock firmware, consider disabling these in the startup script `/etc/rc.local`.
You can replace the entire file with `echo 'exit 0' > /etc/rc.local`.
Or you may comment out launching of the services with `#`. Edit with `vi /etc/rc.local`:
```sh
# Put your custom commands here that should be executed once
# the system init finished. By default this file does nothing.
#sleep 5
#/sbin/kkeps_on &
#/sbin/kkeps_off &
#/sbin/kkeps_seekwifi &
#/sbin/kkeps_reconect &

exit 0
```

## Operating the relay and LEDs
### Stock firmware
The original image has a with GPIO named `relay` to toggle the relay and see its current state.

Turn relay _ON_:
```sh
echo 1 > /sys/class/leds/tp-link:blue:relay/brightness
```
Turn relay _OFF_:
```sh
echo 0 > /sys/class/leds/tp-link:blue:relay/brightness
```

Toggle relay:
```sh
case "`cat /sys/class/leds/tp-link:blue:relay/brightness`" in 0) echo 1 > /sys/class/leds/tp-link:blue:relay/brightness;; 1) echo 0 > /sys/class/leds/tp-link:blue:relay/brightness;; esac
````

> [!NOTE]
> When the relay is changed using this method, the official app will not track that change.
> As a result you'll need to press twice on the physical button on the device to get the output to toggle.
> This is because the system and official app thinks that the output is already _ON_, so it turns it _OFF_, while it was already _OFF_.


#### Get the socket state
See the current state:
```sh
cat /sys/class/leds/tp-link:blue:relay/brightness
```
The output `0` means _OFF_, the `1` means _ON_.

For automation with the Trigger app (see bellow) use:
```sh
case "`cat /sys/class/leds/tp-link:blue:relay/brightness`" in 0) echo '"state":"open"';; 1) echo '"state":"closed"' ;; esac
```


### Vanilla OpenWrt
The OpenWrt 15.05 for the WR703N doesn't have the named `relay` LED for GPIO 26, and it's not defined in the BSP.

Set up:
```sh
echo 26 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio26/direction
```
**Note:** you should put the setup to `/etc/rc.local` to make sure it's done after the device boots.

Turn relay _ON_:
```sh
echo 1 > /sys/devices/virtual/gpio/gpio26/value
```
Turn relay _OFF_:
```sh
echo 0 > /sys/devices/virtual/gpio/gpio26/value
```


### LEDs configuration
There is a configuration for `flashing` blue LED and `Relay` pseudo LED that controls the relay.
See their config with `cat /etc/config/system`:
```
config led
    option name 'flashing'
    option sysfs 'tp-link:blue:config'
    option trigger 'timer'
    option delayon '800'
    option delayoff '800'

config led
    option name 'Relay'
    option sysfs 'tp-link:blue:relay'
    option trigger 'none'
    option default '1'
```

The `flashing` LED (`system.@led[0]` in UCI) is used to just blink the blue LED each 800 milliseconds.
The `Relay` pseudo LED (`system.@led[1]` in UCI) for the relay has default value `1` i.e. is _ON_.

See [OpenWrt LED configuration](https://openwrt.org/docs/guide-user/base-system/led_configuration) for details.


#### Power on reboot
Stopping the plug from turning on when it boots.
If you had a power outage, then after electricity is back, the relay will be _ON_ by default.
The relay is tied to the LED `flashing`, so setting the LED to default `0` will make the relay _OFF_ after bootup:
```sh
uci set system.@led[1].default=0
uci commit system
```
Check with `cat /etc/config/system`:
```
config led
  option name 'Relay'
  option sysfs 'tp-link:blue:relay'
  option trigger 'none'
  option default '0'
```

To test it you can reboot the device with `reboot` command.
**Note:** During reboot from `reboot` command the relay will turn _OFF_ anyway until booted again.


#### Blue LED
For the stock firmware, you can configure the LEDs to act on certain events.
The blue LED `flashing` is annoyingly blinking each 800ms. We can increase this interval:
```sh
uci set system.@led[0].delayon=20000
uci commit system
/etc/init.d/led restart
```

Blink blue LED with network traffic:
```sh
uci set system.@led[0].name=wwan-link
uci set system.@led[0].trigger=netdev
uci set system.@led[0].dev=wlan0
uci set system.@led[0].mode='link tx rx'
uci commit system
/etc/init.d/led restart
```


## Automation
### Using remote SSH command execution
You can use ssh to remotely execute the command to switch the relay:

Turn relay _ON_ on SSH host `kankun`:
```sh
ssh kankun 'echo 1 > /sys/class/leds/tp-link:blue:relay/brightness'
```
Turn relay _OFF_ on SSH host `kankun`:
```sh
ssh kankun 'echo 0 > /sys/class/leds/tp-link:blue:relay/brightness'
```

Toggle relay on SSH host `kankun`:
```sh
ssh kankun 'case "`cat /sys/class/leds/tp-link:blue:relay/brightness`" in 0) echo 1 > /sys/class/leds/tp-link:blue:relay/brightness;; 1) echo 0 > /sys/class/leds/tp-link:blue:relay/brightness;; esac'
````

You can create a desktop shortcut to execute the command.

#### Linux: desktop shortcut
Create launcher file `~/.local/share/applications/kankun-toggle.desktop`:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Toggle Outlet
Icon=system-shutdown
Exec=/usr/bin/ssh kankun 'case "`cat /sys/class/leds/tp-link:blue:relay/brightness`" in 0) echo 1 > /sys/class/leds/tp-link:blue:relay/brightness;; 1) echo 0 > /sys/class/leds/tp-link:blue:relay/brightness;; esac'
Comment=Toggle KanKun relay ON or OFF
Categories=Utility;Electronics;Internet
Terminal=false
```

Now you can find in the Start menu "Toggle Outlet" and click it to toggle the relay.


### Android: Use Trigger app to remote SSH command execution
The [Trigger app](https://f-droid.org/packages/com.example.trigger/) initially was developed for locks and doors,
but it can be used to control any device over SSH.
Open the app and scan this QR code:

![QR code for Trigger to add Kankun plug](https://github.com/user-attachments/assets/60300623-fc5a-43fc-ba93-fd73a1c3fd12)

You may edit the device's "lock" and change its IP address and SSH password if needed.


### Install REST API
It's recommended to install a CGI script [kankun-json](https://github.com/homedash/kankun-json) that provides an API over HTTP(S).
It also has a small Web UI so you can control the light from your browser.

![kankun-json web panel](https://camo.githubusercontent.com/0cf92e335e876977a02581f038ab4eb15758aae70519e2596c5bcded105c1cb3/68747470733a2f2f636c6475702e636f6d2f49575549416a7232704a2d3132303078313230302e706e67)

* https://github.com/homedash/kankun-manager a full installer and configurer with Ansible.
* [Vanilla OpenWrt version of json.cgi](https://blog.donbowman.ca/wp-content/uploads/2018/01/json.cgi_.txt)
* [Change switch IP in the /www/switches.json when it changes](https://gist.github.com/ferstar/6ebad5e70e17a9f4c05dabed7bf79d7b)

The Home Assistant has a [module](https://www.home-assistant.io/integrations/kankun/) that uses the CGI script.
But you can also use the SSH command to control the light without installing anything on the device.

There is also another version https://github.com/sean-/kankun. It's based on the `kankun-json` but looks older.

https://github.com/CodeFoodPixels/kankun-setup CLI setup script. Connects through SSH to the plug,
configures it to be on the Wi-Fi network specified, copies any files in the setup folder, restarts the plug, and then runs the `install.sh` file.

Once you installed the CGI script for the REST API, you can use it with the same [Trigger](https://f-droid.org/packages/com.example.trigger/) app
but also with any other app that supports HTTP requests, e.g. [HTTP Request Shortcuts](https://f-droid.org/packages/ch.rmy.android.http_shortcuts/).

[Python script for remote control](https://drive.google.com/drive/u/2/folders/0B9JxR8qe_XORRWV0aHI5SXFYeTA)

https://github.com/metalx1000/Kankun-Smart-GUI a simpler version of the `kankun-json`.


#### relay.cgi
The `kankun-json` is based on a simple `relay.cgi`. You can put the CGI script on the device to `/www/cgi-bin/relay.cgi` and make it executable with `chmod +x /www/cgi-bin/relay.cgi`:
```sh
#!/bin/sh
echo "Content-Type: text/plain"
echo "Cache-Control: no-cache, must-revalidate"
echo "Expires: Sat, 26 Jul 1997 05:00:00 GMT"
echo

RELAY_CTRL=/sys/class/leds/tp-link:blue:relay/brightness

case "$QUERY_STRING" in
  state) 
    case "`cat $RELAY_CTRL`" in
      0) echo "OFF";;
      1) echo "ON" ;;
    esac;;
  on) 
    echo 1 > $RELAY_CTRL
    echo ON;;
  off) 
    echo 0 > $RELAY_CTRL
    echo OFF;;
  toggle)
    case "`cat $RELAY_CTRL`" in
      0) echo 1 > $RELAY_CTRL
         echo "ON";;
      1) echo 0 > $RELAY_CTRL
         echo "OFF" ;;
    esac;;    
esac
```
On Windows you can use [WinSCP](https://winscp.net/) to copy the file to the device.

Now you can issue commands to the smart plug from a web browser connected to the same network as the socket.
Change the IP address (e.g. `192.168.0.100`) to the appropriate one for your device.

* https://192.168.0.100/cgi-bin/relay.cgi?state enquire whether the relay is _ON_ or _OFF_.
* https://192.168.0.100/cgi-bin/relay.cgi?on turn the relay _ON_.
* https://192.168.0.100/cgi-bin/relay.cgi?off turn the relay _OFF_.
* https://192.168.0.100/cgi-bin/relay.cgi?toggle toggle the relay from _ON_ to _OFF_, or _OFF_ to _ON_.

The original script was written by Konstantin Dondoshanskiy.


### Configuring the plug in OpenHAB
You maye use the [OpenHAB](https://www.openhab.org/) with [http binding](https://www.openhab.org/addons/bindings/http/).

In the `default.items` file, you configure the switch with an HTTP binding by telling it what the URLs are for turning it on and off (change 192.168.0.100 to your switch's IP address):

```
Switch	KanKun1 "KanKun" (GF_Living) { http=">[ON:GET:http://192.168.0.100/cgi-bin/relay.cgi?on] >[OFF:GET:http://192.168.0.100/cgi-bin/relay.cgi?off]" }
```
Adding a switch to the `default.sitemap` is very simple:
```
Frame label="Switches" {
    Switch item=KanKun1
}
```
This should add the KanKun switch in OpenHAB.


### Using native protocol

> [!WARNING]
> This is not recommended and may not work anymore.
> Please let us know if this works and improve the instructions.

You may try to control a Kankun Plug using the stock protocol, no hacks.
* [Kankun controller](https://github.com/0x00string/kankuncontroller) a Python app
* [Kankun plug gist for MacOS (OSX)](https://gist.github.com/oscarmorrison/6ebd9344e16448121ef4a5cdea1427b4) a Python script using native protocol


## Flashing to OpenWrt firmware

> [!WARNING]
> Unless you really need it don't do this.

The original firmware is very outdated, and the Dropbear SSH server on it has some security vulnerability.

Flashing stock OpenWrt from the shell using sysupgrade works fine.
Confirmed to work with `openwrt-15.05.1-ar71xx-generic-tl-wr703n-v1-squashfs-sysupgrade.bin`.
Newer OpenWrt images may be too big for the device with a small flash.

**BEWARE**, there are problems:
* The device has no ethernet port, so wireless must be enabled.
* Vanilla OpenWrt firmware images have wireless disabled.

Theoretically `sysupgrade -c` should solve these problems,
but for me 1 out of 3 Chaos Calmer upgrades failed to preserve `/etc/config/wireless` and other changed config files,
leaving the device unreachable.

You might want to play around with sysupgrade `-l`, `-T` or `-i` to make sure your config files are preserved during upgrade.
Perhaps `-b` and `-f` is the safest way.

Another option would be to use the [OpenWrt firmware image builder](https://openwrt.org/docs/guide-developer/toolchain/beginners-build-guide)
and customize the image to include a wireless configuration that's enabled by default.
Flashing this custom image would be safer in regard to misbehaving `sysupgrade -c`.
Use `-v` with `sysupgrade`, since that will tell you which files will be preserved.

If the device has its wireless interface disabled, i.e., unreachable,
you will have to open the case and solder cables to the serial headers on the pcb to fix it.

See also:
* [kankun-firmware](https://github.com/andrewc12/kankun-firmware) and [buildenv and quilt_rev10.txt](https://gist.github.com/andrewc12/21f92b64feaa0ce0763ea0b5439448a8) Build firmware for Kankun small k (KK-SP3) **EXPERIMENTAL!**
* [Patch to enable the device support](https://gist.github.com/andrewc12/cb1ce8804629a2c6ce10a2b62bc4842a).


## Manual

<img width="1600" height="561" alt="Kankun KK-SP3 Manual" src="https://github.com/user-attachments/assets/b92f2c5e-1b76-421f-945f-6c9247b02217" />

Copied [from Dropbox](https://www.dropbox.com/s/8sq4caf2iivcmmc/manual-english.png?dl=0)


## Articles and reviews
The page is based on the [removed OpenWrt wiki page](https://openwrt.org/toh/kankun/kk-sp3?rev=1621192123) and all of this articles:

* [More hacking to secure the gadget army the Kankun SP3](https://blog.donbowman.ca/2018/01/30/more-hacking-to-secure-the-gadget-army-the-kankun-sp3/)
* [Cheap WIFI Switch review (KK-SP3)](https://mbarabasz.wordpress.com/2015/06/25/cheap-wifi-switch-review-kk-sp3/)
* Unofficial [Kankun Blog](https://kankunblog.wordpress.com) Thoughts and rants for KanKun KK-SP3: mostly how to use the official app
* [The Kankun Smart WiFi Plug/Outlet and ESP8266](https://benlo.com/esp8266/KankunSmartPlug.html) and [sources](https://github.com/GeoNomad/LuaLoader/tree/master/examples/Kankun%20WiFi%20Plug)
* [Hacker News thread about the device](https://news.ycombinator.com/item?id=11952627)
* [KanKun - WiFi розетка с управлением через интернет](https://zftlab.org/pages/2015081200.html)
* mysku.ru: [WiFi розетка Kankun](http://mysku.ru/blog/china-stores/28305.html)
* mysku.ru: [Умная розетка от Сяоми – версия номер 2](http://mysku.ru/blog/china-stores/40018.html)
* [Wifi розетка KanKun](http://www.wofc.ru/kankun.html)
* [Hacking Kankun Smart Wifi Plug](https://www.anites.com/2015/01/hacking-kankun-smart-wifi-plug.html)
* hfuller: [Kankun Plug hacking](https://256.makerslocal.org/wiki/Kankun_Plug)
* [闲鱼买了两kk-sp3插座](https://blog.ferstar.org/post/hacking-kankun-smart-wifi-plug/)
* CNX-Software: [Kankun KK-SP3 Wi-Fi Smart Socket Hacked, Based on Atheros AR9331, Running OpenWRT](https://www.cnx-software.com/2014/07/28/kankun-kk-sp3-wi-fi-smart-socket-hacked-based-on-atheros-ar9331-running-openwrt/)
* [Discussion of some of the security failings of the device, but also its official control protocol](https://mjg59.dreamwidth.org/43486.html)
* YouTube
  * "How to Linux" channel: 
    * [Finding IP of Kankun KK-SP3 WiFi smart plug in router](https://www.youtube.com/watch?v=Rc4PG0jxX8o)
    * [Webserver](https://www.youtube.com/watch?v=qpc3ZJiN-JQ)
    * [Commandline Hack](https://www.youtube.com/watch?v=yVysjg2lEqQ)
  * [WidgetKK for SmartPlug](https://www.youtube.com/@ChopLabalagun/search?query=kankun)
  * [Обзор Kankun Smart Plug Socket Wi-Fi Умной интернет розетки](https://www.youtube.com/watch?v=_bRHiE1qKzg)


## Alternative sockets
* Orvibo S20 socket
  * [Reverse engineering Orvibo S20 socket](https://stikonas.eu/wordpress/2015/02/24/reverse-engineering-orvibo-s20-socket/)
  * https://github.com/fernadosilva/orvfms Web interface for the Orvibo S20 socket


## Boot log
<details>
  <summary>Boot log of stock firmware (OpenWrt)</summary>

```
Dec 16 01:17:49 ÿ
Dec 16 01:17:49  
Dec 16 01:17:49 U-Boot 1.1.4 (Aug 27 2011 - 10:39:39)
Dec 16 01:17:49  
Dec 16 01:17:49 AP121-2MB (ar9330) U-boot
Dec 16 01:17:49  
Dec 16 01:17:49 DRAM:  32 MB
Dec 16 01:17:49 led turning on for 1s...
Dec 16 01:17:50 id read 0x100000ff
Dec 16 01:17:50 flash size 4194304, sector count = 64
Dec 16 01:17:50 Flash:  4 MB
Dec 16 01:17:50 Using default environment
Dec 16 01:17:50  
Dec 16 01:17:50 In:    serial
Dec 16 01:17:50 Out:   serial
Dec 16 01:17:50 Err:   serial
Dec 16 01:17:50 Net:   ag7240_enet_initialize...
Dec 16 01:17:50 Fetching MAC Address from 0x81ff41b8
Dec 16 01:17:50 Fetching MAC Address from 0x81ff41b8
Dec 16 01:17:50 : cfg1 0x5 cfg2 0x7114
Dec 16 01:17:50 eth0: xx:xx:xx:xx:xx:xx
Dec 16 01:17:50 ag7240_phy_setup
Dec 16 01:17:50 eth0 up
Dec 16 01:17:50 : cfg1 0xf cfg2 0x7214
Dec 16 01:17:50 eth1: xx:xx:xx:xx:xx:xx
Dec 16 01:17:50 athrs26_reg_init_lan
Dec 16 01:17:50 ATHRS26: resetting s26
Dec 16 01:17:50 ATHRS26: s26 reset done
Dec 16 01:17:50 ag7240_phy_setup
Dec 16 01:17:50 eth1 up
Dec 16 01:17:50 eth0, eth1
Dec 16 01:17:50 Autobooting in 1 seconds
Dec 16 01:17:51 ## Booting image at 9f020000 ...
Dec 16 01:17:53    Uncompressing Kernel Image ... OK
Dec 16 01:17:53  
Dec 16 01:17:53 Starting kernel ...
Dec 16 01:17:53  
Dec 16 01:17:53 [    0.000000] Linux version 3.10.26 (zhaoyuanbiao@ubuntu)(gcc version 4.6.4 (OpenWrt/Linaro GCC 4.6-2013.05 r39365) ) #44 Tue Jul 29 11:44:32 CST 2014
Dec 16 01:17:53 [    0.000000] bootconsole [early0] enabled
Dec 16 01:17:53 [    0.000000] CPU revision is: 00019374 (MIPS 24Kc)
Dec 16 01:17:53 [    0.000000] SoC: Atheros AR9330 rev 1
Dec 16 01:17:53 [    0.000000] Clocks: CPU:400.000MHz, DDR:400.000MHz, AHB:200.000MHz, Ref:25.000MHz
Dec 16 01:17:53 [    0.000000] Determined physical RAM map:
Dec 16 01:17:53 [    0.000000]  memory: 02000000 @ 00000000 (usable)
Dec 16 01:17:53 [    0.000000] Initrd not found or empty - disabling initrd
Dec 16 01:17:53 [    0.000000] Zone ranges:
Dec 16 01:17:53 [    0.000000]   Normal   [mem 0x00000000-0x01ffffff]
Dec 16 01:17:53 [    0.000000] Movable zone start for each node
Dec 16 01:17:53 [    0.000000] Early memory node ranges
Dec 16 01:17:53 [    0.000000]   node   0: [mem 0x00000000-0x01ffffff]
Dec 16 01:17:53 [    0.000000] Primary instruction cache 64kB, VIPT, 4-way, linesize 32 bytes.
Dec 16 01:17:53 [    0.000000] Primary data cache 32kB, 4-way, VIPT, cache aliases, linesize 32 bytes
Dec 16 01:17:53 [    0.000000] Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 8128
Dec 16 01:17:53 [    0.000000] Kernel command line:  board=TL-WR703N console=ttyATH0,115200 rootfstype=squashfs,jffs2 noinitrd
Dec 16 01:17:53 [    0.000000] PID hash table entries: 128 (order: 3, 512 bytes)
Dec 16 01:17:53 [    0.000000] Dentry cache hash table entries: 4096 (order: 2, 16384 bytes)
Dec 16 01:17:53 [    0.000000] Inode-cache hash table entries: 2048 (order: 1, 8192 bytes)
Dec 16 01:17:53 [    0.000000] Writing ErrCtl register=00000000
Dec 16 01:17:53 [    0.000000] Readback ErrCtl register=00000000
Dec 16 01:17:53 [    0.000000] Memory: 28784k/32768k available (2201k kernel code, 3984k reserved, 592k data, 276k init, 0k highmem)
Dec 16 01:17:53 [    0.000000] SLUB: HWalign=32, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
Dec 16 01:17:53 [    0.000000] NR_IRQS:51
Dec 16 01:17:53 [    0.000000] Calibrating delay loop... 265.42 BogoMIPS (lpj=1327104)
Dec 16 01:17:53 [    0.080000] pid_max: default: 32768 minimum: 301
Dec 16 01:17:53 [    0.080000] Mount-cache hash table entries: 512
Dec 16 01:17:53 [    0.090000] NET: Registered protocol family 16
Dec 16 01:17:53 [    0.100000] MIPS: machine is TP-LINK TL-WR703N v1
Dec 16 01:17:53 [    0.350000] bio: create slab <bio-0> at 0
Dec 16 01:17:53 [    0.360000] Switching to clocksource MIPS
Dec 16 01:17:53 [    0.360000] NET: Registered protocol family 2
Dec 16 01:17:53 [    0.370000] TCP established hash table entries: 512 (order: 0, 4096 bytes)
Dec 16 01:17:53 [    0.370000] TCP bind hash table entries: 512 (order: -1, 2048 bytes)
Dec 16 01:17:53 [    0.370000] TCP: Hash tables configured (established 512 bind 512)
Dec 16 01:17:53 [    0.380000] TCP: reno registered
Dec 16 01:17:53 [    0.380000] UDP hash table entries: 256 (order: 0, 4096 bytes)
Dec 16 01:17:53 [    0.390000] UDP-Lite hash table entries: 256 (order: 0, 4096 bytes)
Dec 16 01:17:53 [    0.400000] NET: Registered protocol family 1
Dec 16 01:17:53 [    0.420000] squashfs: version 4.0 (2009/01/31) Phillip Lougher
Dec 16 01:17:53 [    0.420000] jffs2: version 2.2 (NAND) (SUMMARY) (LZMA) (RTIME) (CMODE_PRIORITY) (c) 2001-2006 Red Hat, Inc.
Dec 16 01:17:53 [    0.430000] msgmni has been set to 56
Dec 16 01:17:53 [    0.440000] io scheduler noop registered
Dec 16 01:17:53 [    0.440000] io scheduler deadline registered (default)
Dec 16 01:17:53 [    0.450000] Serial: 8250/16550 driver, 1 ports, IRQ sharing disabled
Dec 16 01:17:53 [    0.450000] ar933x-uart: ttyATH0 at MMIO 0x18020000 (irq = 11) is a AR933X UART
Dec 16 01:17:53 [    0.460000] console [ttyATH0] enabled, bootconsole disabled
Dec 16 01:17:53 [    0.460000] console [ttyATH0] enabled, bootconsole disabled
Dec 16 01:17:53 [    0.470000] ath79-spi ath79-spi: master is unqueued, this is deprecated
Dec 16 01:17:53 [    0.480000] m25p80 spi0.0: found w25q32, expected m25p80
Dec 16 01:17:53 [    0.480000] m25p80 spi0.0: w25q32 (4096 Kbytes)
Dec 16 01:17:53 [    0.490000] 5 tp-link partitions found on MTD device spi0.0
Dec 16 01:17:53 [    0.490000] Creating 5 MTD partitions on "spi0.0":
Dec 16 01:17:53 [    0.500000] 0x000000000000-0x000000020000 : "u-boot"
Dec 16 01:17:53 [    0.500000] 0x000000020000-0x000000119a18 : "kernel"
Dec 16 01:17:53 [    0.510000] mtd: partition "kernel" must either start or end on erase block boundary or be smaller than an erase block - forcing read-only
Dec 16 01:17:53 [    0.520000] 0x000000119a18-0x0000003f0000 : "rootfs"
Dec 16 01:17:53 [    0.530000] mtd: partition "rootfs" must either start or end on erase block boundary or be smaller than an erase block -- forcing read-only
Dec 16 01:17:53 [    0.540000] mtd: device 2 (rootfs) set to be root filesystem
Dec 16 01:17:53 [    0.540000] 1 squashfs-split partitions found on MTD device rootfs
Dec 16 01:17:53 [    0.550000] 0x0000002f0000-0x0000003f0000 : "rootfs_data"
Dec 16 01:17:53 [    0.560000] 0x0000003f0000-0x000000400000 : "art"
Dec 16 01:17:53 [    0.560000] 0x000000020000-0x0000003f0000 : "firmware"
Dec 16 01:17:53 [    0.580000] libphy: ag71xx_mdio: probed
Dec 16 01:17:54 [    1.140000] ag71xx ag71xx.0: connected to PHY at ag71xx-mdio.1:04 [uid=004dd041, driver=Generic PHY]
Dec 16 01:17:54 [    1.150000] eth0: Atheros AG71xx at 0xb9000000, irq 4, mode:MII
Dec 16 01:17:54 [    1.150000] TCP: cubic registered
Dec 16 01:17:54 [    1.150000] NET: Registered protocol family 17
Dec 16 01:17:54 [    1.160000] 8021q: 802.1Q VLAN Support v1.8
Dec 16 01:17:54 [    1.170000] VFS: Mounted root (squashfs filesystem) readonly on device 31:2.
Dec 16 01:17:54 [    1.180000] Freeing unused kernel memory: 276K (8031b000 - 80360000)
Dec 16 01:17:55 procd: Console is alive
Dec 16 01:17:55 procd: - watchdog 
Dec 16 01:17:55 procd: - preinit -
Dec 16 01:17:57 Press the [f] key and hit [enter] to enter failsafe mode
Dec 16 01:17:57 Press the [1], [2], [3] or [4] key and hit [enter] to select the debug level
Dec 16 01:17:59 mount_root: jffs2 is ready
Dec 16 01:17:59 [    6.160000] jffs2: notice: (292) jffs2_build_xattr_subsystem: complete building xattr subsystem, 3 of xdatum (1 unchecked, 2 orphan) and 43 of xref (0 dead, 30 orphan) found.
Dec 16 01:17:59 procd: - early -
Dec 16 01:17:59 procd: - watchdog -
Dec 16 01:18:00 procd: - ubus -
Dec 16 01:18:00 procd: - init -
Dec 16 01:18:00 Please press Enter to activate this console.
Dec 16 01:18:00 [    7.350000] NET: Registered protocol family 10
Dec 16 01:18:00 [    7.360000] nf_conntrack version 0.5.0 (454 buckets, 1816 max)
Dec 16 01:18:00 [    7.370000] ip6_tables: (C) 2000-2006 Netfilter Core Team
Dec 16 01:18:00 [    7.400000] Loading modules backported from Linux version master-2013-11-05-0-gafa3093
Dec 16 01:18:00 [    7.410000] Backport generated by backports.git backports-20130802-0-gdb67a3f
Dec 16 01:18:00 [    7.420000] ip_tables: (C) 2000-2006 Netfilter Core Team
Dec 16 01:18:00 [    7.470000] xt_time: kernel timezone is -0000
Dec 16 01:18:00 [    7.500000] cfg80211: Calling CRDA to update world regulatory domain
Dec 16 01:18:00 [    7.500000] cfg80211: World regulatory domain updated:
Dec 16 01:18:00 [    7.510000] cfg80211:   (start_freq - end_freq @ bandwidth), (max_antenna_gain, max_eirp)
Dec 16 01:18:00 [    7.510000] cfg80211:   (2402000 KHz - 2472000 KHz @ 40000 KHz), (300 mBi, 2000 mBm)
Dec 16 01:18:00 [    7.520000] cfg80211:   (2457000 KHz - 2482000 KHz @ 40000 KHz), (300 mBi, 2000 mBm)
Dec 16 01:18:00 [    7.530000] cfg80211:   (2474000 KHz - 2494000 KHz @ 20000 KHz), (300 mBi, 2000 mBm)
Dec 16 01:18:00 [    7.540000] cfg80211:   (5170000 KHz - 5250000 KHz @ 80000 KHz), (300 mBi, 2000 mBm)
Dec 16 01:18:00 [    7.540000] cfg80211:   (5735000 KHz - 5835000 KHz @ 80000 KHz), (300 mBi, 2000 mBm)
Dec 16 01:18:00 [    7.550000] cfg80211:   (57240000 KHz - 63720000 KHz @ 2160000 KHz), (N/A, 0 mBm)
Dec 16 01:18:00 [    7.630000] PPP generic driver version 2.4.2
Dec 16 01:18:00 [    7.630000] NET: Registered protocol family 24
Dec 16 01:18:01 [    7.730000] ieee80211 phy0: Atheros AR9330 Rev:1 mem=0xb8100000, irq=2
Dec 16 01:18:01 [    7.740000] cfg80211: Calling CRDA for country: US
Dec 16 01:18:01 [    7.740000] cfg80211: Regulatory domain changed to country: US
Dec 16 01:18:01 [    7.750000] cfg80211:  DFS Master region FCC
Dec 16 01:18:01 [    7.750000] cfg80211:   (start_freq - end_freq @ bandwidth), (max_antenna_gain, max_eirp)
Dec 16 01:18:01 [    7.760000] cfg80211:   (2402000 KHz - 2472000 KHz @ 40000 KHz), (300 mBi, 2700 mBm)
Dec 16 01:18:01 [    7.770000] cfg80211:   (5170000 KHz - 5250000 KHz @ 80000 KHz), (300 mBi, 1700 mBm)
Dec 16 01:18:01 [    7.770000] cfg80211:   (5250000 KHz - 5330000 KHz @ 80000 KHz), (300 mBi, 2400 mBm)
Dec 16 01:18:01 [    7.780000] cfg80211:   (5490000 KHz - 5600000 KHz @ 80000 KHz), (300 mBi, 2400 mBm)
Dec 16 01:18:01 [    7.790000] cfg80211:   (5650000 KHz - 5710000 KHz @ 40000 KHz), (300 mBi, 2400 mBm)
Dec 16 01:18:01 [    7.800000] cfg80211:   (5735000 KHz - 5835000 KHz @ 80000 KHz), (300 mBi, 3000 mBm)
Dec 16 01:18:01 [    7.810000] cfg80211:   (57240000 KHz - 63720000 KHz @ 2160000 KHz), (N/A, 4000 mBm)
Dec 16 01:18:07 [   14.020000] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready
Dec 16 01:18:08 [   15.180000] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
Dec 16 01:18:08 procd: - init complete -
Dec 16 01:18:10 [   17.240000] wlan0: authenticate with xx:xx:xx:xx:xx:xx
Dec 16 01:18:10 [   17.250000] wlan0: send auth to xx:xx:xx:xx:xx:xx (try 1/3)
Dec 16 01:18:10 [   17.260000] wlan0: authenticated
Dec 16 01:18:10 [   17.270000] wlan0: associate with xx:xx:xx:xx:xx:xx (try 1/3)
Dec 16 01:18:10 [   17.270000] wlan0: RX AssocResp from xx:xx:xx:xx:xx:xx (capab=0x431 status=0 aid=2)
Dec 16 01:18:10 [   17.280000] wlan0: associated
Dec 16 01:18:10 [   17.280000] IPv6: ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready
Dec 16 01:18:14  
Dec 16 01:18:14  
Dec 16 01:18:14  
Dec 16 01:18:14 BusyBox v1.19.4 (2014-03-27 17:39:06 CST) built-in shell (ash)
Dec 16 01:18:14 Enter 'help' for a list of built-in commands.
Dec 16 01:18:14  
Dec 16 01:18:14   _    _               _    
Dec 16 01:18:14  | | _| ___ ___  | | | ___ __
Dec 16 01:18:14  |    |     ||     ||    |     ||    |
Dec 16 01:18:14  | |   |    ||  |  || |   |  __||   |
Dec 16 01:18:14  |  _ - |_____||__|__||  _ -_ |_____||__|
Dec 16 01:18:14  |_| -__|  S M A L L   |_| -__| S M A R T
Dec 16 01:18:14  ----------------------------------------------------
Dec 16 01:18:14  KONKE Technology Co., Ltd. All rights reserved.
Dec 16 01:18:14  ---------------------------------------------------
Dec 16 01:18:14   * www.konke.com            All other products and
Dec 16 01:18:14   * QQ:27412237              company names mentioned
Dec 16 01:18:14   * 400-871-3766             may be the trademarks of
Dec 16 01:18:14   * fae@konke.com            their respective owners.
Dec 16 01:18:14  ---------------------------------------------------
Dec 16 01:18:18  root@koven:/#
```
</details>


## Tags
ar71xx AR9330 4Flash 32RAM 0port 0nic ath9k 802.11bgn wall_plug

