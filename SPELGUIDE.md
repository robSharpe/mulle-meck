# Spelguide – Mulle Meck Bygger Bilar (lokal kopia)

En komplett genomgång av hur spelet fungerar, för dig som vill veta vad allt gör.
Ingen förkunskap behövs.

---

## Vad är det här?

En webbaserad version av **Mulle Meck Bygger Bilar** (engelska: *Gary Gadget:
Build a Car*) – klassikern där du hjälper Mulle att bygga ihop bilar av
skrotdelar och köra ut i världen. Spelet är byggt i spelmotorn Phaser och körs
helt **lokalt på din dator**: en liten webbserver (`server.py`) serverar spelet
i webbläsaren. Allt sker offline – det fanns ett multiplayer-läge i originalet,
men det är avstängt här.

**Starta spelet:** dubbelklicka på `starta_mulle.command`. Då startas servern och
webbläsaren öppnas på `http://localhost:8000`. Stäng terminalfönstret för att
stoppa servern.

---

## Så fungerar spelet (spelloopen)

Spelet är uppdelat i *scener*. Du rör dig mellan dem ungefär så här:

```
Meny  →  Garaget  →  Gården  →  Världen  →  Karaktärer & uppdrag
            ↑___________ Skroten ___________↓
```

| Scen | Vad du gör |
|------|------------|
| **Menyn** | Skriv ditt namn för en **ny profil**, eller klicka på ett **befintligt namn** för att fortsätta ett sparat spel. |
| **Garaget** | Mulles verkstad. Här **bygger du bilen** av delar. Mulle säger till om något fattas. |
| **Skroten** | Skrothögen där du **plockar delar** som hamnar i din delsamling. |
| **Gården** | Utanför garaget – här **kör du ut** den färdiga bilen. |
| **Världen** | En karta du **kör runt på** för att hitta platser och uppdrag. |
| **Karaktärer** | Personer och platser du når genom att köra dit: Figge Ferrum, Sture Stortand, Doris Digital, Ludde Labb, Viola, Saftfabriken, Bilshowen m.fl. |

### Att bygga en bil

I garaget sätter du ihop bilen del för del. Mulle kommenterar vad som saknas –
i spelets repliker hör du honom efterlysa bland annat:

- **Motor** ("liksom själva motorn fattas")
- **Hjul** ("Inga hjul, inge kul")
- **Batteri** ("Batteriet som ska ge ström, var är det?")
- **Bensin/tank** ("Soppa saknas! Tanken är inte bara tom – den finns inte ens!")
- **Växellåda** ("här fattas ju växellådan")
- **Ratt** ("Ratten kallas femte hjulet")
- **Broms** ("Hur ska du bromsa?")

Delarna kommer från din samling – dem hittar du i **skroten**. (Vill du fuska
fram delar direkt, se [Fusk och debug](#fusk-och-debug) längst ner.)

---

## Knappar och menyer

Längst upp finns en **topbar** med två knappar till höger:

### ⚙️ Inställningar
Öppnar en meny med:

| Val | Funktion |
|-----|----------|
| **Helskärm** | Visar spelet i helskärm. |
| **Visa spardata** | Öppnar en sida med din **rå spardata** (se [Hur framsteg sparas](#hur-framsteg-sparas)). |
| **Om spelet** | Kort information om den lokala kopian. |
| **Utvecklarläge** | Reglage som slår på/av debug (se [Fusk och debug](#fusk-och-debug)). |
| **Radera all spardata** | **Nollställer alla profiler.** Frågar först, går inte att ångra. |

### 🧰 Delshop
En affärsliknande meny för att **plocka fram bildelar direkt** – bekvämt för att
testa bygget utan att leta i skroten. Delarna är grupperade i logiska kategorier
(*Chassin & karosser*, *Motorer*, *Hjul & däck*, *Styrning*, *Bromsar*,
*Batterier*, *Bränsletank*, *Växellåda*, *Säten & möbler*, *Lampor & elektronik*,
*Dekor & udda prylar*) med renskrivna svenska namn, plus en *Övriga delar*-grupp
för de onumrerade. Det finns en **sökruta**, och delar som redan sitter på bilen
visas nedtonade. Klicka på en del så hamnar den i garaget.

Delshoppen fylls bara när du är i **garaget** (och fusk är på, vilket det är som
standard). Öppnar du den någon annanstans visas en upplysning om det.

---

## Kartor och världen

När du kör ut i **världen** rör du dig på ett rutnät av kartor.

- En **värld** (den som finns heter *"Da Hood"*) är ett rutnät på **5 rader × 6
  kolumner** av kartor. Du börjar på en bestämd ruta nära mitten.
- Varje **karta** (ruta) består av tre saker:
  - en **bakgrundsbild**,
  - en **topologi** – terrängen som avgör var du kan köra (bilderna i mappen
    `topography/`),
  - utplacerade **objekt**.
- Du kör fritt inom en karta. När du når **kanten** byts du automatiskt till
  grannrutan – kartan "rullar" alltså vidare ruta för ruta.

### Objekt på kartan
Objekten är sådant du kan köra fram till och interagera med:

| Typ | Vad det är |
|-----|------------|
| **Destination** (`#dest` / `#rdest`) | En plats – t.ex. ett hus eller en karaktär. Kör dit så byter spelet till den scenen (det är så du kommer till Figge Ferrum, bilshowen osv.). |
| **Korrekt-plats** (`#Correct`) | En plats där något ska levereras/stämma. |
| **Specialobjekt** (`#custom`) | Objekt med särskild logik. |
| **Kullar** (`#SmallHill` / `#BigHill`) | Terräng att ta sig över. |

---

## Uppdrag

Mulle får uppdrag på två sätt:

- **Telefon** – telefonen ringer med ett uppdrag.
- **Post** – ett brev kommer, ibland med en bild.

Varje uppdrag har en inspelad röstreplik som spelas upp. Spelet håller reda på
vilka uppdrag du **fått** och vilka du **slutfört**, och det sparas tillsammans
med resten av dina framsteg.

---

## Hur framsteg sparas

- Allt sparas **lokalt i din webbläsare**, under namnet `mulle_SaveData`. Det finns
  **inga konton och ingen molnlagring** – spardatan ligger i just den här
  webbläsaren på just den här datorn.
- Spelet sparar **automatiskt** medan du spelar (vid bygge och scenbyten).
- Per profil sparas bland annat:
  - **ditt namn** (profilen),
  - **din bil** (alla delar du satt ihop),
  - **dina skrotdelar** (din samling),
  - **slutförda och givna uppdrag**,
  - antal byggda bilar m.m.
- Flera profiler kan finnas samtidigt – du väljer profil i menyn.

**Bra att veta:**
- **Visa spardata** (i Inställningar) visar exakt vad som är sparat (som text).
- **Radera all spardata** (i Inställningar) raderar allt och låter dig börja om från noll.
- Tömmer du webbläsarens lagring (eller byter webbläsare) försvinner spardatan.

---

## Fusk och debug

Det här bygget har två utvecklarlägen:

- **Fusk** (`cheats`) – **på som standard.** Det är detta som fyller **Delshoppen**
  i garaget, så att du kan plocka fram vilken bildel som helst direkt istället för
  att leta i skroten.
- **Debug** (`debug`) – **av som standard.** Slås på via **Utvecklarläge** i
  Inställningar och ger utvecklaröverlägg: i körläget kan bilen flyttas/teleporteras
  med musen, och i världen ritas objektens info ut. Mest användbart för felsökning.

---

## Teknisk översikt (för den nyfikne)

Det här är en helt **statisk sajt** – servern gör inget annat än att skicka
filer. Delarna:

| Fil / mapp | Roll |
|------------|------|
| `server.py` | Liten trådad webbserver som kör spelet på `localhost:8000`. |
| `starta_mulle.command` | Startknapp – startar servern och öppnar webbläsaren. |
| `index.html` | Sidan som laddar spelet. |
| `bundle.js` | Själva spelet (Phaser-koden). |
| `phaser.min.js` | Spelmotorn (Phaser 2.8.8). |
| `assets/` | Grafik och ljud. |
| `data/` | Speldata: delar, objekt, kartor, världar, uppdrag (JSON). |
| `ui/` | Muspekare och gränssnittsbilder. |

Spelet renderas i en fast upplösning på 640×480 som skalas upp för att fylla
fönstret.
