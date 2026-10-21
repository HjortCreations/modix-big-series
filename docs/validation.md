# Provningsstatus

Komponenterna kommer från tidigare fungerande profiler och beställda makroändringar.
Ingen maskin styrs av verktygen i detta repo.

- Gemensam start/slut: samma kommandoföljd som tidigare; siffervärden väljs från komponenterna.
- U-kärna och stop.g: återanvända från senaste gemensamma källorna. Retraktionsvillkor, Z-max och X1Y1 bevaras.
- ULTRA 1,8 mm: operatören rapporterar fungerande 100 mm³/s, 235/215 °C och PA0,035. Detta är ingen uppmätt maximal materialkapacitet.
- Villkorlig U-tilt har tidigare provats fysiskt i en fyrmotorig installation. Det bevisar inte att varje ny kombination är driftsatt.
- Nya rena paket: byggda/kontrollerade offline. Inga systemfiler har laddats upp och ingen firmware har startats om under migreringen.
- Den nyligen införda enkla Y-max/X-min-passagen och senaste X1Y1-avslutet ska fortfarande observeras fysiskt i respektive installation.

## Reproducerbara kontroller

python tools/check.py kontrollerar sammansättning, gemensamma källor, integritet,
U-geometri vid olika prob-/axelgränser, positiv och begränsad Z-parkering, varm
retraktion, cachevillkor och att ULTRA-process/material återanvänds på olika storlekar.
GitHub Actions kör samma kontroll och bygger paketen.

Verklig slicerkontroll görs med PrusaSlicer 2.9.6:

```console
python tools/validate_slicer.py --slicer "/path/to/prusa-slicer-console.exe" --workdir "/path/outside/repo"
```

Den laddar genererad komplett INI, skivar en lokalt genererad modell och kontrollerar
start/slut, villkorlig homing, värmarbyten, accelerationskommandon och flödesgräns.
Den kontrollerar också att bundle-sektionerna bär samma inställningar och identiteter.
Rapporten sparas i arbetsmappen, inte som fler daterade dokument i repot.
Fysiska prov, ljud, temperaturmarginaler och utskriftskvalitet redovisas i privat servicejournal.
