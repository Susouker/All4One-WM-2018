# All4One WM 2018

## Überblick

Das *Gehirn* des Autos ist ein Raspberry Pi (RP).
Der RP macht alle notwendigen Berechnungen und dient als WLAN Router. Falls notwendig kommuniziert der RP mit anderen Geräten im Auto.

Weitere Geräte, wie Fernbedienungen und Tablets sind über das WLAN mit dem RP verbunden und kommunizieren über TCP mit dem RP.

![Image](/Diagramm1.png)

## Protokolle

### TCP

Das erste Byte gibt den Typ der Nachricht an (packetID). Zu jeder packetID gibt es eine eindeutige Länge, sodass eindeutig ist, wo die nächste Nachricht anfängt.

Das Auto (Server) sendet Großbuchstaben und die anderen Geräte (Clients) senden Kleinbuchstaben.

| Identifier | Name          | Nutzung                              | Größe             | Format                          | Einheit    |
| :---- | :----------------- | :----------------------------------- | :---------------  | :------------------------------ | :--------- |
| A     | Angle              | Die Winkel der vier Räder            | 4xfloat - 16 byte | FR, FL, BR, BL                  | rad        |
| T     | Throttle           | Die Motorleisungen der vier Räder    | 4xfloat - 16 byte | FR, FL, BR, BL                  | TBD        |
| R     | Rotation           | Die Rotation des Autos               | 2xfloat -  8 byte | Rechts-Links, Vorne-Hinten      | rad        |
| V     | VGC                | Die Höhen der vier VGC Achsen        | 4xint   -  8 byte | FR, FL, BR, BL                  | 0-1        |
| s     | einfache Lenkung   | Die Werte der Fernbedienung          | 2xfloat -  8 byte | Lenkwinkel, Gas                 | rad/TBD    |
| c     | komplexe Lenkung   | Die Werte der Fernbedienung          | 3xfloat - 12 byte | Komplexe Lenkung (2), Gas       | rad/mm/TBD |
| b     | Tow-Bar            | Die Position der Tow-Bar             | 1xfloat -  4 byte | Position                        | 0-1        |
| t     | Optionen Toggle    | z.B. An- und Ausschalten des Buzzers | 2xbyte  -  2 byte | Identifier, Wert                | -          |
| v     | VGC Mode           |                                      | 1xbyte  -  1 byte | Wert                            | -          |
| d     | Routinen           | Automatisierte Abfolge von Kommandos | 1xbyte  -  1 byte | Wert                            | -          |

#### Optionen

| Identifier | Name   | Format                        |
| :---- | :---------- | :---------------------------- |
| L     | Licht       | 0: aus; 1: an; 2: automatisch |
| B     | Buzzer      | 0: aus; 1: an; 2: automatisch |

#### VGC Mode

| Wert  | Name         | Beschreibung                                       |
| :---- | :----------- | :------------------------------------------------- |
| F     | Unten        | geringster Schwerpunkt                             |
| P     | Oben         | höchster Bodenabstand                              |
| A     | Articulation | Keine Ahnung was, das wird sich noch herausstellen |
| 0     |              | vielleicht noch mehr vielleicht auch nicht         |

#### Routinen

| Wert  | Name         | Beschreibung                                                                                                   |
| :---- | :----------- | :------------------------------------------------------------------------------------------------------------- |
| D     | Demo         | Einmal alle Räder von rechts nach links lenken. VGC nach oben und unten und Lichter an aus etc. |
| 0     |              | vielleicht noch mehr vielleicht auch nicht         |

### I2C oder SPI zwischen RPi und Arduino Slaves

Nach einem Identifier Byte kommt ein Byte mit dem Wert. Wenn es eine Option vier mal gibt (FR,FL,BR,BL) geben die letzten beiden Bits vorne-hinten und rechts-links an.

| Identifier | Name          | Format                  |
| :------- | :-------------- | :---------------------- |
| `Arduino 0` |
| 001000xx | Lenkung         | -1rad - 1rad            |
| 001100xx | VGC             | Räder unten - oben      |
| 00111yxx | VGC min/max adj | y: min/max, x: welches Rad, folgendes Byte: signed 8 bit int  |
| 00101000 | VGC min/max save | folgendes Byte wird gelesen und ignoriert  |
| `Arduino 1` |
| 01100000 | TowBar Position | Rechts - Links          |
| 011100xx | Throttle        | Rückwärts - Vorwärts    |


## ToDo

#### Android App

#### RPi Python

- [ ] angleLimit CS
