def main():
    with open('scheda-partita-dashboard.html', 'r', encoding='utf-8') as f:
        text = f.read()

    target = 'document.getElementById("xg-dettaglio-ospite").textContent = `Attesi: ${m.golO} gol`;'

    logo_update_code = """
      // Loghi Ufficiali e Watermark Sfondo
      const logoC = LOGHI_SQUADRE[m.casa.nome] || "";
      const logoO = LOGHI_SQUADRE[m.ospite.nome] || "";

      const imgC = document.getElementById("logo-casa");
      const siglaC = document.getElementById("sigla-casa");
      if (imgC && logoC) {
        imgC.src = logoC;
        imgC.classList.remove("hidden");
        imgC.style.display = "";
        siglaC.classList.add("hidden");
      } else if (imgC) {
        imgC.classList.add("hidden");
        siglaC.classList.remove("hidden");
      }

      const imgO = document.getElementById("logo-ospite");
      const siglaO = document.getElementById("sigla-ospite");
      if (imgO && logoO) {
        imgO.src = logoO;
        imgO.classList.remove("hidden");
        imgO.style.display = "";
        siglaO.classList.add("hidden");
      } else if (imgO) {
        imgO.classList.add("hidden");
        siglaO.classList.remove("hidden");
      }

      // Watermark sfondo sfumati
      const wmC = document.getElementById("watermark-casa");
      const wmO = document.getElementById("watermark-ospite");
      if (wmC && logoC) wmC.src = logoC;
      if (wmO && logoO) wmO.src = logoO;

      // Aggiorna striscia partite del turno con highlight attivo
      aggiornaStrisciaPartite(turno, m.id);
"""

    if target in text and 'const imgC = document.getElementById("logo-casa")' not in text:
        text = text.replace(target, target + '\n' + logo_update_code, 1)
        with open('scheda-partita-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print('Successfully injected logo rendering into renderizzaPartita!')
    else:
        print('Already present or target not found')

if __name__ == '__main__':
    main()
