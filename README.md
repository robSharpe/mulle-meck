# Mulle Meck Bygger Bilar – lokal & online

En webbaserad kopia av *Mulle Meck Bygger Bilar* (eng. *Gary Gadget: Build a
Car*), byggd i Phaser 2.8.8. Spelet är en helt statisk sajt som kan köras både
lokalt och publiceras via GitHub Pages.

> ⚠️ Grafik och ljud är upphovsrättsskyddat av originalets rättighetsinnehavare.
> Det här är en privat fan-kopia; använd ansvarsfullt.

## 🎮 Spela online

**▶️ https://robsharpe.github.io/mulle-meck/**

Sajten uppdateras automatiskt vid varje push till `main`.

## 💻 Spela lokalt på Mac

Dubbelklicka på **`starta_mulle.command`** – den startar en lokal webbserver och
öppnar spelet i webbläsaren. Stäng terminalfönstret för att stoppa servern.

Eller manuellt:

```sh
python3 server.py
# öppna sedan http://localhost:8000
```

## 📁 Innehåll

| Fil / mapp | Roll |
|------------|------|
| `mulle-meck-lokal/` | Själva spelet (det som publiceras till Pages). |
| `server.py` | Lokal trådad webbserver för spel på `localhost:8000`. |
| `starta_mulle.command` | Startknapp för macOS. |
| `SPELGUIDE.md` | Komplett guide: spelloop, menyer, kartor, sparande m.m. |
| `.github/workflows/deploy-pages.yml` | Publicerar `mulle-meck-lokal/` till GitHub Pages. |

## 📖 Hur spelet fungerar

Se [SPELGUIDE.md](SPELGUIDE.md) för en genomgång av spelet – hur man bygger bilar,
kör i världen, vad menyerna gör och hur framsteg sparas.

## 🔧 Teknik

- Phaser 2.8.8, ren statisk sajt (inga byggsteg, inget serverside).
- Endast relativa sökvägar – fungerar både på `localhost` och under en
  Pages-underadress.
- Offline-läge: nätverks-multiplayer avstängt.
