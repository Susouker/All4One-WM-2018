# All4One WM 2018

## Überblick

Das *Gehirn* des Autos ist ein Raspberry Pi 3B+ (RP).
Der RP macht alle notwendigen Berechnungen und dient als WLAN Router. Falls notwendig kommuniziert der RP mit anderen Geräten im Auto.

Weitere Geräte, wie Fernbedienungen und Tablets sind über das WLAN mit dem RP verbunden und kommunizieren über TCP mit dem RP.

![Image](/Diagramm1.png)

## Protokolle

### TCP

Einzelne Nachrichten beginnen mit / sind getrennt durch ein '$' (ASCII: 36 oder 0x24).

Erstes Byte gibt den Typ der Nachricht an. Das Auto (Server) sendet Großbuchstaben und die anderen Geräte (Clients) senden Kleinbuchstaben.

| Identifier | Name          | Nutzung                              | Größe             | Format                          | Einheit |
| :---- | :----------------- | :----------------------------------- | :---------------  | :------------------------------ | :------ |
| A     | Angle              | Die Winkel der vier Räder            | 4xfloat - 16 byte | FR, FL, BR, BL                  | °       |
| T     | Throttle           | Die Motorleisungen der vier Räder    | 4xfloat - 16 byte | FR, FL, BR, BL                  | TBD     |
| R     | Rotation           | Die Rotation des Autos               | 2xfloat - 8  byte | Rechts-Links, Vorne-Hinten      | °       |
| V     | VGC                | Die Höhen der vier Zylinder          | 4xfloat - 16 byte | FR, FL, BR, BL                  | mm      |
| s     | einfache Lenkung   | Die Werte der Fernbedienung          | 2xfloat - 8  byte | Lenkwinkel, Gas                 | °/TBD   |
| c     | komplexe Lenkung   | Die Werte der Fernbedienung          | 3xfloat - 12 byte | Komplexe Lenkung (2), Ga        | °/TBD   |

#### Beispiele

RP sendet aktuelle Lenkwinkel und Motorleisungen:
```
     $A\xf7eu@\xc2w\x8a@\xb7\xb3\x83A\x0b\x99\x93A$TL\x0ev\xbfe\x14Z\xbf\x00\x00\x80\xbf\x99=e\xbf
HEX: 24 41 f7 65 75 40 c2 77 8a 40 b7 b3 83 41 0b 99 93 41 24 54 4c 0e 76 bf 65 14 5a bf 00 00 80 bf 99 3d 65 bf
```
Fernbedienung sendet Lenkwinkel und Gas in simplen Modus:
```
     $s\x00\x00\xdcAfff?
HEX: 24 73 00 00 dc 41 66 66 66 3f
```
