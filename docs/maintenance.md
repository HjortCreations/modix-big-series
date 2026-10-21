# Komponenter och ändringar

Ändra en sak på ett ställe. En recipe är en kombination, inte en ny kopia av all konfiguration.

| Ändring | Källa |
|---|---|
| Gemensamt utskriftsavslut | firmware/common/stop.g |
| Gemensam start/slutsekvens | slicer/gcode/ |
| Storlek eller Z-skruvgeometri | config/models/ |
| Slaglängd för ett visst exemplar | Lokal recipe utanför Git, via axis_max |
| Huvudets fria rörelse/probning | config/toolheads/; lokal nozzle_insets_mm vid behov |
| PID, BLTouch-offset, skevhet, shaper | Maskinens privata kalibrering; aldrig en huvudstandard |
| Stegmotormodell och TMC-parametrar | config/motors/ + firmware/motors/; aktivt val krävs |
| Hastighetsgräns / travelacceleration | config/motion/ |
| Tidsuppskattning i slicern | Samma motion-komponents slicer_time_estimates; ändrar inte firmware |
| Lager, väggar, infill, printacceleration | slicer/processes/ |
| Retraktion och munstycke | slicer/toolheads/ |
| Temperatur, flöde, fläkt, PA | slicer/materials/ |

Lokala overrides byggs med python tools/build.py --recipe FILE --output DIRECTORY.
Filvägarna ska ligga utanför Git eller under ignorerade local/. Dessa data följer med det lokala paketets manifest, inte in i repo/release.

Exemplet BIG-120Z+ULTRA återanvänder samma process, material och munstyckskomponent som BIG-Meter+ULTRA.
Gränserna hämtas från respektive vald motion-komponent. Exemplet måste driftsättas/provas separat.

BIG-60/120X/180X-varianter läggs till först när underlag finns för geometri, motorordning, homing och frigång.
Det finns inga påhittade fullkonfigurationer för dessa i repot.

Äldre oförändrade original, servicehistorik och övergivna kalibreringstester stannar i det tidigare privata arkivet.
Detta repo har en ny Git-historik utan dessa kunduppgifter. Det äldre repot raderas inte.
