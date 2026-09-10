# Rührwerk

**Live: https://jaayy46.github.io/ruehrwerk/**
Beispielrezept: https://jaayy46.github.io/ruehrwerk/rezepte/kuerbissuppe.html

Eigenes Thermomix-Kochbuch mit Schritt-für-Schritt-Kochmodus. Eine Datei, kein Server,
keine Anmeldung. Läuft auf iPad, iPhone, Android, Desktop.

## Warum nicht Cookidoo

Cookidoo kann eigene Rezepte speichern und auf den TM6/TM7 syncen — aber nur als Text.
**Guided Cooking** (automatische Zeit/Temperatur/Stufe) kann ausschliesslich Vorwerk erzeugen;
es gibt keine öffentliche Schnittstelle, um eigene Rezepte dorthin zu bringen.
Rührwerk baut die Schritt-für-Schritt-Führung deshalb selbst nach — auf dem Tablet neben dem Gerät.

## Starten

Am schnellsten: https://jaayy46.github.io/ruehrwerk/ öffnen.
Auf dem iPad in Safari → Teilen → **Zum Home-Bildschirm**, danach läuft es als eigene App, auch offline.

Lokal:

```bash
python3 serve.py
```

Dann `http://localhost:8777` öffnen. Auf iPad/iPhone: Safari → Teilen → **Zum Home-Bildschirm**.
Danach läuft es als eigene App, auch offline.

Veröffentlicht liegt es in `Jaayy46/ruehrwerk`, Pages auf `main / root`.
Für den Publish-Dialog: Repo `Jaayy46/ruehrwerk`, Branch `main`, Ordner `rezepte`.
HTTPS ist Pflicht, sonst kein Offline-Betrieb und kein Wach-halten des Displays.

## Funktionen

**Bibliothek** — Suche, Schlagwörter, Favoriten. Alles liegt im `localStorage` des Geräts.

**Editor** — Zutaten (Menge / Einheit / Name) und Schritte mit Thermomix-Parametern:
Zeit, Temperatur, Stufe, Linkslauf, Zubehör.

**Kochmodus** — Vollbild, dunkel, ein Schritt pro Seite:
- Anweisung gross, Parameter als Kacheln daneben
- Zutaten des Schritts werden automatisch eingeblendet (Namensabgleich)
- Timer aus der Schrittzeit, mit Signalton und Vibration
- Display bleibt an (Wake Lock)
- Wischen, Pfeiltasten, Leertaste = Timer, Esc = raus
- Portionen live umrechnen, alle Mengen skalieren mit

**Import**
- *Von Website* — liest schema.org-Rezeptdaten über einen öffentlichen Lese-Dienst
  (`r.jina.ai`, Fallbacks AllOrigins/CodeTabs). Die URL verlässt dabei das Gerät.
  Fällt auf Fliesstext-Parsing zurück, wenn keine strukturierten Daten da sind.
- *Text einfügen* — Rezept reinkopieren. Zeilen mit Menge werden Zutaten, der Rest Schritte.
  Funktioniert immer, auch hinter Paywall/Login.
- *JSON-Datei* — vorher exportiertes Backup zurückspielen.

**Thermomix-Notation** wird beim Import erkannt und aus dem Anweisungstext herausgelöst:

| Eingabe | Ergebnis |
|---|---|
| `10 Sek./Stufe 4` | Zeit 10 Sek., Stufe 4 |
| `15 Min./100°C/Stufe 2/Linkslauf` | + Temperatur 100 °C, Linkslauf |
| `4 Min./Varoma/Stufe 2` | Temperatur Varoma |
| `2 Min./Teigstufe` | Stufe Teigstufe |
| `8 Sek./Stufe 4-6` | Stufenbereich |

Erkannt wird nur, was als `/`-Block geschrieben ist — Fliesstext wie
„Rührstab nicht verwenden" bleibt unangetastet.

## Cookidoo — Link-Import

Cookidoos Link-Import liest **schema.org-Rezeptdaten** aus dem Quelltext einer öffentlich
erreichbaren Seite. Rührwerk erzeugt dafür pro Rezept eine eigene statische HTML-Seite:
JSON-LD `@type: Recipe` plus Microdata, mit Zutaten, Schritten und der kompletten
Thermomix-Notation im Schritttext. Kein JavaScript nötig — Importer führen keines aus.

Knopf **Link** auf der Rezeptkarte:

1. GitHub-Repo eintragen (`benutzer/rezepte`), Ordner, optional eigene Pages-Domain.
2. Entweder **HTML herunterladen** und selbst ins Repo legen, oder mit einem
   Fine-grained Token (nur dieses Repo, *Contents: Read and write*) **direkt veröffentlichen**.
   Der Token bleibt im Browser des Geräts und geht nur an `api.github.com`.
3. **Live prüfen** holt die veröffentlichte Seite zurück und liest sie mit demselben Parser,
   den auch Importer verwenden — zeigt Titel, Anzahl Zutaten und Schritte.
4. **URL kopieren** → in Cookidoo einfügen.

GitHub Pages braucht nach dem Push 20–60 Sekunden. `localhost` funktioniert nicht,
Cookidoo muss die Seite von aussen abrufen können. Ob Cookidoo beliebige Domains
akzeptiert oder nur bekannte Rezeptseiten, hängt an Vorwerk — falls der Import eine URL
ablehnt, bleibt der Cookidoo-Text zum Abtippen.

Auch nach dem Import gilt: eigene Rezepte sind in Cookidoo **Text**, kein Guided Cooking.

## TM7-Einstellungen

Pro Schritt einstellbar: **Modus**, Zeit, Temperatur, Stufe, Linkslauf, Kerntemperatur, Zubehör.

Hinterlegte Modi mit dokumentierten Bereichen:

| Modus | Bereich |
|---|---|
| Manuell | 37–120 °C, Sanftrührstufe–10, Turbo, Teigstufe |
| Anbraten | bis 160 °C, leicht oder intensiv |
| Offenes Kochen | bis 100 °C, Messer steht |
| Dampfgaren | Varoma-Aufsatz / Garkörbchen |
| Sous-vide | 37–85 °C |
| Slow Cooking | 37–98 °C, 1–8 Std., max. 800 g |
| Fermentieren | 37–70 °C, bis 12 Std. |
| Erwärmen | bis 90 °C, Sanftrühren bis Stufe 2 |
| Wasser erhitzen | 37–100 °C |
| Vorspülen | 1000 g Wasser; 37 / 55 / 75 / 105 °C |
| Peeler | 600 g Wasser, max. 800 g, ca. 4 Min. |

Dazu Eier kochen, Reis kochen, Andicken, Karamellisieren, Teig kneten, Turbo, Pürieren,
Emulgieren, Kerntemperatur, Reiben/Schneiden, Spiralschneider, Wiegen.

Der Editor **warnt**, blockiert aber nie:

- Temperatur ausserhalb des Modus-Bereichs
- Zeit ausserhalb des Modus-Bereichs
- Heizen ab Stufe 6,5 (der Thermomix heizt dort nicht)
- Deckel öffnen über Stufe 2
- über 120 °C ausserhalb von Anbraten/Karamellisieren

Werte in den Auswahllisten sind Vorschläge; freie Eingabe bleibt jederzeit möglich.
Quellen: Vorwerk FAQ TM7, Vorwerk-Funktionsübersicht, öffentliche Modi-Übersichten —
im Zweifel gilt die Gebrauchsanleitung deines Geräts.

## Cookidoo-Text zum Abtippen

Knopf **Cookidoo** auf jeder Rezeptkarte (oder im Editor) erzeugt den fertigen Text zum
Hineinkopieren in `cookidoo.de → Eigene Rezepte → Rezept erstellen`:
Kopfdaten, Zutaten zeilenweise, Schritte einzeln nummeriert — mit korrekt
zusammengesetzter Vorwerk-Notation, z. B.

```
4. Gemüsebrühe, Salz und Muskat zugeben, garen, 20 Min./100°C/Linkslauf/Stufe 1.
```

Grenzen, damit nichts überrascht:

- Cookidoo hat **keine** Import-Schnittstelle. Kein API, kein Dateiformat, kein Upload.
  Das Formular ist der einzige Weg, auch beim TM7.
- Eigene Rezepte erscheinen dort als **Text**. **Kein Guided Cooking** — der Thermomix
  stellt Zeit, Temperatur und Stufe nicht selbst ein, egal wie das Rezept formatiert ist.
  Diese Rezepte kann ausschliesslich Vorwerk erzeugen.
- Wer echte Schritt-für-Schritt-Führung will, nimmt den Kochmodus dieser App.

## Sicherheit

Importierte Rezepte sind fremder Inhalt. Deshalb:

**Eingangskontrolle.** Alles aus Netz, Zwischenablage oder JSON-Datei läuft durch
`sanitizeRecipe()`: nur bekannte Felder, feste Typen, harte Längen, Modi und Zubehör
nur aus der erlaubten Liste. Unbekannte Schlüssel — `__proto__` eingeschlossen — fallen
weg. Gilt auch beim Lesen aus dem `localStorage`.

**Ausgabe.** Jede Rezeptangabe wird escaped, Attribute sind durchgehend quotiert.
Gefetchte Fremdseiten werden nur mit `DOMParser` gelesen, nie als `innerHTML` gesetzt —
dabei werden Tags zusätzlich entfernt. Im JSON-LD der veröffentlichten Seite ist `<` als
`\u003c` kodiert, ein `</script>` im Rezepttitel kann den Block nicht sprengen.

**URLs.** Bild- und Quell-Adressen laufen durch `safeUrl()`: nur `https:`, `http:` oder
`data:image/*`. `javascript:` und Konsorten werden verworfen. Externe Links bekommen
`rel="nofollow noopener noreferrer ugc"`.

**Seitenrichtlinie (CSP).** Die App erlaubt Netzverbindungen ausschliesslich zu
`r.jina.ai`, `api.allorigins.win`, `api.codetabs.com` und `api.github.com`. Keine fremden
Skripte, keine externen Bilder, kein Einbetten. Selbst wenn doch einmal Code durchkäme,
gäbe es kein Ziel, an das er etwas senden könnte. Die veröffentlichte Rezeptseite fährt
`default-src 'none'` — dort läuft **überhaupt kein** JavaScript.

**GitHub-Token.** Getrennt von der übrigen Konfiguration gespeichert und standardmässig
nur im Arbeitsspeicher: Tab zu, Token weg. Dauerhaft speichern ist ein bewusster Haken,
daneben liegt „Token löschen". Er geht ausschliesslich als `Authorization`-Header an
`api.github.com`, nie in eine URL, und ist nie Teil des Rezept-Exports.
Empfehlung: Fine-grained Token, nur dieses eine Repo, *Contents: Read and write*,
mit Ablaufdatum.

**Repo-Pfad.** Ordnerangaben werden auf `[A-Za-z0-9._-]` reduziert, `..` entfernt,
maximal vier Ebenen — kein Schreiben ausserhalb des vorgesehenen Ordners.

**Service Worker.** Cacht nur eigene Dateien und exakt `fonts.googleapis.com` /
`fonts.gstatic.com`. Import- und API-Verkehr wird nie zwischengespeichert.

Geprüft mit einem Payload (`"><img onerror=…><svg/onload=…>`, `javascript:`-Bild,
`__proto__`, `</script>`-Ausbruch) über den Import bis in Bibliothek, Editor, Kochmodus
und veröffentlichte Seite: keine Ausführung, keine Prototype-Verschmutzung, Bild verworfen,
JSON-LD intakt. Ein Test-`fetch` auf eine fremde Domain wurde von der CSP blockiert.

**Was bleibt:** die Import-URLs sind für `r.jina.ai` sichtbar, und wer physischen Zugriff
auf dein entsperrtes Gerät hat, kommt an einen gespeicherten Token. Beides ist eine
Abwägung, keine Lücke.

## Backup

Pfeil-nach-oben-Knopf oben rechts exportiert alle Rezepte als JSON.
Der Speicher hängt am Browser: Website-Daten löschen löscht auch die Rezepte. Also exportieren.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | komplette App (Markup, Stil, Logik) |
| `sw.js` | Service Worker, Offline-Cache. HTML netzwerk-zuerst, Rest cache-zuerst |
| `manifest.webmanifest` | Home-Screen-Installation |
| `icon.svg` | App-Icon |
| `serve.py` | lokaler Server |

Nach Änderungen an `index.html` die `VERSION` in `sw.js` hochzählen, sonst sehen
installierte Geräte unter Umständen die alte Fassung.
