# Domoticz-EspNowSerial-Plugin

Python plugin for EspNowSerial interface module

[English version and French version in the same document]
[Versions françaises et anglaises dans le même document]

## What's for? / CéKoi ?

* Maps EspNow (switches) devices to Domoticz devices, 1 switch per configured device

* Intègre des senseurs EspNow de type switch dans Domoticz

## Hardware prerequisites / Prérequis matériel

* You must have some sensors preconfigured with EspNow, as described at https://github.com/SmartNodeRules/Documentation/wiki/SampleESPNOW
* You must create a gateway on an ESP8266 device with ESPCoreRules EspNow protocol support, with baud settings to 115200
* You must then connect gateway module to any (physical or USB) serial port on machine running Domoticz (or map a serial local port to a remote one)

You'll find details in SmartNodeRules.md

* Vous devez avoir configuré des senseurs EspNow, comme décrit à https://github.com/SmartNodeRules/Documentation/wiki/SampleESPNOW
* Vous devez créer une passerelle sur un ESP8266 avec ESPCoreRules, avec le support du protocole EspNow, et une vitesse de 115200 bauds
* Vous devez connecter la passerelle au travers d'un lien série (physique ou USB) sur une machine tournant Domoticz (ou associer un port série local à un port distant)

Vous trouverez des détails dans le fichier SmartNodeRules.md

## Plugin Installation / Installation du plug-in

- Tested on Python version 3.7 & Domoticz version 2020.2
- Make sure that your Domoticz supports Python plugins (https://www.domoticz.com/wiki/Using_Python_plugins).


Follow these steps:

1. Clone repository into your Domoticz plugins folder.
```
cd domoticz/plugins
git clone https://github.com/FlyingDomotic/domoticz-espnowserial-plugin.git EspNowSerial
```
2. Restart Domoticz.
3. Make sure that "Accept new Hardware Devices" is enabled in Domoticz settings.
4. Go to "Hardware" page and add new item with type "EspNowSerial".
5. Select gateway serial port.
6. Define list of devices (see at bottom of this document).

- Testé avec Python version 3.7 & Domoticz version 2020.2
- Vérifiez que votre version de Domoticz supporte les plugins Python (https://www.domoticz.com/wiki/Using_Python_plugins).

Suivez ces étapes :

1. Clonez le dépôt GitHub dans le répertoire plugins de Domoticz.
```
cd domoticz/plugins
git clone https://github.com/FlyingDomotic/domoticz-espnowserial-plugin.git EspNowSerial
```
2. Redémarrer Domoticz.
3. Assurez-vous qu' "Acceptez les nouveaux dispositifs" est coché dans les paramètres de Domoticz.
4. Allez dans la page "Matériel" du bouton "configuration" et ajouter une entrée de type "EspNowSerial".
5. Sélectionnez le port série où la passerelle est connectée.
6. Définissez la liste des senseurs (voir à la fin de ce document).

## Plugin update / Mise à jour du plugin

1. Go to plugin folder and pull new version:
```
cd domoticz/plugins/EspNowSerial
git pull
```
2. Restart Domoticz.

Note: if you did any changes to plugin files and `git pull` command doesn't work for you anymore, you could stash all local changes using
```
git stash
```
or
```
git checkout <modified file>
```

1. Allez dans le répertoire du plugin et charger la nouvelle version :
```
cd domoticz/plugins/EspNowSerial
git pull
```
2. Relancez Domoticz.

Note : si vous avez fait des modifs dans les fichiers du plugin et que la commande `git pull` ne fonctionne pas, vous pouvez écraser les modifications locales avec la commande
```
git stash
```
ou
```
git checkout <fichier modifié>
```

## Plugin Configuration / Configuration du plug-in

| Field | Information|
| ----- | ---------- |
| Serial Port | Dropdown to select the Serial Port the gateway is plugged into |
| Device definitions | List of the devices you want to get into Domoticz (details here under)|
| Debug | Debug level. Will be more verbose when set to true |

| Zone | Information|
| ----- | ---------- |
| Serial Port | Liste déroulante pour sélectionner le port série de la passerelle |
| Device definitions | Liste des senseurs à intégrer dans Domoticz (détails ci-dessous) |
| Debug | Niveau de trace. Plus bavard si défini à True |


### Devices list / Liste des dispositifs

Device list is made by device definitions, separated by `|`. Device definition is made by EspNow device name followed by #2 for a switch or #8 for a PIR (in fact, Domoticz switch type can be used here). For example, `SW_1#2|PIR_1#8` defines `SW_1` EspNow device as a switch (#2) and `PIR_1` EspNow device as PIR (#8)

La liste des dispositifs est composée de définitions séparées par des `|`. Les définitions sont composées du nom du senseur EspNow, suivi de #2 pour un switch ou #8 pour un détecteur de mouvements (en fait, n'importe quel type de switch Domoticz peut être spécifié ici). Par exemple, `SW_1#2|PIR_1#8` definie `SW_1` le senseur EspNow comme un switch (#2) et le senseur `PIR_1` comme un détecteur de mouvement (#8)
