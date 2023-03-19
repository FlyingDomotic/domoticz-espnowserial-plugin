# Configuring ESPcoreRules / Configurer ESPcoreRules

## Configure EspNow on gateway / Configurer EspNow sur la passerelle

Install https://github.com/SmartNodeRules/ESPCoreRules following information at https://github.com/SmartNodeRules/Documentation/wiki/SampleESPNOW

Installer https://github.com/SmartNodeRules/ESPCoreRules selon les infos à https://github.com/SmartNodeRules/Documentation/wiki/SampleESPNOW

Load ESPcoreRules.ino into Arduino IDE

Avec l'IDE Arduino, charger ESPcoreRules.ino

Define CPU type to your ESP type and flash it, fully clearing flash

Définir le type de CPU selon votre ESP et flasher le module en effaçant toute la flash

On Arduino IDE console, enter `wificonnect ssid/pwd`, check we got an IP using settings`

Sur le port console de l'IDE Arduino (115200), entrer `wificonnect ssid/pwd`, vérifier qu'on a une @ip par "settings"

Get IP value and connect with a browser to load the following boot file:

Récupérer l'IP, et se connecter avec un browser pour charger le fichier boot suivant :
```
on System#Config do
  Config,AutoConnect,0
  Config,AutoAPOnFailure,0
  ESPNowConfig ad562bc940cafe3d,ad562bc940cafe3d,36:33:33:33:33:33,Receiver
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:01,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:02,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:03,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:04,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:05,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:06,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:07,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:08,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:09,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:0A,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:0B,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:0C,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:0D,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:0E,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:0F,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:10,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:11,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:12,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:13,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:14,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:15,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:16,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:17,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:18,1
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:19,1
Endon
```

It'll allow 19 sensors and a gateway.

Il autorise 19 senseurs et une paserelle

## Configure EspNow on sensors / Configurer EspNow sur les senserus

On Arduino IDE, set `ESP8266 generic` as CPU type, set the right serial/USB adaptor COM port , set flash mode to `DOUT`, flash size to `2 MB, 128K SPISSF`

Sur l'IDE Arduino , mettre le bon CPU (ESP8266 generic), le port COM de l'adapteur série/USB), flash mode DOUT, 2 MB flash, 128K SPISSF

Load code on TYW3S

Charger le code dans le TYWE3S

On Arduino IDE console, enter `wificonnect ssid/pwd`, check we got an IP using settings`

Sur le port console de l'IDE Arduino (115200), entrer `wificonnect ssid/pwd`, vérifier qu'on a une @ip par "settings"

Get IP value and connect with a browser to load the following boot file:

Récupérer l'IP, et se connecter avec un browser pour charger le fichier boot suivant :

Load the following code into boot file

Charger le code suivant dans le fichier de boot

```
on System#Config do
  Config,Name,xx_xx
  TuyaCheck
  Config,WifiSSID,<ssid>
  Config,WifiKey,<pwd>
  Config,WifiAPKey,<AP key>
  Config,Group,MyGroup
  Config,Port,65501
  Config,Time,0
  Config,DST,0
  Config,MSGBus,UDP,0
  Config,Timezone,120
  Config,Baudrate,9600
  Config,Rules,Clock,0
Endon
```
Load the following code into rules file

Charger le code suivant dans le fichier "rules"

```
on TUYA#Event do
  ESPNowConfig ad562bc940cafe3d,ad562bc940cafe3d,36:33:33:33:33:xx,Sender
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:33,0
  ESPNowSend %sysname%/Event=%eventvalue%
endon
on TUYA#BatteryLow do
  ESPNowConfig ad562bc940cafe3d,ad562bc940cafe3d,36:33:33:33:33:xx,Sender
  ESPNowAddPeer ad562bc940cafe3d,36:33:33:33:33:33,0
  ESPNowSend %sysname%/BatteryLow=%eventvalue%
endon
```

## Loading a new firmware version / Chargement d'une nouvelle version de firmware

For gateway, connect module on PC through USB port and load firmware

Pour la passerelle, la connecter sur le PC et recharger le code depuis le port USB.

For modules, switch them to WiFi (push reset button for at least 5 secs, enter `wificonnect ssid/pwd`, check we got an IP address with `settings`, get it), connect with a browser and use `Tools > Firmware` to select and load new firmware

Pour les modules, les passer en mode Wifi (appui sur le bouton reset pendant au moins 5 secondes), passer les commandes `wificonnect ssid/pwd`, vérifier qu'on a une @ip par `settings`, récupérer l'IP, et se connecter avec un browser pour utiliser le menu `Tools > Firmware`pour sélectionner et charger le nouveau firmware

