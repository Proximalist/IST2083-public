# IST2083 — ders belgelerinin ihtiyaç duyduğu R paketleri
#
# İki işi vardır:
#   1. Yeni bir ortamda (yerel makine, Codespaces, CI) paketleri kurar.
#   2. renv.lock üretilirken hangi paketlerin kilitleneceğini belirler.
#
# Kullanım:  Rscript scripts/paketler.R

# --- Denetimden geçmiş modüllerin (bkz. _quarto.yml render listesi) ve izlencenin ihtiyaçları ---
temel <- c(
  "knitr", "rmarkdown",   # render altyapısı
  "here",                 # proje köküne göre dosya yolu
  "ggplot2", "dplyr",     # görselleştirme ve veri işleme
  "tidyr",                # 05. modülde pivot_longer()/pivot_wider()
  "readr",                # 05. modülde read_csv() ile veri okuma
  "scales",               # 03. modülde eksen biçimlendirme (label_dollar)
  "gapminder",            # 01., 03., 05., 10. ve 11. modülde kullanılan sürekli veri seti
  "mosaicData",           # 03. modülde Simpson paradoksu örneği (SAT verisi)
  "ggrepel",              # 03. modülde Gamson grafiğinde parti etiketleme
  "patchwork",            # 03. modülde Minard grafiğinde iki paneli birleştirme
  "readxl", "writexl",    # Excel okuma/yazma
  "gtsummary",            # 04. ve 14. modülde yayına hazır tablo (tbl_regression)
  "mdsr",                 # 11. modülde SAT_2010 veri seti (öğretmen maaşı - SAT puanı örneği)
  "broom",                # 11. modülde tidy()/glance() ile düzenli regresyon çıktısı; 14. modülde multinom/polr için tidy()
  "performance",          # 11. modülde check_model() ile görsel varsayım denetimi
  "fst",                  # 12. modülde taiwan_real_estate.fst okuma
  "car",                  # 12. modülde vif() ile çoklu doğrusallık denetimi
  "modelsummary",         # 12. modülde makale formatında çoklu model tablosu
  "haven",                # 13. modülde read_dta() ile Stata verisi okuma
  "forcats",              # 13. modülde fct_rev() ile ölçek yönü çevirme
  "nnet",                 # 14. modülde multinom() ile çoklu lojistik regresyon
  "MASS",                 # 14. modülde polr() ile sıralı lojistik regresyon
  "tidyverse"             # 13. ve 14. modülde toplu yükleme
)

# --- Henüz denetlenmemiş modüllerin ek ihtiyaçları --------------------
# 14. modül denetimiyle birlikte depodaki tüm modüller (01-14) denetimden
# geçmiştir; aşağıdakiler eksik/gelecek bir modülün ihtiyacı değil,
# 14. modülün ders notunda yalnızca ILLUSTRATIF (```r, hiç çalıştırılmayan)
# kod bloklarında gösterilen, öğrencinin isterse kendi başına deneyebileceği
# ileri düzey araçlardır — bu yüzden render'ı hiç etkilemezler ve "temel"e
# taşınmaları gerekmez:
#   - ggeffects: multinom() modelinin marjinal etkilerini çizgi grafiğiyle
#     göstermek için (bkz. "İleri Düzey: Marjinal Etkileri Görselleştirmek")
#   - brant: polr()'un orantılı odds varsayımını sınamak için
#     (bkz. "Orantılı odds varsayımı her zaman kontrol edilmelidir")
#
# Not: 14. modülün ilk (denetlenmemiş) taslağında burada duran "AER",
# "coefplot", "pscl", "mlogit" paketleri, taslağın gerçekte kurduğu
# modele (ikili lojistik regresyonun bir tekrarı) değil, hiç
# kullanılmayan sayım/seçim modellerine aitti; 14. modül denetiminde
# kaldırıldı (bkz. docs/belge-standardi.md).
ek <- c(
  "lubridate",
  "kableExtra", "janitor",
  "nycflights13", "NHANES", "macleish", "fec16",
  "ggmosaic", "ggthemes", "wesanderson",
  "ggeffects", "brant"
)

# Ayna seçimi: ortam zaten geçerli bir ayna ayarlamışsa (GitHub Actions'ta
# setup-r `use-public-rspm: true` ile RSPM'i ayarlar ve oradan ikili paket
# gelir, kaynaktan derleme yapılmaz) onu kullanırız; ayarlanmamışsa
# cloud.r-project.org'a düşeriz. install.packages() çağrısına repos'un
# DAİMA açıkça verilmesi gerekir (bkz. docs/belge-standardi.md §13).
ayna <- function() {
  mevcut <- getOption("repos")[["CRAN"]]
  if (is.null(mevcut) || is.na(mevcut) || mevcut %in% c("", "@CRAN@")) {
    "https://cloud.r-project.org"
  } else {
    mevcut
  }
}

kur <- function(paketler) {
  eksik <- paketler[!paketler %in% rownames(installed.packages())]
  if (length(eksik) == 0) {
    message("Tüm paketler zaten kurulu.")
  } else {
    message("Kurulacak: ", paste(eksik, collapse = ", "))
    install.packages(eksik, repos = ayna())
  }
}

args <- commandArgs(trailingOnly = TRUE)
if (length(args) > 0 && args[1] == "hepsi") kur(c(temel, ek)) else kur(temel)
