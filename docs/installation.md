# Installation

Paketen är **överlägg**, inte universella fullständiga maskinkonfigurationer.
Behåll den fungerande Modix config.g, drivriktningar/strömmar, M584/M671-ordning,
G31, config_probe.g, PID-filer, värmar-/fläktkoppling och tillbehör.
Använd maskinens befintliga nätverk. Bygget har ingen kontakt med skrivaren.

1. Ta en lokal backup av SD/systemfiler och aktiva slicerinställningar. Förvara den utanför repot.
2. Välj rätt geometri, hårdvara och huvud. Kontrollera särskilt X/Y-ändstoppsriktning, fyra separata Z-drivrutiner och ordningen för M671-skruvarna.
3. Kontrollera huvudets frigång och probeoffset mot den faktiska maskinen. ULTRA:s 40 mm frontfrigång är ett beprövat startvärde från en installation, ingen universell offset. Automatisk Z-offset-puck ingår inte.
4. Granska paketets manifest.json. Installera dess sys/ tillsammans: bed.g, g32_u.g, adaptive_mesh.g, stop.g, axeltest och rätt fyra homingfiler. Höj inte drivrutinsström eller ändra kabelkoppling för att matcha ett modellnamn.
5. Paketets reference/config_model.g är en jämförelsefil. Kopiera inte dess M208/M671 över en redan kalibrerad maskin utan att ha verifierat geometri och motorordning.
6. Kontrollera M906:s vilofaktor och M84:s timeout i befintlig config. Referensinstallationerna använder 50 % efter 100 s. Stopprutinen håller Z aktivt; vald hållström måste kunna bära bädden.
7. Bekräfta systemfilerna genom återläsning och hash. G32 D1, adaptiv-mesh-anropets D1-läge och homingfilernas D1-läge visar planer utan rörelse.
8. Prova homing, G32, mesh och avslut under uppsikt med fri bädd. Det är ett separat fysiskt prov; ett lyckat bygge bevisar inte rörelser eller kabelkoppling.
9. Importera PrusaSlicer-bundle.ini med **File → Import → Import Config Bundle** och välj de tre matchande presetsen. Process/material har samma namn oavsett modell; skrivarpreseten har geometri/huvud i namnet. Alternativt kan hela PrusaSlicer.ini importeras med **Import Config**.
10. Koppla fysisk skrivare/IP lokalt i PrusaSlicer. Skiva om gamla jobb: äldre G-code innehåller fortfarande sin gamla start- och slutkod.

Full/Z-homing rensar giltig tilt, XY-homing behåller den. Om Z släpps blir positionen okänd och nästa start homar/riktar igen. Efter mekaniskt ingrepp: kör G32 S1.
Firmwareomstart tappar tillståndet. Villkoret kan inte upptäcka att någon manuellt har flyttat bäddens skruvar.

Griffin-referensens Y-min-homing behåller sin äldre dubbla passage. Y-max-varianten behåller en enda passage enligt den senaste källan. Homing förenhetligas inte genom att kopiera en annan maskins riktningar.
ULTRA:s normala temperaturbyte efter första lagret är gemensamt i paketet; även Griffin-profilerna får detta uttryckliga byte till sin inställda normaltemperatur. Start-/slutsekvensen är i övrigt densamma.
