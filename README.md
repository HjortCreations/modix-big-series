# Modix BIG Series

Gemensamma RepRapFirmware-makron och PrusaSlicer-profiler för Modix BIG-serien.
**Griffin och Griffin ULTRA är oberoende av maskinstorleken.**

## Hämta och använd

Hämta ett färdigbyggt ZIP-paket från [Releases](https://github.com/HjortCreations/modix-big-series/releases).
Läs [installation](docs/installation.md) innan systemfiler läggs på en skrivare.
Paketet kompletterar en fungerande Modix-konfiguration; ingen ersättande `config.g` ingår.

| Paket | Geometri | Huvud / munstycke | Material / process |
|---|---|---|---|
| `big-120z-griffin-0.6` | BIG-120Z V4, 600×600×1200 | Griffin 0,6 mm | PLA, 0,2 mm lager |
| `big-meter-griffin-0.8` | BIG-Meter V4-referens, 980×1000×1000 | Griffin 0,8 mm | addnorth ePLA, 0,4 mm lager |
| `big-meter-ultra-1.8` | BIG-Meter äldre uppgraderad variant, 965×980×1000 | ULTRA 1,8 mm | FormFutura ePLA, 1,0 mm lager |

Måtten är etablerade arbetsvolymer, inte en garanti för alla exemplar av samma modell.
Källorna är migrerade och kontrolleras offline. **De nya sammansatta paketen är ännu inte installerade eller fysiskt provade.**
Fler BIG-storlekar läggs till när geometri och hårdvara finns verifierade. IDEX och annan Z-topologi ingår inte nu.

## Var finns inställningen?

| Del | Ansvar |
|---|---|
| `firmware/common/` | En U-rutin, ett stop.g, adaptiv mesh och axeltest |
| `config/models/` | Arbetsvolym och Z-skruvgeometri |
| `config/hardware/`, `firmware/hardware/` | Styrkort, ändstoppsriktning och befintlig homing |
| `config/motion/`, `config/motors/` | Rörelsegränser, tidsuppskattning och valbara motorparametrar |
| `config/toolheads/` | Huvudets frigång; ingen universell BLTouch-offset |
| `slicer/toolheads/` | Munstycke, retraktion och lagergränser |
| `slicer/processes/` | Lager, väggar, infill, hastigheter och printacceleration |
| `slicer/materials/` | Temperatur, kylning, flöde och PA för material/huvud/munstycke |
| `slicer/gcode/` | Vår gemensamma start-, slut- och lagerkod |
| `recipes/` | Små kombinationsfiler som väljer komponenter |

ULTRA-processen och materialet återanvänds utan kopior på en annan modell.
[Exemplet](examples/big-120z-ultra-1.8.json) visar sammansättningen och är inte en driftsatt maskinprofil.

## Gemensamt beteende

- Värm munstycket under homing. Full homing om Z är okänt, annars bara XY.
- Villkorlig G32: återanvänd lyckad riktning medan Z hålls och huvudet är oförändrat. `G32 S1` tvingar ny riktning.
- Proba adaptiv mesh för varje utskrift. U-vägen växlar riktning mellan passen.
- Behåll Modix avslut via M0 → stop.g: varm retraktion, kylning, sänk till minst Z300 med högst Z-max, parkera X1 Y1 och behåll Z-hållström.
- Startkoden styr acceleration, axelgränser och PA. Slicerns accelerationsöverstyrningar är noll.
- Byggplattevärmarna används inte. Samma tydliga filnamnsformat används överallt.

ULTRA 1,8 mm: **100 mm³/s, 235/215 °C, PA 0,035, print250/travel800**,
1,0/1,2 mm lager och retraktion 1,2 mm vid 35 mm/s. Detta är operatörens fungerande inställningar, inte uppmätt maxkapacitet.
G-code resolution behåller **0,0125 mm** i den migrerade baslinjen; förslaget 0,05 mm har inte införts automatiskt.

## Bygg och kontrollera

Kräver Python 3.10+; inga Python-paket behövs.

```console
python tools/check.py
python tools/build.py --all
```

Utdata hamnar i ignorerade dist/. ZIP-paketen innehåller ett manifest, systemfiler och två slicerformat:
PrusaSlicer.ini för **Import Config** samt PrusaSlicer-bundle.ini för **Import Config Bundle**.
Bundle-formatet delar namn på process/material mellan maskinstorlekarna.

[Underhållsregler](AGENTS.md) · [Komponenter och ändringar](docs/maintenance.md) · [Provningsstatus](docs/validation.md)
