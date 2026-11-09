# BUILD BOOK – P1 „Czy to napisało AI?” (PsychoPy)
---

## 0. Metryczka

| Pole | Wartość |
|---|---|
| Przedmiot / karta | LBK · KL-A (rozdz. 0, 1, 14) |
| Zespół | Yevhen Rohozhynskyi (YR) · Vladyslav Uharov (VU) |
| Pakiet LBK | **P1** – Etykieta źródła AI a alokacja uwagi wzrokowej i ocena dowodów |
| Zgłoszenie w forum „Pytania do projektu”| 09.11.2026 – YR |
| Materiały źródłowe | `A_PROTOKOL_BADAWCZY.md` (protokół, v1.0), `B_INSIGHTLAB_BUILD_PACKAGE.md`, `LBK_1_dokumenty_i_skrypty.zip`, `LBK_2_bodzce_plansze_i_ekrany.zip`, `LBK_3_listy_gotowe_do_podmiany.zip` |
| Narzędzie budowy | PsychoPy Standalone **2026.2.5** (Windows, x64) – ta sama u YR i VU |
| Aparatura docelowa (LBK) | EyeLogic Lite 120 Hz / LogicOne 250 Hz; monitor 24″ 1920 × 1080, dystans 60–65 cm (1° ≈ 41 px) |
| Układ | 2 × 2 × 2 wewnątrzosobowo, 24 triale + 6 treningowych, 16 list (8 × 2 kierunki) |
| Repozytorium | https://github.com/s0nelywy111/repo_P1_KL-A_1.git |
| Wersja Build Booka | 0.1 (09.11.2026) |

### Struktura repozytorium

```
BUILD_BOOK.md
README.md
dane/nagranie.jsonl            ← 60 s z symulatora (KL-A)
narzedzia/opisz_nagranie.py    ← opis pól nagrania
materialy/                     ← (później) plansze PNG i tabela_triali.csv z pakietu P1
eksperyment/                   ← (później) plik .psyexp
```

---

## 1. Instalacja (dotychczasowe kroki)

| # | Krok | Polecenie / działanie | Oczekiwany wynik | Autor |
|---|---|---|---|---|
| 1.1 | Pobranie PsychoPy Standalone | psychopy.org → *Download* → Standalone dla Windows, plik `StandalonePsychoPy-2026.2.5-…-win64.exe`  | instalator na dysku | YR|
| 1.2 | Instalacja | uruchomić instalator; ścieżka instalacji `D:\Program\PsychoPy` | w menu Start: „PsychoPy-2026.2.5” | YR|
| 1.3 | Pierwsze uruchomienie | menu Start → PsychoPy-2026.2.5; zamknąć okna „Porada dnia” i „Changes in …” (OK). Otwiera się **Runner**; Builder: *Window → Show builder* | okno *PsychoPy Builder (v2026.2.5)* | YR |
| 1.4 | Odczyt wersji | pasek tytułu okna Builder/Runner (lub *Help → About*) | wersja: **2026.2.5** | YR |
| 1.5 | Demo | Builder: *Demos → Unpack Demos…* → wybrać folder *Dokumenty* (PsychoPy tworzy w nim `PsychoPy3 Demos`) → *Demos → Experiments → stroop* → zamknąć okno readme → przełącznik *Pilot/Run* na **Run** → zielony przycisk ▶ → w oknie dialogowym `participant` = `test`, OK → odpowiedzi strzałkami: ← czerwone, ↓ zielone, → niebieskie litery | wszystkie triale przechodzą; Runner, zakładka *Stdout*: `## Running: …\PsychoPy3 Demos\Experiments\stroop\stroop_lastrun.py ##` | YR |
| 1.6 | Ta sama wersja u drugiej osoby | powtórzyć 1.1–1.5 | wersja **identyczna** z 1.4: **2026.2.5** | VU|
| 1.7 | Python do skryptów pomocniczych | `python --version` (≥ 3.8) | **Python 3.13.5** | VU|
| 1.8 | Repozytorium | utworzyć prywatne repo **GitHub**, dodać prowadzącego (*Read*), `git clone https://github.com/s0nelywy111/repo_P1_KL-A_1.git` | lokalna kopia | VU |
| 1.9 | Symulator | pobrać z platformy AHE „Kod do laboratorium – symulator i klient startowy” (*Pobierz folder*) → rozpakować do `narzedzia/` → `python narzedzia/symulator_biosygnalow.py --mode file --duration 60 --out dane/nagranie.jsonl` (Python 3.8+, tylko biblioteka standardowa; bez `--seed` wartości różnią się przy każdym uruchomieniu – dla powtarzalności dodać np. `--seed 1`) | komunikat `Zapisano dane/nagranie.jsonl`; 241 linii JSON (t = 0…60 s, 4 Hz) | YR |
| 1.10 | Opis pól | `python narzedzia/opisz_nagranie.py dane/nagranie.jsonl` | 8 pól: `t, seq, hr, rr_ms, eda_us, focus, quality, scenario`; ≈ 4 rekordy/s; brak wzroku, źrenicy, oddechu | YR |
| 1.11 | Wersja i tag | `git add . && git commit -m "KL-A" && git tag KL-A && git push --tags` | tag `KL-A` widoczny w repo | VU |

**Problemy napotkane i rozwiązania**

| Problem | Rozwiązanie | Autor |
|---|---|---|
| Demo *stroop* (2026.2.5): po ostatnim trialu `IndexError: list index out of range` w `trials.saveAsExcel(...)` (`psychopy\data\trial.py`, l. 1496); „Experiment ended with exit code 1”. Wszystkie triale wyświetliły się i przyjmowały odpowiedzi – błąd dotyczy tylko eksportu .xlsx w demie. | Uznajemy demo za uruchomione: plik `PsychoPy3 Demos\Experiments\stroop\data\test_2026-11-09_21h37.35.386.csv` powstał mimo błędu – 30 triali (5 powtórzeń × 6 warunków), `psychopyVersion` = 2026.2.5, `frameRate` ≈ 165 Hz, wszystkie odpowiedzi poprawne. RT ≈ 2,7–3,4 s są sztucznie długie (odpowiedzi wprowadzane zdalnie, test techniczny, nie dane uczestnika). We własnym eksperymencie nie używamy `saveAsExcel` – zapis domyślny CSV. | YR |
| Ostrzeżenia `Parameters not known to this version of PsychoPy` (parametry eye-trackera: `elAddress`, `plPupil…`, `tbModel`…) przy generowaniu skryptu dema | nieszkodliwe – plik dema zawiera ustawienia z innej wersji; nie dotyczy działania | YR|

---

## 14. Pierwsze pytania do LBK

| # | Pytanie | Dlaczego ważne dla P1 | Autor |
|---|---|---|---|
| 14.1 | Czy w LBK możemy sterować eksperymentem z PsychoPy (wtyczka EyeLogic do PsychoPy / ioHub), czy obowiązuje InsightLab? Którą wersję wtyczki i PsychoPy macie zainstalowaną? | od tego zależy, czy budujemy pętlę na `tabela_triali.csv`, czy liniowy łańcuch z pakietu B | YR |
| 14.2 | Który tracker będzie dostępny – Lite 120 Hz czy LogicOne 250 Hz? | 120 Hz wystarcza do dwell/fiksacji, nie do dynamiki sakkad | YR|
| 14.3 | Czy PsychoPy może wysyłać znaczniki zdarzeń (onset karty, SPACJA, odpowiedź) do zapisu okoruchowego i do EDA/EKG – wspólny zegar, LSL czy TTL? | bez synchronizacji nie policzymy CEAP dla karty ani okna SCR 1–5 s po karcie | VU |
| 14.4 | Czy eksport zawiera surowe próbki z flagą ważności i średnicą źrenicy, czy tylko gotowe fiksacje? Jaki algorytm i parametry detekcji fiksacji? | kryterium ≥ 70% ważnych próbek; protokół zakłada przeliczenie I2MC | VU |
| 14.5 | Ile punktów ma kalibracja, czy jest walidacja z błędem w stopniach i czy można rekalibrować w środku sesji (po trialu 8 i 16)? | kryterium < 1,0° i RMS < 0,5° | YR|
| 14.6 | Czy jest podpórka pod brodę i czy jasność monitora / oświetlenie są stałe i zmierzone? | dane źrenicy są interpretowalne tylko przy stałej luminancji | VU |
| 14.7 | Czy aparatura zapisuje obraz oka/twarzy domyślnie i czy da się to wyłączyć? | RODO – protokół zakłada brak wideo oka | YR |
| 14.8 | Czy można zablokować wszystkie klawisze poza F, J, 1–7, SPACJA? | odpowiedzi uczestnika w protokole | VU |
