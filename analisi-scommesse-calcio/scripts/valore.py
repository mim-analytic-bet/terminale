#!/usr/bin/env python3
"""Probabilità implicita, quota equa e valore di un pronostico o di una multipla.

Uso:
  valore.py QUOTA PROB              es. valore.py 1,85 58
  valore.py --combo Q:P Q:P [...]   es. valore.py --combo 1,30:80 1,28:82 1,35:77

PROB è la probabilità stimata in percentuale (58 = 58%).
La multipla vale solo per eventi su partite diverse (indipendenti).
"""
import sys


def num(s):
    return float(s.strip().replace("%", "").replace(",", "."))


def it(x, dec=2):
    return f"{x:.{dec}f}".replace(".", ",")


def segno(x):
    return "+" if x >= 0 else ""


def stampa(quota, prob):
    valore = prob * quota - 1
    print(f"Quota: {it(quota)}")
    print(f"Prob. implicita: {it(100 / quota, 1)}%")
    print(f"Prob. stimata: {it(prob * 100, 1)}%  (circa {round(prob * 10)} volte su 10)")
    print(f"Quota equa (1/prob. stimata): {it(1 / prob)}")
    print(f"Valore: {segno(valore)}{it(valore * 100, 1)}%")


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    if argv[0] == "--combo":
        coppie = [a.split(":") for a in argv[1:]]
        if len(coppie) < 2:
            print("Servono almeno 2 eventi.")
            return 1
        quota, prob = 1.0, 1.0
        for q, p in coppie:
            quota *= num(q)
            prob *= num(p) / 100
        print(f"Multipla di {len(coppie)} eventi")
        stampa(quota, prob)
        return 0
    stampa(num(argv[0]), num(argv[1]) / 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
