"""Opis pól nagrania JSONL z symulatora (KL-A).

Użycie:  python opisz_nagranie.py dane/nagranie.jsonl
Wypisuje: liczbę rekordów, czas trwania, częstotliwość próbkowania,
każde pole (także zagnieżdżone) z typem, min/max i przykładem
oraz listę sygnałów LBK, których w nagraniu nie znaleziono.
"""
import json
import sys
from collections import OrderedDict


def splaszcz(obj, prefix=""):
    out = OrderedDict()
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(splaszcz(v, f"{prefix}{k}."))
    elif isinstance(obj, list) and obj and all(isinstance(x, (int, float)) for x in obj):
        out[prefix[:-1]] = obj  # wektor liczb traktujemy jako jedno pole
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(splaszcz(v, f"{prefix}{i}."))
    else:
        out[prefix[:-1]] = obj
    return out


def main(path):
    rekordy, zle = [], 0
    with open(path, encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if not linia:
                continue
            try:
                rekordy.append(splaszcz(json.loads(linia)))
            except json.JSONDecodeError:
                zle += 1
    print(f"Plik: {path}\nRekordów: {len(rekordy)}  (niepoprawnych linii: {zle})")
    if not rekordy:
        return

    pola = OrderedDict()
    for r in rekordy:
        for k, v in r.items():
            pola.setdefault(k, []).append(v)

    # pole czasu: pierwsze, którego nazwa sugeruje czas i jest liczbowe
    czas = next((k for k in pola if (k.lower() in ("t", "ts") or any(s in k.lower() for s in ("time", "czas", "t_")))
                 and all(isinstance(v, (int, float)) for v in pola[k])), None)
    if czas:
        t = pola[czas]
        dt = t[-1] - t[0]
        print(f"Pole czasu: {czas}  zakres: {t[0]} … {t[-1]}  (Δ = {dt})")
        if dt > 0:
            # zgadujemy jednostkę: > 1e6 → µs/ns lub ms epoki
            print(f"Śr. częstotliwość ≈ {(len(t) - 1) / dt:.4g} rekordów na jednostkę czasu")

    print("\n| Pole | Typ | Obecne w % rekordów | Min | Max | Przykład |")
    print("|---|---|---|---|---|---|")
    for k, vals in pola.items():
        typy = sorted({type(v).__name__ for v in vals})
        num = [v for v in vals if isinstance(v, (int, float)) and not isinstance(v, bool)]
        mn = f"{min(num):.4g}" if num else ""
        mx = f"{max(num):.4g}" if num else ""
        przyklad = json.dumps(vals[0], ensure_ascii=False)[:40]
        print(f"| `{k}` | {'/'.join(typy)} | {100 * len(vals) / len(rekordy):.0f} | {mn} | {mx} | {przyklad} |")

    klucze = " ".join(pola).lower()
    sygnaly = {
        "wzrok (gaze x/y, fiksacje)": ("gaze", "eye", "fix", "wzrok"),
        "źrenica": ("pupil", "zrenic", "źrenic"),
        "oddech": ("resp", "breath", "oddech"),
        "EDA": ("eda", "gsr", "scl", "scr", "skin"),
        "EKG / HR": ("ecg", "ekg", "hr", "heart", "rr", "ibi"),
    }
    print("\nSygnały LBK (heurystyka po nazwach pól – sprawdź ręcznie):")
    for nazwa, wzorce in sygnaly.items():
        jest = any(w in klucze for w in wzorce)
        print(f"  [{'x' if jest else ' '}] {nazwa}{'' if jest else '  ← NIE ZNALEZIONO'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
