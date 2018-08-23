# All4One WM 2018

## Überblick

Das *Gehirn* des Autos ist ein Raspberry Pi (RP).
Der RP macht alle notwendigen Berechnungen und dient als WLAN Router. Falls notwendig kommuniziert der RP mit anderen Geräten im Auto.

Weitere Geräte, wie Fernbedienungen und Tablets sind über das WLAN mit dem RP verbunden und kommunizieren über TCP mit dem RP.

![Image](/Diagramm1.png)

## Protokolle

### TCP

Das erste Byte gibt den Typ der Nachricht an (packetID). Jede packetID hat eine eindeutige Länge, sodass klar ist, wo die nächste Nachricht anfängt.

Das Auto (Server) sendet Großbuchstaben und die anderen Geräte (Clients) senden Kleinbuchstaben.

| Identifier | Name          | Nutzung                              | Größe             | Format                          | Einheit |
| :---- | :----------------- | :----------------------------------- | :---------------  | :------------------------------ | :------ |
| A     | Angle              | Die Winkel der vier Räder            | 4xfloat - 16 byte | FR, FL, BR, BL                  | rad     |
| T     | Throttle           | Die Motorleisungen der vier Räder    | 4xfloat - 16 byte | FR, FL, BR, BL                  | TBD     |
| R     | Rotation           | Die Rotation des Autos               | 2xfloat - 8  byte | Rechts-Links, Vorne-Hinten      | rad     |
| V     | VGC                | Die Höhen der vier Zylinder          | 4xfloat - 16 byte | FR, FL, BR, BL                  | mm      |
| s     | einfache Lenkung   | Die Werte der Fernbedienung          | 2xfloat - 8  byte | Lenkwinkel, Gas                 | rad/TBD |
| c     | komplexe Lenkung   | Die Werte der Fernbedienung          | 3xfloat - 12 byte | Komplexe Lenkung (2), Gas       | rad/TBD |
| b     | Tow-Bar            | Die Position der Tow-Bar             | 1xfloat - 4 byte  | Position                        | 0-1     |
| t     | Optionen Toggle    | z.B. An- und Ausschalten des Buzzers | 2xbyte  - 2  byte | Identifier, Wert                | -       |
| v     | VGC Mode           |                                      | 1xbyte  - 1  byte | Wert                            | -       |
| d     | Routinen           | Automatisierte Abfolge von Kommandos | 1xbyte  - 1  byte | Wert                            | -       |

#### Optionen

| Identifier | Name   | Format                        |
| :---- | :---------- | :---------------------------- |
| L     | Licht       | 0: aus; 1: an; 2: automatisch |
| B     | Buzzer      | 0: aus; 1: an; 2: automatisch |

#### VGC Mode

| Wert  | Name         | Beschreibung                                       |
| :---- | :----------- | :------------------------------------------------- |
| F     | Flat         | Alle Magnete aus -> ganz unten                     |
| A     | Articulation | Keine Ahnung was, das wird sich noch herausstellen |
| 0     |              | vielleicht noch mehr vielleicht auch nicht         |

#### Routinen

| Wert  | Name         | Beschreibung                                                                                                   |
| :---- | :----------- | :------------------------------------------------------------------------------------------------------------- |
| D     | Demo         | Einmal alle Räder von rechts nach links lenken. Jeden VGC Zylinder nach oben und unten und Lichter an aus etc. |
| T     |              | vielleicht noch mehr vielleicht auch nicht         |

#### Beispiele

RP sendet aktuelle Lenkwinkel und Motorleisungen:
```
Werte: A (3.834348440170288, 4.327118873596191, 16.462751388549805, 18.44972801208496) T (-0.9611556529998779, -0.8518736958503723, -1.0, -0.8954711556434631)
       A\xf7eu@\xc2w\x8a@\xb7\xb3\x83A\x0b\x99\x93ATL\x0ev\xbfe\x14Z\xbf\x00\x00\x80\xbf\x99=e\xbf
HEX:   41 f7 65 75 40 c2 77 8a 40 b7 b3 83 41 0b 99 93 41 54 4c 0e 76 bf 65 14 5a bf 00 00 80 bf 99 3d 65 bf
```
Fernbedienung sendet Lenkwinkel und Gas in simplen Modus:
```
Werte: s (27.5, 0.9)
       s\x00\x00\xdcAfff?
HEX:   73 00 00 dc 41 66 66 66 3f
```

## ToDo

#### Android App

- [ ] Verbindungsstatusicon
- [ ] IP und Port in Settings
- [ ] VGC-Mode-Auswahl-Knöpfe

#### RPi Python

- [ ] "Routinen" (sowas wie einmal Lenkung von ganz rechts nach ganz links oder einen kleinen Tanz etc.)
- [ ] Steuerung des Autos
