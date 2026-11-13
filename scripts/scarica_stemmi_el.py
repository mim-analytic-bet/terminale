#!/usr/bin/env python3
"""Scarica gli stemmi ufficiali trasparenti (PNG) per le 24 squadre di Europa League
e li salva direttamente in assets/loghi/<slug>.png.
"""
import os, sys, json, re, urllib.request, urllib.parse, ssl, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGHI_DIR = os.path.join(BASE, "assets", "loghi")
os.makedirs(LOGHI_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "AntigravityBot/1.0 (calcio-terminale-official@gmail.com)"
}
CTX = ssl._create_unverified_context()

MAPPATURA = {
    "az_alkmaar": "AZ_Alkmaar",
    "anderlecht": "RSC_Anderlecht",
    "ararat_armenia": "FC_Ararat-Armenia",
    "benfica": "S.L._Benfica",
    "besiktas": "Beşiktaş_J.K.",
    "celtic": "Celtic_F.C.",
    "dinamo_zagreb": "GNK_Dinamo_Zagreb",
    "ferencvaros": "Ferencvárosi_TC",
    "hapoel_be_er": "Hapoel_Be'er_Sheva_F.C.",
    "jagiellonia_bialystok": "Jagiellonia_Białystok",
    "lech_poznan": "Lech_Poznań",
    "levski_sofia": "PFC_Levski_Sofia",
    "nec_nijmegen": "NEC_Nijmegen",
    "nk_celje": "NK_Celje",
    "ofi_crete": "OFI_Crete_F.C.",
    "olympiacos": "Olympiacos_F.C.",
    "omonia_nicosia": "AC_Omonia",
    "rb_salzburg": "FC_Red_Bull_Salzburg",
    "sparta_prague": "AC_Sparta_Prague",
    "stade_rennais": "Stade_Rennais_F.C.",
    "sturm_graz": "SK_Sturm_Graz",
    "torreense": "S.C.U._Torreense",
    "union_st_gilloise": "Royale_Union_Saint-Gilloise",
    "viktoria_plzen": "FC_Viktoria_Plzeň"
}

def trova_logo_file(wiki_page):
    url = f"https://en.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(wiki_page)}&redirects=1&section=0&prop=wikitext&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12, context=CTX) as resp:
        data = json.loads(resp.read().decode())
        wt = data.get("parse", {}).get("wikitext", {}).get("*", "")
        m = re.search(r"\|\s*(?:clublogo|logo|image_shield|image|badge)\s*=\s*([^|\n}]+)", wt, re.I)
        if m:
            val = m.group(1).strip()
            # Pulizia sintassi tipo [[File:Name.svg|150px]]
            val = re.sub(r"^\[\[(?:File|Image):", "", val, flags=re.I)
            val = val.split("|")[0].replace("]]", "").strip()
            return val
    return None

def ottieni_png_url(filename, width=256):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&iiurlwidth={width}&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12, context=CTX) as resp:
        data = json.loads(resp.read().decode())
        pages = data.get("query", {}).get("pages", {})
        p = list(pages.values())[0]
        ii = p.get("imageinfo", [{}])[0]
        return ii.get("thumburl") or ii.get("url")

def scarica_file(url, dest_path):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
        dati = resp.read()
        if not dati.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError(f"Dati scaricati non sono un PNG valido ({dati[:10]})")
        with open(dest_path, "wb") as f:
            f.write(dati)
        return len(dati)

def main():
    print(f"=== Scarico stemmi ufficiali Europa League ({len(MAPPATURA)} squadre) ===")
    ok = 0
    for slug, wiki_page in MAPPATURA.items():
        dest = os.path.join(LOGHI_DIR, f"{slug}.png")
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            print(f"[OK ESISTE] {slug}.png ({os.path.getsize(dest)} bytes)")
            ok += 1
            continue
        try:
            print(f"Ricerca {slug} ({wiki_page})...", end=" ", flush=True)
            logo_name = trova_logo_file(wiki_page)
            if not logo_name:
                print(f"FAILED (nessun logo nel wikitext)")
                continue
            time.sleep(0.5)
            png_url = ottieni_png_url(logo_name)
            if not png_url:
                print(f"FAILED (nessun url per {logo_name})")
                continue
            time.sleep(0.5)
            sz = scarica_file(png_url, dest)
            print(f"SCARICATO {logo_name} -> {slug}.png ({sz} bytes)")
            ok += 1
        except Exception as e:
            print(f"ERRORE: {e}")
        time.sleep(0.8)
    print(f"\nRisultato: {ok} / {len(MAPPATURA)} stemmi ufficiali pronti su disco.")

if __name__ == "__main__":
    main()
