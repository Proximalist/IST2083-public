#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IST2083 — alıştırma şıklarını yeniden dağıtan betik.

NEDEN VAR
---------
13 Eylül 2026 denetiminde, depodaki 269 çoktan seçmeli sorunun 196'sında
(%72.9) doğru cevabın "b" şıkkı olduğu bulundu (chi-kare = 341, df = 3;
tekdüze beklenti her şık için %25). "d" şıkkı 269 sorunun yalnızca 2'sinde
doğruydu. Bunun kaynağı soru yazımındaki bir reflekstir: önce bir bariz
çeldirici, hemen ardından doğru cevap.

Sınavlarda şık sırası gruplar arasında karıştırıldığı için sınavın kendisi
bundan zarar görmez; zarar gören, alıştırmaların TEK işlevidir — öğrencinin
sınav öncesinde kendi durumunu ölçmesi. Hiçbir şey bilmeden tüm sorulara
"b" diyen öğrenci alıştırmalardan %72.9 alıyordu.

NE YAPAR
--------
Her modülde doğru cevapları a/b/c/d arasında olabildiğince eşit dağıtır,
ardından her sorunun kalan çeldiricilerini kendi içinde karıştırır.
Hem `NN_modul_alistirmalar.qmd` hem `NN_modul_cevap_anahtari.qmd` aynı
anda güncellenir.

TASARIM KARARLARI
-----------------
1. Sabit tohum (`TOHUM`). Betik iki kez çalıştırıldığında aynı sonucu
   verir; çıktı yeniden üretilebilir kalır ve git farkı gürültülenmez.
2. Şık ön ekleri (`a\\)`, `b)` gibi) YERİNDE KALIR; yalnızca metinler
   slotlar arasında taşınır. Kaynak dosyadaki kaçış karakteri düzeni
   (bazı satırlarda `a\\)`, bazılarında `b)`) pandoc'un "fancy list"
   ayrıştırmasıyla ilgilidir; ona hiç dokunmuyoruz ki render çıktısı
   biçim olarak birebir aynı kalsın.
3. Cevap anahtarındaki açıklama metninde parantez içi şık atıfları
   (`(c) yanlıştır` gibi) yeni harflere göre yeniden yazılır.
4. Sıralı/sayısal şık kümeleri (tüm şıkları sayı olan sorular)
   karıştırılmaz — sayısal şıklarda artan sıra bir okuma kolaylığıdır.

KULLANIM
--------
    python3 scripts/sik-permutasyonu.py            # denetim (dosya yazmaz)
    python3 scripts/sik-permutasyonu.py --uygula   # dosyaları güncelle
"""

from __future__ import annotations

import random
import re
import sys
from collections import Counter
from pathlib import Path

TOHUM = 20262027  # 2026-2027 Güz
KOK = Path(__file__).resolve().parent.parent
MODULLER = [f"{n:02d}_modul" for n in range(1, 15)]

# Bir sorunun gövdesinde şık satırının başlangıcı: "a) " veya "a\) "
SIK_BAS = re.compile(r"^([a-e])(\\?\))(.*)$")
SORU_BAS = re.compile(r"^\*\*(\d+)\.\*\*")
CEVAP_BAS = re.compile(r"^\*\*(\d+)\. Doğru cevap: ([a-e])\)\*\*", re.M)
SAYISAL = re.compile(r"^[\s$\\a-zA-Z]*[-+]?\d[\d.,]*\s*[^\n]{0,25}$")


class Soru:
    """Bir alıştırma sorusunun şık bloğu."""

    def __init__(self, numara, satir_araligi, onekler, metinler, son_devam):
        self.numara = numara
        self.satir_araligi = satir_araligi  # (bas, bit) alıştırma satırlarında
        self.onekler = onekler              # ['a\\)', 'b)', ...] — yerinde kalır
        self.metinler = metinler            # şık metinleri (çok satırlı olabilir)
        self.son_devam = son_devam          # son şıkta satır sonu `\` var mıydı


def alistirma_ayristir(satirlar):
    """Alıştırma dosyasını soru bloklarına ayırır."""
    sorular = []
    i = 0
    while i < len(satirlar):
        m = SORU_BAS.match(satirlar[i])
        if not m:
            i += 1
            continue
        numara = int(m.group(1))
        # Şık bloğunu bul: sonraki "a)" satırından başlayıp boş satıra kadar
        j = i + 1
        while j < len(satirlar) and not SIK_BAS.match(satirlar[j]):
            if SORU_BAS.match(satirlar[j]) or satirlar[j].startswith("## "):
                break
            j += 1
        if j >= len(satirlar) or not SIK_BAS.match(satirlar[j]):
            i += 1
            continue
        bas = j
        onekler, metinler = [], []
        while j < len(satirlar) and satirlar[j].strip():
            m2 = SIK_BAS.match(satirlar[j])
            if m2:
                onekler.append(m2.group(1) + m2.group(2))
                metinler.append(m2.group(3).lstrip())
            else:
                # önceki şıkkın devam satırı
                if not metinler:
                    break
                metinler[-1] += "\n" + satirlar[j]
            j += 1
        bit = j
        # Satır sonu `\` işaretlerini metinden ayır
        son_devam = metinler[-1].endswith("\\") if metinler else False
        metinler = [t[:-1] if t.endswith("\\") else t for t in metinler]
        if len(onekler) >= 2:
            sorular.append(Soru(numara, (bas, bit), onekler, metinler, son_devam))
        i = bit
    return sorular


def sayisal_kume(metinler):
    """Tüm şıklar sayı ile başlıyorsa True — bu soruda sıra korunur."""
    return all(SAYISAL.match(t.strip()) for t in metinler)


def hedef_dagilim(n, harfler, rng):
    """n soruyu harfler arasında olabildiğince eşit dağıtan liste."""
    tam, kalan = divmod(n, len(harfler))
    hedef = [h for h in harfler for _ in range(tam)]
    hedef += rng.sample(harfler, kalan)
    rng.shuffle(hedef)
    return hedef


def modulu_isle(modul, rng, uygula):
    a_yol = KOK / modul / f"{modul}_alistirmalar.qmd"
    c_yol = KOK / modul / f"{modul}_cevap_anahtari.qmd"
    a_satir = a_yol.read_text(encoding="utf-8").split("\n")
    c_metin = c_yol.read_text(encoding="utf-8")

    sorular = alistirma_ayristir(a_satir)
    dogrular = {
        int(m.group(1)): m.group(2)
        for m in CEVAP_BAS.finditer(c_metin)
    }
    eksik = [s.numara for s in sorular if s.numara not in dogrular]
    if eksik:
        raise SystemExit(f"{modul}: cevap anahtarında karşılığı olmayan sorular: {eksik}")

    karistirilabilir = [s for s in sorular if not sayisal_kume(s.metinler)]
    harfler = ["a", "b", "c", "d"]
    hedef = hedef_dagilim(len(karistirilabilir), harfler, rng)

    esleme = {}  # soru numarası -> {eski harf: yeni harf}
    for soru, yeni_dogru in zip(karistirilabilir, hedef):
        n = len(soru.metinler)
        harf_listesi = [chr(ord("a") + k) for k in range(n)]
        eski_dogru = dogrular[soru.numara]
        if yeni_dogru not in harf_listesi:
            yeni_dogru = harf_listesi[-1]
        # doğru şıkkı hedef konuma koy, kalanları karıştır
        digerleri = [h for h in harf_listesi if h != eski_dogru]
        rng.shuffle(digerleri)
        yeni_sira = []
        it = iter(digerleri)
        for h in harf_listesi:
            yeni_sira.append(eski_dogru if h == yeni_dogru else next(it))
        # yeni_sira[k] = k. konuma gelecek ESKİ harf
        esleme[soru.numara] = {
            eski: chr(ord("a") + k) for k, eski in enumerate(yeni_sira)
        }
        yeni_metinler = [soru.metinler[ord(e) - ord("a")] for e in yeni_sira]
        soru.metinler = yeni_metinler
        dogrular[soru.numara] = yeni_dogru

    # --- alıştırma dosyasını yeniden yaz (sondan başa, satır indisleri kaysın diye)
    for soru in sorted(sorular, key=lambda s: s.satir_araligi[0], reverse=True):
        bas, bit = soru.satir_araligi
        yeni = []
        for k, (onek, metin) in enumerate(zip(soru.onekler, soru.metinler)):
            sondaki = k < len(soru.metinler) - 1 or soru.son_devam
            yeni.append(f"{onek} {metin}" + ("\\" if sondaki else ""))
        a_satir[bas:bit] = yeni

    # --- cevap anahtarını yeniden yaz
    def cevap_degistir(m):
        numara = int(m.group(1))
        if numara not in esleme:
            return m.group(0)
        return f"**{numara}. Doğru cevap: {dogrular[numara]})**"

    yeni_c = []
    for satir in c_metin.split("\n"):
        m = CEVAP_BAS.match(satir)
        if m:
            numara = int(m.group(1))
            govde = satir[m.end():]
            if numara in esleme:
                harita = esleme[numara]
                govde = re.sub(
                    r"\(([a-e])\)",
                    lambda mm: f"({harita.get(mm.group(1), mm.group(1))})",
                    govde,
                )
            satir = CEVAP_BAS.sub(cevap_degistir, satir[:m.end()]) + govde
        yeni_c.append(satir)

    if uygula:
        a_yol.write_text("\n".join(a_satir), encoding="utf-8")
        c_yol.write_text("\n".join(yeni_c), encoding="utf-8")

    return Counter(dogrular[s.numara] for s in sorular), len(sorular), len(karistirilabilir)


def main():
    uygula = "--uygula" in sys.argv
    rng = random.Random(TOHUM)
    toplam = Counter()
    print(f"{'modül':9}{'N':>4}{'karıştırılan':>14}   dağılım (a/b/c/d)")
    for modul in MODULLER:
        sayac, n, k = modulu_isle(modul, rng, uygula)
        toplam.update(sayac)
        print(f"{modul:9}{n:4}{k:14}   " + "/".join(str(sayac[h]) for h in "abcd"))
    N = sum(toplam.values())
    beklenen = N / 4
    ki2 = sum((toplam[h] - beklenen) ** 2 / beklenen for h in "abcd")
    print(f"\nTOPLAM N={N}  a={toplam['a']} b={toplam['b']} c={toplam['c']} d={toplam['d']}")
    print(f"chi-kare = {ki2:.1f} (df=3; 0.05 düzeyinde kritik değer 7.8)")
    if not uygula:
        print("\n(deneme çalıştırması — dosyalar değiştirilmedi; --uygula ile yazar)")


if __name__ == "__main__":
    main()
