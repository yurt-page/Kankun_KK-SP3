# Kankun KK-SP3: Полное руководство
[In English](./README.md)

"Kankun Smart Plug", также известная как "Huafeng WiFi Plug", "Small K WiFi switch" это недорагая электророзетка управляемая по Wi-Fi .
В линейке представлено множество моделей, совместимых с североамериканскими, европейскими, австралийскими и британскими вилками и розетками.

Внутри этого невзрачного на вид адаптера находится Wi-Fi роутер, работающий на прошивке [OpenWrt](https://openwrt.org).
Его аппаратная часть аналогична роутеру [TP-link TL-WR703N](https://openwrt.org/toh/tp-link/tl-wr703n), поэтому вы можете установить чистую версию OpenWrt вместо оригинальной прошивки от производителя.
Роутер подключен к реле на 10 Ампер, способному выдерживать мощность до 2000 Ватт.
Это устройство полностью поддается модификации, и внутри него установлена полноценная операционная система Linux!

Существовали приложения для Android и iOS, позволяющие управлять этой розеткой, но они больше недоступны.
Приложение для Android (на китайском языке) можно найти здесь: https://apkcombo.com/es/smartplug/hangzhou.kankun/
Демонстрация приложения: https://www.youtube.com/watch?v=xsVjhS9BROM

Поэтому вам потребуется получить доступ к командной строке розетки и настроить её вручную.
Альтернативы официальным приложениям см. в разделе [Автоматизация](#Автоматизация) ниже.

## Возможности
* Прошивка: OpenWrt 14 Barrier Breaker r39365 TARGET="ar71xx/generic".
* Система на чипе: Atheros AR9330 rev 1 at 400MHz. См. [datasheet](https://www.openhacks.com/uploadsproductos/ar9331_datasheet.pdf).
* 4 MB постоянной памяти.
* 32 MB оперативной памяти Winbond W9425G6JH.
* Wi-Fi 802.11 b/g/n.
* Нет входа ethernet или USB.
* Питается от электросети.
* Реле контролирующее розетку нагрузки: OMRON HF32F-G/012-H
  * 10 Амперов или 2,200 Ватт. **Если её перегрузите то возникнет пожар. Особенно во время жары или лета.**
  * Максимальное коммутируемое напряжение постоянного тока: 30 В
  * Максимальный коммутируемый ток: 10 А
  * Максимальная коммутируемая мощность: 300 Вт
  * Номинальное напряжение катушки постоянного тока: 12 В
  * Максимальное напряжение катушки: -15,6 В
  * Сопротивление катушки: 320 Ом
  * Мощность катушки: 450 мВт

> [!CAUTION]
> Превышение мощности в 2200 Вт может привести к пожару, особенно в жару или летом.
> См. столбец «Максимальная потребляемая мощность» в разделе [Потребление электроэнергии бытовыми приборами](https://www.daftlogic.com/information-appliance-power-consumption.htm).
> Особенно не используйте его для:
> * Бытового кондиционера, испарительного кондиционера, обогревателя;
> * Бойлера, электрической духовки, гидромассажной ванны, джакузи, водонагревателя, мойки рук, душевой кабины с мощным напором воды;
> * Парового утюга, фена, сушилки для белья;
> * Зарядного устройства для электромобилей;

## Фотографии
<img width="640" height="480" alt="Kankun KK-SP3: обратная сторона с вилкой" src="https://github.com/user-attachments/assets/c06fec92-c45c-4a27-85ca-e9da46a2f567" />
<details>
  <summary>Подробные фото</summary>

На передней панели расположен универсальный разъём, подходящий для всех типов вилок.
Также видны индикаторные лампочки и кнопка управления. Одна лампочка загорается синим цветом при загрузке и мигает синим, когда устройство готово.
Вторая лампочка загорается красным, когда устройство включено.
Кнопка позволяет осуществлять локальное управление устройством без доступа в интернет.
<img width="640" height="480" alt="Kankun KK-SP3: front with socket" src="https://github.com/user-attachments/assets/34cb52f1-64a0-4f73-aef0-9c0633077a87" />

Для разборки просуньте что-нибудь тонкое, например, пластиковую карту, в зазор между корпусом и крышкой в любом месте.
<img width="640" height="480" alt="Kankun KK-SP3: disassembly" src="https://github.com/user-attachments/assets/f8a4329a-2d17-45cb-8da9-a5a2c55106e9" />

Устройство состоит из двух основных частей: розетки с блоком питания и вилкой, а также модуля Wi-Fi, подключённого через шестиконтактный микроразъём.
<img width="640" height="480" alt="Kankun KK-SP3: two parts" src="https://github.com/user-attachments/assets/c98a2a20-1401-4bfb-93d4-83ddaf87c070" />
</details>


## Серьёзная проблема безопасности!

> [!CAUTION]
> В версии для США/Северной Америки вместо *фазы* меняют местами *нейтральный* провод!
> Это означает что когда розетка выключена, подключенное к нему устройство остаётся под напряжением и готово вас ударить током.
> Я предполагаю, что это связано с тем, что это конструкция для нескольких стран, и они всегда меняют местами провод *слева*.
> Это правильно для Китая/Австралии, но неправильно для Северной Америки; см. соответствующую распиновку:
>
> <img width="640" height="480" alt="Australian Socket-Outlet, Auto Switched" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Australian_Socket-Outlet%2C_Auto_Switched.jpg/1201px-Australian_Socket-Outlet%2C_Auto_Switched.jpg" />


## Сброс до заводских настроек
Вы можете сбросить все существующие настройки и восстановить заводские параметры.
Нажмите и удерживайте почти невидимую белую кнопку на поверхности вилки в течение 4 секунд.
Если не появилась Wi-Fi сеть `OK_SP3` то дополнительно выключите и включите розетку.


## Подключение к устройству
Изначально устройство предварительно настроено как точка доступа Wi-Fi (Access Point, AP).
Подключитесь к её сети Wi-Fi с именем SSID `OK_SP3`, она без пароля (и шифрования).
После подключения в информации о подключении вы увидите «Шлюз по умолчанию IPv4», то есть адрес маршрутизатора, к которому подключено устройство.
Он должен быть `192.168.10.253`.
Вы даже можете открыть его в обозревателе по адресу http://192.168.10.253, но там нет веб-панели администратора, поэтому вы увидите пустую страницу с текстом `Index of /`.


## Получение удалённого доступа к командной оболочке root
Вы можете подключиться через telnet с пользователем root без пароля. Но лучше использовать SSH.

Если у вас ещё нет RSA ключа для SSH, вам потребуется сгенерировать его с помощью команды `ssh-keygen -t rsa`.
На устройстве установлен старый SSH-сервер Dropbear, использующий устаревшие алгоритмы шифрования, поэтому команда `ssh` завершится ошибкой:
```
$ ssh root@192.168.10.253
Unable to negotiate with 192.168.10.253 port 22: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,kexguess2@matt.ucc.asn.au
```
Лучший способ — добавить в файл `~/.ssh/config` конфигурацию разрешающую использование устаревших алгоритмов шифрования:
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

Теперь вы сможете зайти в удалённую командную строку используя команду `ssh root@192.168.10.253` или просто `ssh kankun`.
Пароль пользователя root по умолчанию — `p9z34c`, `admin` или `1234`.


### Установка SSH ключа
Получив root-доступ к оболочке, вы можете настроить авторизацию по ключу, чтобы избежать запроса пароля в следующий раз.
Используйте `ssh-copy-id -i ~/.ssh/id_rsa kankun`, чтобы добавить свой ключ в `/etc/dropbear/authorized_keys` для Dropbear.

### Смена пароля
Чтобы другие вас не взломали, вам следует сменить стандартный пароль с помощью команды `passwd`:
```
# passwd
Changing password for root
New password:
Retype password:
Password for root changed by root
```

## Настройка на изначальной прошивке
### Необязательно: Изменение имени хоста
Имя хоста этой розетки по умолчанию это `koven`.
Если у вас их несколько, вам может потребоваться изменить имя хоста, чтобы их можно было идентифицировать.
```sh
uci set system.hostname='kankun'
uci commit
```
Или измените файл конфигурации напрямую с помощью команды `vi /etc/sysconfig/system`, в этом разделе:
```
config system
    option hostname 'kankun'
```
Чтобы выйти из редактора Vim, нажмите `Esc`, затем введите `wq!` и нажмите `Enter`.


### Настройка сети
Вероятно, вам потребуется использовать устройство в качестве клиента в вашей существующей сети Wi-Fi:
Вам нужно будет изменить `/etc/config/network` и `/etc/config/wireless` на UCI.
```sh
uci set network.wwan=interface
uci set network.wwan.proto=dhcp
uci commit
```

Проверить изменения можно через `cat /etc/config/network`:
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

Измените файл `/etc/config/wireless` и установите пароль для вашей сети Wi-Fi (замените здесь `ВашаWifiСеть` и `ПарольВашейСети`):
```sh
uci set wireless.@wifi-iface[0].ssid='ВашаWifiСеть'
uci set wireless.@wifi-iface[0].key='ПарольВашейСети'
uci set wireless.@wifi-iface[0].encryption='psk2'
uci set wireless.@wifi-iface[0].network='wwan'
uci set wireless.@wifi-iface[0].mode='sta'
uci commit
```

Проверить изменения можно через `cat /etc/config/wireless`:
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

После изменения настроек перезагрузите устройство с помощью команды `reboot` и дождитесь подключения к вашей сети Wi-Fi.
Перейдите в панель администратора вашего маршрутизатора (обычно http://192.168.1.1/ или http://192.168.0.1/) и найдите новый DHCP-клиент в локальной сети.
Это и будет розетка Kankun. Нам нужно сделать её IP адрес статическим по MAC-адресу.
Перейдите в настройки DHCP-клиента маршрутизатора и установите статический IP-адрес, например, `192.168.0.100`.

Теперь вернитесь в файл `~/.ssh/config` и замените старый IP-адрес `192.168.10.253` на новый.
Теперь вы можете проверить, что по-прежнему подключаетесь к розетке, с помощью команды `ssh kankun`.


### Отключение удаленной службы Kankun
В стандартной прошивке есть пара процессов (`kkeps_*`), которые отправляют запросы на серверы в Китае, чтобы обеспечить
облачный доступ к устройству через ваш смартфон.
Если вы используете стандартную прошивку, рассмотрите возможность отключения этих процессов в скрипте запуска `/etc/rc.local`.
Вы можете заменить весь файл с помощью `echo 'exit 0' > /etc/rc.local`.

Или вы можете закомментировать запуск этих служб с помощью `#`. Отредактируйте с помощью `vi /etc/rc.local`:
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

## Управление реле и светодиодами
### Стандартная прошивка
В исходном образе есть интерфейс GPIO с именем `relay` для переключения реле и просмотра его текущего состояния.

Включить реле:
```sh
echo 1 > /sys/class/leds/tp-link:blue:relay/brightness
```
Отключить реле:
```sh
echo 0 > /sys/class/leds/tp-link:blue:relay/brightness
```

Переключение реле:
```sh
case "`cat /sys/class/leds/tp-link:blue:relay/brightness`" in 0) echo 1 > /sys/class/leds/tp-link:blue:relay/brightness;; 1) echo 0 > /sys/class/leds/tp-link:blue:relay/brightness;; esac
````

> [!NOTE]
> При изменении состояния реле этим методом официальное приложение не будет отслеживать это изменение.
> В результате вам потребуется дважды нажать на физическую кнопку на устройстве, чтобы переключить выход.
> Это происходит потому, что система и официальное приложение считают, что выход уже _ВКЛЮЧЁН_, поэтому они выключают его, хотя он уже был _ОТКЛЮЧЧЁН_.

#### Получение состояния розетки
Просмотр текущего состояния:
```sh
cat /sys/class/leds/tp-link:blue:relay/brightness
```
Выходной сигнал `0` означает _ОТКЛЮЧЕНО_, `1` значит _ВКЛЮЧЕННО_.

Для автоматизации с помощью приложения Trigger (см. ниже) используйте:
```sh
case "`cat /sys/class/leds/tp-link:blue:relay/brightness`" in 0) echo '"state":"open"';; 1) echo '"state":"closed"' ;; esac
```


### На чистом OpenWrt
В OpenWrt 15.05 для WR703N отсутствует светодиод с именем `relay` для GPIO 26, и он не определен в BSP.

Настройка:
```sh
echo 26 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio26/direction
```
**Примечание:** Чтобы настройка завершилась после загрузки устройства, следует поместить файл `/etc/rc.local`.

Переключить реле в _ВКЛЮЧЕНО_:
```sh
echo 1 > /sys/devices/virtual/gpio/gpio26/value
```
Переключить реле в _ОТКЛЮЧЕНО_:
```sh
echo 0 > /sys/devices/virtual/gpio/gpio26/value
```


### Настройка индикаторов
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

Светодиод `flashing` LED (в UCI `system.@led[0]` используется чтобы просто мигать синим каждые 800 миллисекунд.
Псевдо светодиод `Relay` LED (в UCI `system.@led[1]`) контролирует само реле и его значение по умолчанию `1` т.е. _ВКЛЮЧЕНО_.

See [OpenWrt LED configuration](https://openwrt.org/docs/guide-user/base-system/led_configuration) for details.


#### Включение питания при перезагрузке
Предотвращение включения розетки при загрузке.
Если у вас было отключение электроэнергии, то после восстановления электроснабжения реле будет _ВКЛЮЧЕНО_ по умолчанию.
Реле привязано к миганию светодиода, поэтому установка светодиода в значение по умолчанию `0` приведёт к тому, что реле будет _ОТКЛЮЧЕНО_ после загрузки:
```sh
uci set system.@led[1].default=0
uci commit system
```
Проверьте изменения с помощью `cat /etc/config/system`:
```
config led
  option name 'Relay'
  option sysfs 'tp-link:blue:relay'
  option trigger 'none'
  option default '0'
```

Для проверки можно перезагрузить устройство с помощью команды `reboot`.
**Примечание:** Во время перезагрузки с помощью команды `reboot` реле всё равно выключится до следующей загрузки.


#### Синий светодиод
В стандартной прошивке можно настроить светодиоды на реагирование на определенные события.
Синий светодиод раздражающе "мигает" каждые 800 мс. Мы можем увеличить этот интервал:
```sh
uci set system.@led[0].delayon=20000
uci commit system
/etc/init.d/led restart
```

Мигание синего светодиода при сетевой активности:
```sh
uci set system.@led[0].name=wwan-link
uci set system.@led[0].trigger=netdev
uci set system.@led[0].dev=wlan0
uci set system.@led[0].mode='link tx rx'
uci commit system
/etc/init.d/led restart
```


## Автоматизация
### Удалённое выполнения команд по SSH
Вы можете использовать ssh для удаленного выполнения команды переключения реле:

Включить реле на SSH-хосте `kankun`:
```sh
ssh kankun 'echo 1 > /sys/class/leds/tp-link:blue:relay/brightness'
```
Отключить реле на SSH-хосте `kankun`:
```sh
ssh kankun 'echo 0 > /sys/class/leds/tp-link:blue:relay/brightness'
```

Переключить реле на SSH-хосте `kankun`:
```sh
ssh kankun 'case "`cat /sys/class/leds/tp-link:blue:relay/brightness`" in 0) echo 1 > /sys/class/leds/tp-link:blue:relay/brightness;; 1) echo 0 > /sys/class/leds/tp-link:blue:relay/brightness;; esac'
````

Вы можете создать ярлык на рабочем столе для выполнения этой команды.


#### Linux: Ярлык запуска на рабочем столе
Создать файл ярлыка запуска `~/.local/share/applications/kankun-toggle.desktop`:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Toggle Outlet
Name[ru]=Переключть розетку
Icon=system-shutdown
Exec=ssh kankun 'case "`cat /sys/class/leds/tp-link:blue:relay/brightness`" in 0) echo 1 > /sys/class/leds/tp-link:blue:relay/brightness;; 1) echo 0 > /sys/class/leds/tp-link:blue:relay/brightness;; esac'
Comment=Toggle KanKun relay ON or OFF
Comment[ru]=Переключть розетку ВКЛЮЧЕНО или ОТКЛЮЧЕНО
Categories=Utility;Electronics;Internet;
Terminal=false
Actions=OutletON;OutletOFF;

[Desktop Action OutletON]
Name=Turn Outlet ON
Name[ru]=Включть розетку
Exec=ssh kankun 'echo 1 > /sys/class/leds/tp-link:blue:relay/brightness'

[Desktop Action OutletOFF]
Name=Turn Outlet OFF
Name[ru]=Отключть розетку
Exec=ssh kankun 'echo 0 > /sys/class/leds/tp-link:blue:relay/brightness'
```

Теперь в меню «Пуск» вы можете найти пункт «Переключить розетку» и нажать, чтобы переключить реле.

### Android: Используйте приложение Trigger для удалённого выполнения команд по SSH
Приложение [Trigger](https://f-droid.org/packages/com.example.trigger/) изначально было разработано для замков и дверей,
но его можно использовать для управления любым устройством по SSH.
Откройте приложение и отсканируйте этот QR-код:

![QR код для приложения Trigger чтобы добавить розетку Kankun](./trigger_qr_ssh.gif)

Вы можете изменить этот «замок» и изменить его IP-адрес и пароль SSH при необходимости.

### Установка REST API
Рекомендуется установить CGI-скрипт [kankun-json](https://github.com/homedash/kankun-json), который предоставляет API по протоколу HTTP(S).
Он также имеет небольшой веб-интерфейс, позволяющий управлять освещением из обозревателя.

![kankun-json web panel](https://camo.githubusercontent.com/0cf92e335e876977a02581f038ab4eb15758aae70519e2596c5bcded105c1cb3/68747470733a2f2f636c6475702e636f6d2f49575549416a7232704a2d3132303078313230302e706e67)

* https://github.com/homedash/kankun-manager — полный установщик и конфигуратор с Ansible.
* [Версия json.cgi для OpenWrt](https://blog.donbowman.ca/wp-content/uploads/2018/01/json.cgi_.txt)
* [Изменение IP-адреса выключателя в файле /www/switches.json при его изменении](https://gist.github.com/ferstar/6ebad5e70e17a9f4c05dabed7bf79d7b)

В Home Assistant есть [модуль](https://www.home-assistant.io/integrations/kankun/), который использует CGI-скрипт.
Но вы также можете использовать команду SSH для управления розеткой без установки чего-либо на устройство.

Существует также другая версия https://github.com/sean-/kankun. Она основана на `kankun-json`, но выглядит более старой.

https://github.com/CodeFoodPixels/kankun-setup Скрипт настройки CLI. Подключается к розетке по SSH,
настраивает её на работу в указанной сети Wi-Fi, копирует все файлы из папки setup, перезапускает розетку, а затем запускает файл `install.sh`.

После установки CGI-скрипта для REST API вы можете использовать его с тем же приложением [Trigger](https://f-droid.org/packages/com.example.trigger/),
а также с любым другим приложением, поддерживающим HTTP-запросы, например, [HTTP Request Shortcuts](https://f-droid.org/packages/ch.rmy.android.http_shortcuts/).

[Скрипт на Python для удаленного управления](https://drive.google.com/drive/u/2/folders/0B9JxR8qe_XORRWV0aHI5SXFYeTA)

https://github.com/metalx1000/Kankun-Smart-GUI — упрощённая версия `kankun-json`.

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


### Используя родной протокол

> [!WARNING]
> Это не рекомендуется да и может уже не работать.
> Please let us know if this works and improve the instructions.

You may try to control a Kankun Plug using the stock protocol, no hacks.
* [Kankun controller](https://github.com/0x00string/kankuncontroller) a Python app
* [Kankun plug gist for MacOS (OSX)](https://gist.github.com/oscarmorrison/6ebd9344e16448121ef4a5cdea1427b4) a Python script using native protocol


## Прошивание чистым OpenWrt

> [!WARNING]
> Делайте это только если вам это действительно нужно.

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

См. также:
* [kankun-firmware](https://github.com/andrewc12/kankun-firmware) и [buildenv and quilt_rev10.txt](https://gist.github.com/andrewc12/21f92b64feaa0ce0763ea0b5439448a8) Build firmware for Kankun small k (KK-SP3) **EXPERIMENTAL!**
* [Patch to enable the device support](https://gist.github.com/andrewc12/cb1ce8804629a2c6ce10a2b62bc4842a).


## Оригинальное руководство

<img width="1600" height="561" alt="Kankun KK-SP3 Manual" src="https://github.com/user-attachments/assets/b92f2c5e-1b76-421f-945f-6c9247b02217" />

Скопировано с [from Dropbox](https://www.dropbox.com/s/8sq4caf2iivcmmc/manual-english.png?dl=0)


## Статьи и обзоры
Эта статья основана на [удалённой странице в Вики OpenWrt](https://openwrt.org/toh/kankun/kk-sp3?rev=1621192123) и всех этих статьях:

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
  * Канал "How to Linux": 
    * [Finding IP of Kankun KK-SP3 WiFi smart plug in router](https://www.youtube.com/watch?v=Rc4PG0jxX8o)
    * [Webserver](https://www.youtube.com/watch?v=qpc3ZJiN-JQ)
    * [Commandline Hack](https://www.youtube.com/watch?v=yVysjg2lEqQ)
  * Канал Kris Occhipinti:
      1. [BusyBox](https://www.youtube.com/watch?v=-Mk7RP1tTzo&pp=0gcJCSgKAYcqIYzv)
      2. [HTTP Webserver](https://www.youtube.com/watch?v=D3P0gALPOvE)
      3. [Trouble Shooting Linux Tutorial](https://www.youtube.com/watch?v=C4MYbV8Xjc4)
      4. [Connect to Wi-Fi router SSH](https://www.youtube.com/watch?v=dOJdxb4aXjM)
      5. [Custom GUI](https://www.youtube.com/watch?v=spPLbki3Gvo)
  * [WidgetKK for SmartPlug](https://www.youtube.com/@ChopLabalagun/search?query=kankun)
  * [Обзор Kankun Smart Plug Socket Wi-Fi Умной интернет розетки](https://www.youtube.com/watch?v=_bRHiE1qKzg)


## Альтернативные розетки
* Orvibo S20 socket
  * [Reverse engineering Orvibo S20 socket](https://stikonas.eu/wordpress/2015/02/24/reverse-engineering-orvibo-s20-socket/)
  * https://github.com/fernadosilva/orvfms Web interface for the Orvibo S20 socket


## Журнал загрузки (boot log)
<details>
  <summary>Журнал заггрузки оригинальной прошивки от производителя (OpenWrt)</summary>

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


## Метки
ar71xx AR9330 4Flash 32RAM 0port 0nic ath9k 802.11bgn wall_plug

