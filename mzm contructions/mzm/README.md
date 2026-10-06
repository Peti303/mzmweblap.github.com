# MZM Construction — Landing · 2. FÁZIS

**Referencia:** [kononenkogroup.com](https://kononenkogroup.com) — a **"Refined & Bold Essential"** szekciótól az oldal legvégéig (Footer).

**Státusz:** statikus váz (1. fázis) + **GSAP + ScrollTrigger animációk, parallax, egyedi kurzor** (2. fázis). Nincs 3D / Canvas / WebGL.

## Fájlok

| Fájl | Szerep |
|---|---|
| `index.html` | **A leadandó, önálló fájl** — képek, betűtípusok ÉS a GSAP könyvtárak is inline (data-URI / beágyazott JS). Hálózat nélkül is teljesen működik. |
| `src/index.html` | Szerkeszthető forrás — itt a GSAP **CDN-es** `<script>` tag-ekkel. Éles honlapon ez használható közvetlenül. |
| `src/build.py` | `python3 src/build.py` → legyártja a gyökér `index.html`-t (CDN→inline csere + assetek beágyazása). |
| `assets/fonts/` | Hedvig Letters Serif (OFL) + Archivo (OFL) woff2. |
| `assets/img/` | AI-generált placeholder fotók (1024px) + `opt/` (640px, a beágyazáshoz). |
| `assets/js/` | gsap.min.js + ScrollTrigger.min.js (3.13.0, MIT-licencű — a build inline-olja). |

## Animációk (2. fázis)

### Scroll (GSAP + ScrollTrigger)
| Elem | Hatás |
|---|---|
| 1. szekció (`Refined & Bold Essential`) | Natív sticky "pin" (200vh), scrub: true. **SEBESSÉG-VEZÉRELT RUGALMAS KÜLLŐK (velocity-dial):** a küllők cubic Bézier `<path>`-ok (`M + C…`), álló helyzetben a vezérlőpontok KOLINEÁRIAK → tökéletesen egyenesek (mérés: 0.12px eltérés). A görbület KIZÁRÓLAG a két vezérlőpont tangenciális eltolása (végpontok rögzítve → a 01–08 számok végig a küllővégeken, Δ=0.0°). **LE gördítés:** CCW forgás + íves meghajlás (bend>0, ∝ scroll-sebesség, clamp ±78px); **FEL:** CW + ellentétes hajlás; **MEGÁLLÁS:** `elastic.out(1, 0.3)` gumirugó visszatérés egyenesbe (mérhető túllövéssel/oszilációval). Simított sebesség: `vS += (dy−vS)·0.16` a tickerben; forgás: `dial.vel += −vS·0.05`; a tl1 scrub a `dial.base` proxyra megy (0→110°) → a kettő SOHA nem ütközik; a kiírás (`qqg` rotation + `--rot`) egyetlen `apply()`-ból megy. A modul csak akkor aktív, amikor a `.nmc` a viewporton van (ScrollTrigger onToggle), kilépéskor a bend nullázódik. Mobil: a velocity-réteg itt is él (a szekció rövidebb). **Téma-váltás:** a háttér a pin második felében fehér→fekete; a fehér küllővonalak vastagsága a témával SZINKRONBAN scrub-elve 0.94px→1.45px (+54%) — fekete háttéren a vékony vonalak így is jól láthatóak (világos fázisban változatlan). **Címváltás odometer-effekttel:** a régi sorok felfelé gördülnek ki (`yPercent −115 + rotateX 60`), az újak alulról be (`yPercent 115 + rotateX −60`), scrub-determinista opacity-kapuval. No-JS: egyenes küllők + régi cím. |
| 2b. Galéria (2026-09-16, VÉGSŐ — szöveg-védelem + fade) | **Két új réteg:** (1) **BELÉPŐ FADE:** `op = clamp((0.86vh − gTop)/(0.26vh))` — a kártyák csak akkor tűnnek fel, amikor a .gal ténylegesen beérkezik (gal.top=950: opacity=0 → NEM jelennek meg korán); (2) **SZÖVEG-VÉDELEM:** ha a kártya nézeti X-e a szövegsávba (W·0.50-ig) esik, Y-a legalább `h3.bottom + 36 − gTop` (a cím AKTUÁLIS képernyő-pozíciójához képest) → a kártyák SOHA nem csúsznak rá a címsorra (mérve: 0 fedés user-pillanatban ÉS gal.top=120-nál is). Horgonyok: 0.70vh→0.30vh smoothstep² (a sor KÖZVETLEN a szöveg alatt fut), mX=+0.07W, platón p 0.35–0.72 a teljes diagonál kint, kör `end:'center 40%'` (10/10 kártya látható). NINCS pin, determinisztikus, 0 hiba; mobil ok; no-JS statikus; 10 meglévő kép. |
| 2. szekció (`People & Process`) | A **fotógyűrű pin-elve** forog (scrub, -8°→96°), a képekben **ellentétes irányú belső parallax** fut (`yPercent ±7`), a cím felette központan marad. A két bekezdés utána fade-in-up. |
| Statisztika-sorok (`15+ / 490+ / 45+ / 40K`) | Az eredeti logikájával: `toggleClass` alapú **"felgyulladás"** — a sor 'top 78%' -nál vált aktívvá (opacity .2→1), szekvenciálisan, ahogy gördülsz (hoverre is aktív). |
| 3. szekció (Brands) | Az óriáscím fade-in-up + scale belépés; a **partner-buborékok orbitja** a teljes szekción scrub-elve forog (0°→90°), a buborékok scale+fade belépéssel jönnek. |
| Footer | A **KNKO óriáslogó betűi alulról "tolódnak fel"** (`yPercent 105→0`, stagger .09) — mint az eredetinél; a nav/media/address/oszlopok data-reveal fade-in-up. |
| Általános | Minden szöveg/kártya `data-reveal` attribútummal **fade-in-up** (`y:44 → 0, opacity 0→1, power3.out`, opcionális késleltetéssel). |

### Hover / interaktív
- **Linkek:** lágy opacity-átmenet + **aláhúzás-sweep** (jobbról tűnik el, balról tér vissza — lekerekített, `cubic-bezier(.22,1,.36,1)`).
- **Fotógyűrű + galéria képei:** hoverre belső wrapper **scale 1.06–1.07** (smooth) — nem ütközik a GSAP mozgásokkal.
- **Partner-buborékok:** belső SVG **scale 1.1 + 4° dülöngés**.
- **Egyedi kurzor:** `mix-blend-mode: difference` **dot (7px) + lemaradó ring (34px)**; `gsap.quickTo`-val a ring lassabban követ (.42s) → prémium "lag" érzet; link/kép/buborék fölött **ring 1.9×-re nő, dot összehúzódik**; kattintásnál benyomódik.

### Robusztusság
- **Progresszív fejlesztés:** minden rejtett kezdeti állapotot a GSAP állít be → **JS/CDN nélkül az oldal teljesen látható és használható** (`html.js` kapu + `.js` hatókörű CSS).
- **`prefers-reduced-motion: reduce`** → minden animáció és a kurzor kikapcsol.
- **Mobil (≤767px):** nincs pin (a GSAP matchMedia kezeli) — csak belépő animációk; a kurzor csak finom pointeren (`hover:hover and pointer:fine`) aktív.
- **`ScrollTrigger.sort()` + refresh** load/font-ready után — a pin-spacer offset így minden triggerbe belefontolódik (ellenőrizve: a statisztika-triggerök px-pontosan a sorok 78%-ánál activálnak).

## Technika (1. fázisból változatlan)

- **Skála:** `:root{font-size:.0520833vw}` → 1920px-en 1rem = 1px; mobilon `.2666667vw` → 375px-en 1rem = 1px. Minden méret az eredeti px-értéke.
- **Rácsok / színek / tipográfia:** footer 15 oszlop (`repeat(15,1fr)`, 20rem gap), `#000 / #fff / #929292 / #f8f8f8`; **Hedvig Letters Serif** (az eredeti display-betű, OFL) + **Archivo** (Neue Montreal helyettesítő, OFL — a `--sans` változóval cserélhető).

## 3. fázisra váró pontok

- Valódi (nem scrub-elt) inertiahajtású smooth-scroll (pl. Lenis) — az eredeti tehetgés-hangulathoz
- Szövegek cseréje MZM tartalomra + MZM branding a footerben (óriás SVG logó)
- partner-logók véglegesítése (saját SVG/PNG)
- Esetleg: WebGL/3D elemek — ezt a megrendelő külön dönti el
