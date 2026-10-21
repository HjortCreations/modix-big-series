# Underhållsregler

- Detta repo innehåller återanvändbara komponenter. Kundnamn, adresser, IP/MAC, kortets UID, CRM-id, lösenord, nätverk och serviceanteckningar hör till privata lokala servicejournaler utanför repot.
- Ändra rätt komponent i stället för att lägga till en maskinkopia. Modellgeometri får inte finnas i huvud-, material- eller processprofiler. Material/process får inte ha modellnamn.
- firmware/common/stop.g, firmware/common/g32_u.g och slicer/gcode/ är de enda källorna för respektive gemensam rutin. Ändra aldrig genererade kopior manuellt.
- config_probe.g, PID-filer, M556, input shaper, nätverk och enskilda kalibreringar får inte versionshanteras. Bevara maskinens fungerande config och lokala backup.
- Nya rörelsegränser, temperaturer eller algoritmer kräver en separat avsiktlig ändring. En städning får inte presenteras som fysisk provning.
- En recipe väljer modell, geometri, hårdvara, huvud/munstycke, process, material och motion. Ange faktiskt provningsläge. Anta inte att modellnamn bestämmer kabelkoppling, homingriktning eller probeoffset.
- Valfri motortuning laddas aldrig automatiskt. Ange antaganden och återställningsparametrar.
- Kör python tools/check.py och bygg alla paket. Vid slicerändring, gör dessutom verklig CLI-slicing med PrusaSlicer enligt docs/validation.md. Kontrollera start/slut, temperaturer, gränser och flöde.
- Uppdatera befintliga korta dokument på plats. Inga daterade serviceberättelser, screenshots, loggmappar, övergivna testprofiler eller alternativa final/v2-filer här.
- dist/, lokala profiler och granskningsloggar är ignorerade. Release-paket byggs från en angiven commit; inga hemligheter får finnas i Git-historiken.
- Installera eller kör inget på en skrivare som en bieffekt av ett bygge eller test. Användarens uppdrag och aktuella maskintillstånd styr separat driftsättning.
