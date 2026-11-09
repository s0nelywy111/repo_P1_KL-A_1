# KL-A – Człowiek jako źródło danych · mapa sygnałów

**Zespół:** Yevhen Rohozhynskyi (YR) · Vladyslav Uharov (VU)
**Pakiet:** P1 „Czy to napisało AI?” – *Etykieta źródła AI a alokacja uwagi wzrokowej i ocena dowodów*
**Repozytorium:** https://github.com/s0nelywy111/repo_P1_KL-A_1.git · tag `KL-A`

---

## 1. Co mierzy badanie główne P1 (zmienne zależne → sygnał)

Układ 2 (sprawca: redaktor / system AI) × 2 (weryfikacja: brak / ekspert) × 2 (wniosek: uzasadniony W / nieuzasadniony N), wewnątrzosobowo, 24 triale. Trial: krzyż 800 ms → karta informacyjna (tempo własne, maks. 45 s, SPACJA) → Q1–Q6 → przerwa 600 ms. Analiza okoruchowa dotyczy **tylko karty**.

| Zmienna zależna | Co to jest | Sygnał / źródło |
|---|---|---|
| **CEAP** (pierwszorzędna) | dwell(blok KRYTYCZNY) / [dwell(KRYTYCZNY) + dwell(WYNIK)] | wzrok – fiksacje w AOI `SLOT1`/`SLOT2` + rola slotu z `tabela_triali.csv` |
| FIRSTPASS_CEAP | CEAP z pierwszego przebiegu czytania | wzrok – sekwencja fiksacji |
| SAP, SDI | udział / log-iloraz dwell źródła vs dowodów | wzrok – dwell w `SRC_AGENT`, `SRC_VERIF` |
| SKIP | 0 fiksacji w bloku krytycznym (0/1) | wzrok – liczba fiksacji w AOI |
| SRC_RETURN | liczba powrotów do paska źródła | wzrok – wejścia do AOI (visit count) |
| TOTALTIME | czas ekspozycji karty | zachowanie – czas do naciśnięcia SPACJI |
| Werdykt Q1 → *d′*, *c* | TAK (F) / NIE (J) vs poprawna odpowiedź | zachowanie – odpowiedź klawiszem |
| Q2–Q4 | wiarygodność informacji, pewność, wiarygodność źródła (1–7) | zachowanie – ocena na skali |
| Q5, Q6 | rekomendacja udostępnienia; pytanie kontrolne (zaangażowanie) | zachowanie – odpowiedź |
| E4 (eksploracyjnie) | średnica źrenicy jako indeks obciążenia | źrenica – tylko przy stałej luminancji |

Protokół nie przewiduje EDA, EKG ani oddechu – w tabeli poniżej używam ich jako sygnałów **dodatkowych** z aparatury LBK (wiersz 3).

---

## 2. Model procesora ludzkiego – skale czasu (Card, Moran i Newell, 1983)

| Parametr | Wartość typowa [zakres] |
|---|---|
| Cykl procesora percepcyjnego τP | 100 ms [50–200] |
| Cykl procesora poznawczego τC | 70 ms [25–170] |
| Cykl procesora motorycznego τM | 70 ms [30–100] |
| Ruch oka (sakkada + fiksacja) | 230 ms [70–700] |
| Prosta reakcja (τP + τC + τM) | ≈ 240 ms [105–470] |

Z tego wynika reguła: system nie musi reagować szybciej niż jeden cykl percepcyjny (~100 ms), bo człowiek i tak nie zmieni zachowania w krótszym czasie. Musi natomiast zdążyć **przed** zdarzeniem, które chce wychwycić albo uratować (następną fiksacją, końcem triala, następnym blokiem).

---

## 3. Tabela: stan → sygnał → wymagany czas reakcji → możliwy błąd interpretacji

| # | Stan uczestnika / pomiaru | Sygnał | Wymagany czas reakcji systemu (uzasadnienie z modelu procesora) | Możliwy błąd interpretacji |
|---|---|---|---|---|
| 1 | **Utrata śledzenia wzroku** na karcie (głowa poza polem 30 × 20 cm, odbicia w okularach, spojrzenie na klawiaturę F/J) | wzrok – flaga ważności próbek / brak współrzędnych, % ważnych próbek w trialu (próg ≥ 70%) | **≤ 100–250 ms** (1 cykl τP ≈ jedna fiksacja ~230 ms). Wykrycie musi nastąpić w czasie jednej fiksacji, bo pojedyncza fiksacja w bloku krytycznym przesądza o SKIP i CEAP. Decyzja „trial do odrzucenia / przerwa i rekalibracja” – w przerwie 600 ms przed następnym trialem. | **Mrugnięcie** (100–400 ms) albo krótkie spojrzenie na klawiaturę uznane za utratę śledzenia – i odwrotnie: utrata danych w bloku krytycznym odczytana jako **SKIP = 1** („nie przeczytał”), choć uczestnik czytał, tylko tracker go nie widział. |
| 2 | **Pominięcie bloku krytycznego / powierzchowne czytanie** (pośpiech, zgadywanie) | wzrok – liczba fiksacji i dwell w AOI `SLOT1`/`SLOT2` (rola KRYTYCZNY); zachowanie – TOTALTIME < 10 s, błędna odpowiedź w Q6 | **Rzędu sekund – na koniec karty** (po SPACJI, przed Q1). Czytanie 97 słów to ~100+ fiksacji × ~230 ms ≈ 15–30 s; ocenę można wydać dopiero, gdy cały przebieg czytania się skończył. Szybsza reakcja (w trakcie karty) nie ma sensu, bo uczestnik może jeszcze wrócić do bloku. | **Czytanie parafowealne** – informację z sąsiedniej linii można wydobyć bez fiksacji (Rayner, 2009), więc „0 fiksacji” ≠ „nie przetworzył”. Również **dryf kalibracji**: fiksacje przesunięte o > 1° (41 px) wypadają w pas neutralny albo w sąsiednie AOI – wygląda to na pominięcie, a jest błędem pomiaru. |
| 3 | **Podwyższone pobudzenie** w reakcji na kartę (np. na etykietę „system AI”) | EDA – odpowiedź skórno-galwaniczna (SCR, latencja 1–3 s); HR/HRV z EKG; dodatkowo zmiana średnicy źrenicy | **Okno 1–5 s po pojawieniu się karty**; analiza po trialu, nie w czasie rzeczywistym. Reakcja autonomiczna jest wielokrotnie wolniejsza niż cykle τP/τC (~100 ms): SCR pojawia się 1–3 s po bodźcu, HR zmienia się w skali kilku uderzeń serca. Detektor szybszy niż ~1 s łapałby tylko szum. | SCR i wzrost HR wywołane **ruchem i oddechem** (naciśnięcie klawisza, głęboki wdech, westchnienie), a nie etykietą. Przy źrenicy: zmiana wynika z **luminancji / gęstości tekstu** albo z kąta patrzenia (pasek u góry vs dół karty), a nie z obciążenia – protokół (11.4) dopuszcza źrenicę wyłącznie eksploracyjnie. |

**Stan dodatkowy (poza punktacją):** zmęczenie w ciągu 24 triali – rosnąca liczba mrugnięć, narastający dryf, wydłużone RT, spadek trafności Q6; reakcja w skali minut (kontrola w przerwach po trialu 8 i 16). Błąd: przyspieszanie się z wprawą (efekt uczenia) maskuje zmęczenie.

---

## 4. Symulator – nagranie 60 s

**Źródło:** platforma AHE → „Kod do laboratorium – symulator i klient startowy” → `symulator_biosygnalow.py` (tylko biblioteka standardowa Pythona 3.8+).
**Polecenie:** `python symulator_biosygnalow.py --mode file --duration 60` → plik `nagranie.jsonl` (domyślne: scenariusz `mix`, 4 Hz, `--noise 0.1`, `--dropout 0.05`, bez ziarna – każde uruchomienie daje inne wartości).
**Wynik:** 241 rekordów NDJSON (t = 0,00 … 60,00 s co 0,25 s), w tym 232 × `ok`, 5 × `noisy`, 4 × `lost`; scenariusz: `spokoj` (0–40 s) → `skupienie` (40–60 s).

Przykładowy rekord:
```json
{"t": 0.0, "seq": 0, "hr": 70.1, "rr_ms": 866, "eda_us": 2.49, "focus": 0.57, "quality": "ok", "scenario": "spokoj"}
```

| Pole | Typ | Zakres w nagraniu (tylko `ok`) | Sygnał / znaczenie | Odpowiednik w aparaturze LBK |
|---|---|---|---|---|
| `t` | float, s | 0–60 | czas próbki od startu symulacji (krok 0,25 s = 4 Hz) | znacznik czasu urządzenia – **własny zegar**, bez synchronizacji z bodźcem (→ LSL, KL-B) |
| `seq` | int | 0–240 | numer kolejny próbki; luka w `seq` = zgubiona próbka transmisji | licznik próbek |
| `hr` | float, bpm / null | 65,7–77,6 (śr. 69,9) | tętno – wartość już wyliczona, wygładzona | **EKG** → HR (aparatura daje surowy EKG, HR trzeba policzyć z załamków R) |
| `rr_ms` | int, ms / null | 737–955 (śr. 859) | odstęp między uderzeniami serca (RR/IBI) → podstawa **HRV** (np. RMSSD w `klient_startowy.py`) | **EKG** → interwały RR |
| `eda_us` | float, µS / null | 1,98–3,11 (śr. 2,41) | aktywność elektrodermalna: poziom toniczny (SCL) + losowe odpowiedzi fazowe SCR (+0,2–0,8 µS) | **EDA/GSR** |
| `focus` | float 0–1 / null | 0,31–0,94 | syntetyczny „indeks skupienia” – **nie jest sygnałem fizjologicznym**, tylko gotową etykietą-estymatą | brak bezpośredniego odpowiednika (w LBK trzeba by go wyliczyć, np. z wzroku/HRV) |
| `quality` | str | `ok` / `noisy` / `lost` | jakość próbki: `noisy` = artefakt ruchowy (HR ±25–60 bpm, EDA +1,5–4 µS – np. `hr` = 17 lub 100 w nagraniu), `lost` = utrata kontaktu (wszystkie sygnały = null) | flaga jakości / utrata kontaktu elektrody |
| `scenario` | str | `spokoj`, `skupienie` | „prawda” symulacji – **tylko do ewaluacji**, nie wolno jej używać do sterowania | brak – w realnym badaniu stanu nie znamy |

**Czego symulator nie wysyła:**
☒ **wzrok** – brak współrzędnych spojrzenia, fiksacji, AOI i flagi ważności eye-trackera
☒ **średnica źrenicy**
☒ **oddech** – brak sygnału respiracji (częstość, amplituda)
☒ surowy EKG (jest tylko gotowe HR i RR) oraz znaczniki zdarzeń/bodźców

**Konsekwencja dla P1:** główne zmienne P1 (CEAP, SKIP, SAP, SRC_RETURN) pochodzą z eye-trackera, więc na symulatorze nie da się ich przetestować – wiersze 1 i 2 tabeli wymagają MouseGaze (zastępczo, myszą) albo aparatury LBK. Symulator obsługuje wiersz 3 (pobudzenie: `eda_us`, `hr`, `rr_ms`) i pozwala ćwiczyć obsługę braków i artefaktów (`quality` = `noisy` / `lost`), które w P1 odpowiadają problemom z wiersza 1. Brak wspólnego zegara z bodźcem (`t` liczone od startu symulatora) to dokładnie problem z okna SCR 1–5 s po karcie – rozwiązanie: LSL (KL-B).
