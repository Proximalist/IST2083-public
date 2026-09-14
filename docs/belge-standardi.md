# IST2083 — Belge Standardı

Bu belge, depodaki tüm ders belgelerinin **dosya adlandırması** ve **YAML
başlığı** için tek geçerli kuralı tanımlar. Yeni bir belge üretirken bu
sayfaya bakılır; istisna yapılmaz.

## 0. Oturum mu, modül mü?

Depo iki farklı numaralandırma kullanır ve bunlar **kasten** birbirinden
ayrıdır:

- **Oturum**, takvimdeki bir ders günüdür (1. oturum = 1 Ekim). Yalnızca
  izlencede geçer. Dönem içinde tatil, telafi veya iptal olduğunda
  değişebilir.
- **Modül**, bir konu paketidir (`05_modul/` = veri işleme). Depodaki
  klasör ve dosya adları modül numarasını taşır ve bu numara dönem
  boyunca **değişmez**.

İkisi bire bir eşleşmez: 3. oturum iki modülü birden işler
(`05_modul/` + `15_modul/`), 10. modül ise iki oturuma yayılır (8. ve
9. oturum). Modül numarası oturum sırasını göstermez: `15_modul/`
3. oturumda, `14_modul/` 11. oturumda işlenir. Hangi oturumda hangi modülün işleneceği **yalnızca
izlencedeki tabloda** tanımlıdır; başka hiçbir yerde tekrarlanmaz ki
çelişme ihtimali olmasın.

Bu yüzden belge başlıkları "5. Hafta" demez, **"Modül 05"** der.
Ders notlarının **metni içinde** ise oturum numarası kullanılır
("3. oturumda `dplyr` göreceğiz"), çünkü öğrenci için anlamlı olan
takvimdir.

## 1. Klasör adları

```
NN_modul/          NN = 01 … 15, daima iki haneli
```

İki hane zorunludur: aksi hâlde hem `ls` hem GitHub dosya listesi
`10, 11, 12, 13, 14, 1, 2, 3 …` sırasıyla dizer ve klasörler karışır.

## 2. Dosya adları

```
NN_modul_<tur>[_<ek>].qmd
```

`<tur>` sabit bir sözlükten seçilir:

| `<tur>` | Belge |
|---|---|
| `ders` | Modülün ders notu (ana içerik) |
| `sunum` | Derste yansıtılan revealjs sunumu |
| `lab` | Derste birlikte yapılan rehberli uygulama |
| `alistirmalar` | Çoktan seçmeli alıştırma seti |
| `cevap_anahtari` | Alıştırmaların gerekçeli cevapları |

`<ek>` yalnızca **aynı türden birden fazla belge** varsa kullanılır:
`06_modul_ders_olasilik.qmd`, `14_modul_alistirmalar_1.qmd`.

Kurallar:

- Dosya adı klasör adını tekrar eder (`02_modul/02_modul_ders.qmd`).
  Gereksiz görünür ama gereklidir: RStudio sekme çubuğu yalnızca dosya
  adını gösterir; üç modülün `ders.qmd` dosyası açıkken hangisinin
  hangisi olduğu ayırt edilemez.
- Türkçe karakter, boşluk ve büyük harf **kullanılmaz**. Dosya adları
  yalnızca `a-z`, `0-9` ve `_` içerir. Gerekçe: macOS'un dosya
  adlarını Unicode olarak normalize etme biçimi Linux'unkinden farklıdır;
  `ı`, `ğ`, `ü` içeren yollar Codespaces ve CI'da sessizce kırılabilir.
- Uzantı daima `.qmd`'dir. `.Rmd` kullanılmaz.

## 3. YAML başlığı

Tüm belgeler `lang`'e kadar **birebir aynıdır**; yalnızca `title`,
isteğe bağlı `subtitle` ve `format` bloğu değişir.

### Ders notu, lab, alıştırma, cevap anahtarı (PDF)

```yaml
---
title: "Modül NN: Konu Başlığı"
subtitle: "yalnızca lab/alıştırma/cevap anahtarı için"
author: "Prof. Dr. Hakan Mehmetcik"
date: "`r Sys.Date()`"
lang: tr
format: pdf
editor: visual
execute:
  echo: true
  warning: true
  message: false
  cache: false
df-print: kable
---
```

### Sunum (revealjs)

```yaml
---
title: "Modül NN: Konu Başlığı"
author: "Prof. Dr. Hakan Mehmetcik"
date: "`r Sys.Date()`"
lang: tr
format:
  revealjs:
    theme: simple
    slide-number: true
    toc: true
    toc-depth: 2
    incremental: true
    code-overflow: scroll
    code-line-numbers: false
    transition: fade
    math: mathjax
editor: visual
execute:
  echo: true
  warning: false
  message: false
  cache: false
df-print: kable
---
```

### Alanların gerekçesi

- **`date`** — daima `Sys.Date()` çağrısıyla verilir; sabit tarih yazılmaz. Sabit tarihler bir
  önceki dönemden kalır ve belgenin bayat olduğunu gizler.
- `lang: tr` — Quarto'nun otomatik ürettiği etiketleri Türkçeleştirir
  ("Figure" → "Şekil", "Contents" → "İçindekiler") ve LaTeX'in Türkçe
  heceleme kurallarını devreye sokar.
- `warning: true` (ders notunda) — R'ın uyarıları öğretici olduğu için
  öğrenciye gösterilir. Sunumda `false`, çünkü slayt düzenini bozar.
- `message: false` — `library()` çağrılarının paket yükleme mesajları
  gösterilmez.
- `cache: false` — önbellek, veri değiştiğinde sessizce eski sonuç
  gösterebilir; ders belgelerinde bu risk alınmaz.
- **`output: asis` kullanılmaz.** Bu bir öbek seçeneğidir; `execute:`
  altında genel olarak verildiğinde `df-print: kable` çıktısını ham
  LaTeX/HTML olarak basar.

## 4. Render çıktıları

Render edilmiş `.pdf` / `.html` belgeler ve revealjs sunumlarının
`*_files/` klasörleri **depoda tutulur.** Gerekçe: öğrenci kaynak
dosyayı kendi bilgisayarında render edemediğinde (paket eksik, LaTeX
kurulu değil, Codespaces kotası dolmuş) hazır belgeye erişebilmelidir.

Bunun bir bedeli vardır ve kural budur:

> **Bir `.qmd` dosyasını düzenlediyseniz, aynı commit'te onu yeniden
> render edip çıktısını da ekleyin.** Unutulursa depoda içerikle
> uyuşmayan bir belge kalır ve öğrenci yanlış sürümü okur.

Bu kural, CI kurulana kadar elle uygulanır. CI kurulduğunda render
otomatikleşir ve bu madde yeniden değerlendirilir.

İstisnalar: `figure-pdf/` ve `figure-latex/` ara figür klasörleri
izlenmez (nihai PDF'e zaten gömülürler). `_calisma/`, `sinav/` ve
`notlar/` klasörleri hiçbir koşulda izlenmez.

## 5. Görsel yolları

Görseller belgenin **kendi klasöründeki** `images/` altında tutulur
(`02_modul/images/...`) ve belgede `images/dosya.png` biçiminde,
göreli olarak çağrılır. RStudio belgeleri kendi klasörlerine göre
render eder; proje köküne göre yazılan yollar (`../images/...`)
çalışmaz.

Görsel dosya adlarında Türkçe karakter kullanılmaz (bkz. §2).

Kod ile üretilen görsellerin kaynak betiği `scripts/` altında,
görselle aynı adı taşıyacak biçimde tutulur ve proje kökünden
çalıştırılır:

```
python3 scripts/veri-yapilari-tipolojisi.py
```

Böylece görsel yeniden üretilebilir kalır; PNG'yi elden düzeltmek
yerine betik düzenlenir.

## 6. Yeni bir modül denetimden geçtiğinde

Modül elden geçirildikten sonra iki dosyada birer satır güncellenir:

1. **`_quarto.yml`** — o modülün satırındaki `#` kaldırılır, böylece
   `quarto render` ve CI onu da render etmeye başlar.
2. **`scripts/paketler.R`** — modülün kullandığı paketler `ek`
   vektöründen `temel` vektörüne taşınır. **CI iş akışında ayrıca bir
   liste tutulmaz:** `render-dogrulama.yml` doğrudan
   `Rscript scripts/paketler.R` çağırır, yani `temel` vektörü tek
   kaynaktır.

Bu iki adım atlanırsa modül CI tarafından hiç sınanmaz ve Linux'ta
kırık olduğu fark edilmez.

**Düzeltme geçmişi:** 13 Eylül 2026 denetiminde, CI iş akışının kendi
elle yazılmış paket listesini taşıdığı ve bu listenin 11–14. modüllerin
paketlerini (`mdsr`, `broom`, `performance`, `fst`, `car`,
`modelsummary`, `haven`, `forcats`, `nnet`, `MASS`) hiç almadığı
bulundu — `_quarto.yml` bu modülleri render listesine aldığı hâlde.
Aynı listenin iki yerde tutulması bu hatayı kaçınılmaz kılıyordu; CI
adımı `paketler.R`'ye bağlanarak ikinci kaynak kaldırıldı.

## 7. CI profili

`_quarto-ci.yml`, yalnızca GitHub Actions'ta (`QUARTO_PROFILE=ci`)
devreye giren ayarları taşır. Yerel render'ı etkilemez. Şu an tek
içeriği, CI'da otomatik LaTeX paket kurulumunu kapatmaktır — runner'daki
TinyTeX kurulumu CTAN aynalarından yeni olabildiği için `tlmgr` hata
veriyor ve render'ı düşürüyordu.

CI'ın ürettiği PDF'ler **geçici artefakttır**, öğrenciye gitmez.
Öğrenciye giden belgeler sizin makinenizde render edilip commit edilir
(bkz. §4).

## 8. Öğrenciye giden metinde yazar notu bırakmayın

Belgeler herkese açık bir depoda ve öğrenci PDF'i doğrudan okuyor.
Aşağıdakiler render edilen metinde **asla** görünmemelidir:

- kendinize bıraktığınız yapılacak notları ("şu dosyayı indirip
  `images/...` olarak kaydedin", "aşağıdaki satırı yorumdan çıkarın")
- `TODO`, `FIXME`, `XXX` gibi işaretler
- "yakında eklenecek", "denetim tamamlandığında yazılacak" türü
  eksiklik beyanları

Bunlar için `_calisma/` klasörü var; orası izlenmez ve öğrenciye
gitmez. Görsel kaynak künyesi ise metinde kalır ama yalnızca
**künye** olarak: eser adı, sanatçı/kurum, yıl, telif durumu.

## 9. Grafik içeren PDF belgeleri

R grafiklerinde Türkçe karakter kullanan PDF belgelerine knitr aygıtı
olarak `cairo_pdf` verin:

```yaml
knitr:
  opts_chunk:
    dev: "cairo_pdf"
```

R'ın varsayılan `pdf()` aygıtı tek baytlık kodlamaya düşer ve grafik
başlıklarındaki `ş`, `ı`, `ğ` harflerini sessizce düşürür
(`mbcsToSbcs` uyarısı). Sunumlarda (PNG çıktı) gerek yoktur.

## 10. `date` alanı: R kodu içermeyen belgede `` `r Sys.Date()` `` kullanmayın

Bir belgede **hiç** çalıştırılabilir R öbeği yoksa (çoğu `cevap_anahtari`
belgesi böyledir), Quarto o belge için knitr motorunu hiç devreye
sokmaz ve YAML'daki `` `r Sys.Date()` `` ifadesi hiç değerlendirilmeden
pandoc'a düz metin olarak geçer; pandoc bunu bir tarih olarak
ayrıştıramayıp sessizce **"Invalid Date"** basar. Render hata vermediği
için bu, PDF'e bakılmadan fark edilmez.

Kural: hiç R öbeği içermeyen belgelerde tarih alanı için

```yaml
date: today
```

yazılır — bu, R'a ihtiyaç duymadan Quarto'nun kendisi tarafından
çözülür. En az bir R öbeği içeren belgelerde (`ders`, `lab`,
`alistirmalar`) `` `r Sys.Date()` `` kullanmaya devam edilir, çünkü
knitr zaten çalışıyor olacaktır.

**Düzeltme geçmişi:** `01_modul/01_modul_cevap_anahtari.qmd` ve
`02_modul/02_modul_cevap_anahtari.qmd` bu hatayı taşıyordu (PDF'lerinde
"Invalid Date" yazıyordu); 03. modül denetimi sırasında fark edildi,
04. modül denetimiyle birlikte düzeltildi — her iki dosyanın `date`
alanı `date: today` olarak güncellendi ve PDF'leri yeniden render edildi.
Aynı hata `09_modul/09_modul_alistirmalar.qmd` ve
`09_modul/09_modul_cevap_anahtari.qmd` dosyalarında da (hiç R öbeği
içermedikleri hâlde `` `r Sys.Date()` `` kullanıyorlardı) bulundu; 10.
modül denetimi sırasında fark edildi ve aynı şekilde `date: today`
olarak düzeltildi.

## 11. Düz metinde matematik sembolü kullanmayın — `$...$` içine alın

`$...$` **dışındaki** düz metinde tek başına bir Unicode matematik
sembolü (`≈`, `≤`, `≥` gibi) yazıldığında, xelatex'in ana metin
fontu (Latin Modern Roman) bu karakteri içermeyebilir; render **hata
vermez**, sembol PDF'te sessizce **boş bırakılır** ("çarpıklık ≈ 0"
yazıp "çarpıklık   0" olarak basılır). Ok işaretleri (`→`) bu sorunu
yaşamaz — yalnızca matematik sembolleri etkilenir.

Kural: metinde bir matematik sembolü geçiyorsa, LaTeX matematik
komutuyla ve `$...$` içinde yazılır: `≈` yerine `$\approx$`, `≤`
yerine `$\le$`. Emin değilseniz Türkçe kelimeyle yazmak ("yaklaşık")
her zaman güvenlidir.

**Bilinen etkilenmiş belgeler:** `06_modul/06_modul_ders_olasilik.qmd`
(`≈` üç örnekte düz metin/denklem karışımı içinde) ve
`08_modul/08_modul_ders.qmd` (`≈`, `≤`, `μ`, `σ` `$...$` içinde ama
unicode-math yüklenmeden kullanılmış) bu deseni taşıyor; 04. modül
denetimi sırasında fark edildi, düzeltilmedi çünkü ikisi de kapsam
dışı (henüz denetlenmemiş modüller). Bu iki dosya kendi denetim
sırası geldiğinde gözden geçirilmeli.

**10. modül bulgusu:** `10_modul/10_modul_ders.qmd`, 06/08. modüllerden
çok daha ağır bir biçimde bu deseni taşıyordu — `α`, `μ`, `≤`, `≥`,
`≠` ve alt simge Unicode rakamları (`₀`, `₁`) toplam 58 kez `$...$`
dışında geçiyordu. 10. modül denetimi sırasında tamamı `$...$` içine
alınarak düzeltildi; ayrıca aynı dosyadaki bir tablo hücresinde
"H0H_0H0" biçiminde üçlü bir metin bozulması ve kapsam dışı bir
regresyon örneği (bkz. izlence — regresyon Modül 11-12'nin konusu)
tespit edilip kaldırıldı.

**11. modül bulgusu:** `11_modul_ders.qmd`'nin taslak sürümü, model
denklemini tanımlayan madde imli listede `β`, `ϵ` sembollerini
(`β0​: Kesme noktası...` gibi) `$...$` dışında düz metin olarak
kullanıyordu — aynı desenin 10. modüldeki kadar yaygın olmayan ama
aynı kök nedene sahip bir tekrarı. 11. modül denetimi sırasında
tamamı `$\beta_0$`, `$\beta_1$`, `$\epsilon$` biçiminde matematik
moduna alınarak düzeltildi. Bu desen yeni bir modül taslağı her
teslim alındığında (bkz. hazırlık aşamasındaki 12. modül) ilk kontrol
maddesi olmalıdır — kaynağı büyük olasılıkla kelime işlemciden veya
bir sohbet asistanından kopyala-yapıştır yoluyla gelen matematik
gösterimidir.

## 12. Terminoloji standardı: "Residüel" değil "Artık"

Regresyon konusunda R'ın `summary()` çıktısındaki `Residuals` etiketi
İngilizce kalır (R'ın kendi çıktısı değiştirilemez), ancak öğrenciye
yönelik **açıklama metninde** bu kavramın Türkçe karşılığı olarak
Türkçe istatistik literatüründeki yerleşik terim **"artık"** kullanılır
— "residüel" değil.

Kural:

- Metinde: "artık", "artığı", "artığın", "artıklar" (Türkçe ünlü
  uyumu ve ünsüz yumuşaması gözetilerek çekimlenir).
- R çıktısındaki `Residuals` etiketine ilk değinildiğinde yanına
  parantez içinde Türkçe karşılığı eklenir: "**Residuals** (artıklar)".
- R kod içindeki değişken adları (`residuel`, `resid_df` vb.) bu
  kuraldan **muaftır** — yalnızca öğrenciye görünen düz metin ve
  yorumlar etkilenir, kod bozulmaz.

**Düzeltme geçmişi:** `11_modul/` dosyalarının ilk taslağı "residüel"
kullanıyordu; 11. modülün ikinci iç değerlendirmesi sırasında fark
edildi ve ders notu, lab, sunum, alıştırmalar ve cevap anahtarının
tamamında "artık"a çevrildi. Regresyon konusuna devam eden her modül
(12. modül ve sonrası) bu terimi kullanmalıdır.

## 13. `scripts/paketler.R`: `install.packages()` çağrısına CRAN aynası verilmeden non-interactive çalıştırılamaz

`Rscript scripts/paketler.R` komut satırından (non-interactive) çalıştırıldığında, R'ın interaktif ayna seçim penceresi açılamaz ve `install.packages()` "trying to use CRAN without setting a mirror" hatasıyla durur. RStudio içinden çalıştırıldığında bu sorun görünmez, çünkü RStudio zaten varsayılan bir ayna ayarlamıştır — bu yüzden hata yalnızca komut satırından/CI'dan çalıştırıldığında ortaya çıkar.

Kural: betikteki tek `install.packages()` çağrısı daima açık bir `repos` argümanıyla yazılır:

```r
install.packages(eksik, repos = "https://cloud.r-project.org")
```

**Düzeltme geçmişi:** 12. modül denetimi sırasında `car` paketi kurulurken fark edildi ve düzeltildi.

## 14. Veri dosyaları UTF-8 ve BOM'suz olmalı

`data/` altındaki `.csv` dosyaları **ham hâlleriyle** (genelde bir web sitesinden kopyala-yapıştır veya dışa aktarma yoluyla) depoya girer ve kodlamaları kontrol edilmeden bırakılırsa iki sessiz hata ortaya çıkabilir:

1. **Latin-1/ISO-8859 kodlama:** Dosya UTF-8 değilse, `readr::read_csv()` veriyi okur ama içindeki bazı baytlar geçersiz UTF-8 karakter üretir. Bu, veri okunurken hata vermez; yalnızca o veri `kable()` gibi bir fonksiyonla yazdırılmaya çalışıldığında ("input string N is invalid UTF-8") render'ı düşürür — hatanın kaynağı ilk bakışta anlaşılmaz çünkü suçlu satır veri setinin ortasında bir yerdedir.
2. **UTF-8 BOM (Byte Order Mark):** Dosyanın başındaki 3 baytlık (`EF BB BF`) görünmez işaret, base R'ın `read.csv()`'si tarafından temizlenmez; ilk sütun adının önüne yapışır (`Species` → `ï»¿Species`). Bu da veri okunurken hata vermez; yalnızca o sütuna `$isim` ile erişilmeye çalışıldığında sessizce `NULL` döner.

Kural: yeni bir veri dosyası depoya eklenmeden önce kodlaması doğrulanır:

```bash
file data/yenidosya.csv   # "UTF-8 Unicode text" demeli, "ISO-8859" veya "with BOM" değil
```

Sorunlu ise Python ile düzeltilir (R'da bu tür ham bayt işlemleri daha zahmetlidir):

```python
raw = open("data/dosya.csv", "rb").read()
raw = raw.replace(b"\xef\xbb\xbf", b"", 1)          # BOM varsa temizle
text = raw.decode("latin-1")                          # ya da doğru kaynak kodlama
open("data/dosya.csv", "w", encoding="utf-8", newline="").write(text)
```

**Düzeltme geçmişi:** `data/worldrecord.csv` (ISO-8859, ülke adı önünde 375 adet NBSP artığı) ve `data/Fish.csv` (BOM'lu UTF-8) 12. modül render denemesi sırasında bulundu ve düzeltildi. Bu, 04. modüldeki Titanic verisinde de yaşanan sorunun (BOM + satır sonu temizliği) aynı sınıfının bu kez yazıya geçirilmiş hâlidir.

## 15. Metinde kontrol karakteri (görünmez bayt) olmamalı

`11_modul/11_modul_ders.qmd`'de `$r \approx 0.68$` yazması gereken bir yerde `$r \x07pprox 0.68$` bulundu — yani `\a` iki karakter (ters eğik çizgi + a) olarak değil, tek bir **BEL kontrol karakteri** (0x07) olarak kaydedilmişti. xelatex bunu "Text line contains an invalid character" hatasıyla reddediyor.

Kaynağı muhtemelen bir metin işleme betiğinde (Python, vb.) `"\approx"` gibi bir dizginin **ham dizgi (raw string, `r"..."`) olmadan** yazılması: Python'da `\a` alarm/bell karakteri için ayrılmış bir kaçış dizisidir ve sessizce 0x07 baytına dönüşür — ne yazma ne de commit sırasında bir hata verir, yalnızca xelatex bu baytı gördüğünde patlar.

Kural: Belge içeriğini bir betikle (özellikle Python) toplu değiştirirken LaTeX komutu içeren dizgiler (`\alpha`, `\approx`, `\beta`, `\epsilon`, `\to`, `\sim` vb.) **daima ham dizgi olarak** yazılır (`r"\approx"` veya `"\\approx"`), asla düz dizgi (`"\approx"`) olarak değil.

**Düzeltme geçmişi:** 12. modül render denemesi modül 11'in bu hatasını ortaya çıkardı (kaynağı önceki bir oturumdaki metin düzenlemesi); tüm depo genelinde başka bir kontrol karakteri kalıntısı olup olmadığı tarandı, bulunmadı.

## 16. Veri dosyaları yalnızca `data/` altında tutulur — modül klasörüne kopyalanmaz

`data/`, depodaki tüm ham veri setleri için **tek kaynaktır**; her modül
`here("data", "dosya.uzanti")` ile buraya başvurur. Bir modül klasörünün
(`NN_modul/`) içine ayrıca bir veri kopyası konmaz — konursa iki risk
birden doğar: (1) kopya, kaynak dosya güncellendiğinde **fark edilmeden
bayatlar**; (2) hiçbir kod tarafından okunmadığı için depoda sessizce
şişkinlik birikir.

**14. modül bulgusu:** `14_modul/` klasöründe `csvdata.csv`,
`csvdata.xlsx`, `simd2020.dta`, `simd2020.xlsx` adlarıyla toplam ~9,7 MB
veri dosyası bulundu. `csvdata.csv`'nin `data/simd2020.csv` ile **bayt
bayt aynı** olduğu doğrulandı; diğerleri aynı verinin yinelenen
kopyalarıydı. Hiçbiri hiçbir `.qmd` tarafından okunmuyordu — modülün
kendi kodu zaten doğru şekilde `here("data", "simd2020.csv")`'ye işaret
ediyordu. 14. modülün konusu değiştirilirken (bkz. §17) bu veri seti
tamamen kapsam dışı kaldığından hem yerel kopyalar hem de
`data/simd2020.csv` depodan kaldırıldı.

## 17. Bir modülün izlencedeki durumu değişebilir — belgeler bu durumla senkron tutulmalı

Bir modülün izlencede karşılığı olup olmadığı (sınav kapsamında mı,
kapsam dışı isteğe bağlı bir zenginleştirme mi) **sabit bir gerçek
değildir**; öğretim üyesinin kararıyla dönem içinde değişebilir.
Modülün kendi metninde bu duruma dair bir ifade varsa (ör. bir
`callout` bloğuyla "sınav kapsamı dışındadır" ya da "final kapsamına
girer" denmesi), bu ifade **izlenceyle her zaman tutarlı olmalıdır** —
ve izlence değiştiğinde modülün metni de **aynı commit ile**
güncellenmelidir. Ayrıca bu ifade **önceki modülün** metniyle de
çelişmemelidir: bir önceki modül "dönemin son yeni konusu" diyorsa ve
yeni bir modül aynı oturuma ekleniyorsa, o ifade de güncellenmelidir —
aksi hâlde öğrenci iki belge arasında çelişen bir mesaj alır.

**14. modül bulgusu:** Modülün ilk taslağı ("Ek Uygulama" başlığıyla)
izlenceye hiç işlenmemişti. Taslağın kendisi de 13. modülle (aynı
`scottish.dta` veri seti, aynı `RefvoteDum` bağımlı değişkeni üzerine
kurulu bir ikili lojistik regresyon) **içerik olarak örtüşüyordu** —
pedagojik katma değeri yoktu. Ancak taslağın `library()` çağrılarında
yüklenip hiç kullanılmayan paketler ve zaten hazırlanmış `pid1` (3
kategorili, nominal) ile `trust` (sıralı) değişkenleri, yarım kalmış
gerçek bir niyete işaret ediyordu: ikili lojistik regresyonun **çoklu
(multinomial)** ve **sıralı (ordinal)** uzantıları — 13. modülün
tekrarı değil, doğal ve örtüşmeyen bir devamı. İçerik bu yönde yeniden
yazılırken modül henüz izlenceye işlenmemişti, bu yüzden belgeler
başlangıçta "sınav kapsamı dışı" olarak işaretlendi.

Belgeler teslim edildikten hemen sonra öğretim üyesi izlenceyi
güncelleyerek 14. modülü 11. oturuma (13. modülle birlikte) ekledi —
yani modül **sınav kapsamına girdi**. Bu, ilk teslimattaki "kapsam
dışı" ifadesini yanlışa düşürdü; hem 14. modülün beş belgesindeki hem
de 13. modülün "dönemin son yeni konusu" cümlesi ve final-kapsamı
özet tablosundaki ilgili ifadeler bu değişikliği yansıtacak şekilde
aynı oturumda güncellendi.

**Genel ders:** (1) Yarım kalmış bir taslakta **kullanılmayan ama
yüklenmiş paketler**, yazarın asıl niyetine dair ipucu taşıyabilir —
denetim sırasında çalışmayan/kullanılmayan `library()` çağrılarını da
okumak, modülün "gerçekte ne olması gerektiği" sorusuna yanıt
verebilir. (2) İzlence ile modül metinleri arasındaki "kapsam"
tutarlılığı **tek seferlik bir kontrol değil**, izlence her
değiştiğinde yeniden yapılması gereken bir kontroldür.

## 18. `library(MASS)`, `dplyr::select()`'i sessizce maskeler

`MASS` paketi de (adım seçimi fonksiyonları için) kendi `select()`
fonksiyonunu tanımlar. `library(MASS)`, `library(tidyverse)`'den
(dolayısıyla `dplyr`'den) **sonra** çalıştırılırsa, R'ın arama yolunda
`MASS::select` `dplyr::select`'in **önüne** geçer ve o noktadan sonra
düz `select(...)` çağrıları sessizce `MASS::select`'e yönlenir. Bu bir
uyarı ile bildirilir (`The following object is masked from
'package:dplyr': select`), ama knitr/quarto render'ında bu uyarı
konsola karışıp kolayca gözden kaçar; hata ancak `select()`
gerçekten çağrıldığında ("unused arguments") ortaya çıkar — ki bu,
kütüphane satırından çok sonra, belgenin ortasında bir yerde
olabilir.

Kural: `MASS` paketiyle aynı belgede `dplyr::select()` kullanılıyorsa,
çağrı **daima açıkça isim uzayıyla** (`dplyr::select(...)`) yazılır;
`library(MASS)`'ı `library(tidyverse)`'den önce yüklemek de riski
azaltır ama tek başına yeterli değildir (aynı belgede ileride tekrar
`library(MASS)` çağrılabilir).

**Düzeltme geçmişi:** `14_modul/14_modul_ders.qmd`'de çoklu lojistik
regresyon örneğindeki `broom::tidy(model_multi, ...) %>%
select(y.level, term, ...)` satırı, öğretim üyesinin ilk render
denemesinde tam olarak bu hatayla ("unused arguments (y.level, term,
estimate, p.value, conf.low, conf.high)") düştü; `dplyr::select(...)`
olarak düzeltildi.


## 19. Yeni bir kural yazıldığında depo TAMAMI o kurala göre taranır

§10 ve §11'in düzeltme geçmişleri aynı deseni gösteriyor: kural bir
modül denetiminde keşfediliyor, o modülde düzeltiliyor, yazıya
geçiriliyor — ama **kuralın geçmişe dönük uygulanması yapılmıyor.**
Sonraki modül denetiminde aynı hata başka bir dosyada yeniden
keşfediliyor.

13 Eylül 2026 denetimi bunun bedelini ölçtü: §10 (R öbeği içermeyen
belgede `` `r Sys.Date()` ``) kuralı 04. modül denetiminde yazılmış
olmasına rağmen, kural yazıldığı gün altı belge daha aynı hatayı
taşıyordu ve PDF'lerinde **"Invalid Date"** basılıydı —
`01_modul_alistirmalar`, `06_modul_alistirmalar`,
`07_modul_alistirmalar`, `GitHub_Kullanim_Kilavuzu`,
`R-Hizli-Referans`, `R_RStudio_Kurulum_Rehberi`. Son üçü modül
denetimi döngüsünün dışında kaldığı için hiç gözden geçirilmemişti.

Kural: bu belgeye yeni bir madde eklendiğinde, **aynı oturumda** depo
genelinde o desenin taraması yapılır ve bulunan her örnek düzeltilir.
Kök dizindeki üç kılavuz (`R-Hizli-Referans`,
`GitHub_Kullanim_Kilavuzu`, `R_RStudio_Kurulum_Rehberi`) ve `izlence/`
bu taramaya **daima dahildir** — hiçbir modülün denetim kapsamına
girmedikleri için başka türlü hiç kontrol edilmiyorlar.

## 20. İzlence değişince senkronize edilecek dosyalar

§17 izlence–modül tutarlılığını kurala bağlamıştı ama kapsamı "modül
metinleri" olarak yazılmıştı. 13 Eylül denetiminde iki kaçak bulundu:

1. **`README.md`** kendi ders programı tablosunu taşıyor ve izlencenin
   13 Eylül güncellemesini almamıştı: 11. oturum hâlâ "Lojistik
   regresyon ve genel tekrar / `13_modul/`" diyordu, 14. modül hiç
   görünmüyordu. README deponun açılış sayfası — öğrencinin gördüğü
   ilk program odur.
2. **İzlencenin kendi PDF'i** üç gün bayattı (§4 zaten bunu
   gerektiriyordu ama izlence, "modül" olmadığı için render alışkanlığının
   dışında kalmıştı).

Kural: izlence tablosu değiştiğinde **aynı commit'te** güncellenecek
dosyalar şunlardır:

- ilgili modüllerin kapsam ifadelerini taşıyan belgeleri (§17)
- `README.md` ders programı tablosu
- `izlence/…​.pdf` (yeniden render)

Ayrıca izlencede verilen sözler de kontrol edilir: 01. modülün ders
notu "bu iddiayı 11. oturumdaki genel tekrarda sınayacağız" diyordu,
ama 11. oturum 13. + 14. modüle ayrıldığında genel tekrar slotu
kalmamıştı. Bir modül metni **gelecek bir oturuma numarayla söz
veriyorsa**, o oturumun içeriği değiştiğinde söz de gözden geçirilir.

## 21. Çoktan seçmeli şıkların dağılımı

13 Eylül 2026 denetiminde depodaki 269 alıştırma sorusunun **196'sında
(%72.9) doğru cevabın "b" şıkkı** olduğu bulundu (chi-kare = 341,
df = 3; tekdüze beklenti her şık için %25). "d" şıkkı yalnızca 2
soruda doğruydu. En ağır modüller: 07 (%90), 12 (%90), 14 (%88),
09 (%85).

Sınav gruplarında şık sırası karıştırıldığı için **sınavın** geçerliliği
bundan zarar görmez; zarar gören, alıştırmaların izlencede tanımlanan
tek işlevidir — öğrencinin sınav öncesinde kendi durumunu ölçmesi.
Hiçbir şey bilmeden tüm sorulara "b" diyen öğrenci alıştırmalardan
%72.9 alıyordu.

Kaynağı soru yazımındaki bir reflekstir: önce bir bariz çeldirici,
hemen ardından doğru cevap. Tek tek bakıldığında görünmez; 269 soruda
görünür.

Kural: şıklar elle karıştırılmaz, `scripts/sik-permutasyonu.py` ile
karıştırılır. Betik sabit tohumla çalışır, `alistirmalar` ve
`cevap_anahtari` dosyalarını eşzamanlı günceller, cevap anahtarı
metnindeki parantez içi şık atıflarını (`(c) yanlıştır` gibi) yeni
harflere göre yeniden yazar ve tüm şıkları sayı olan soruların sırasını
korur. Yeni bir modülün alıştırmaları yazıldıktan sonra:

```bash
python3 scripts/sik-permutasyonu.py            # denetim, dosya yazmaz
python3 scripts/sik-permutasyonu.py --uygula   # uygular
```

**Not:** Aynı yanlılık sınav soru havuzunda da beklenmelidir; havuz
`_calisma/` dışında tutulduğu için bu denetimin kapsamına girmedi,
ayrıca kontrol edilmelidir.

## 22. Bir modül klasörü tek bir konu paketi olmalıdır

`06_modul/` üç ders belgesi taşıyordu: Quarto ile raporlama,
çıkarımsal istatistiğe giriş, olasılık. İzlence bu klasörü **iki ayrı
oturuma** atıyordu (3. oturum: Quarto; 6. oturum: olasılık) — ama
modülün tek sunum, lab, alıştırma ve cevap anahtarı vardı ve hepsi
olasılık içerikliydi.

Somut sonuç: 22 Ekim'de `06_modul/`'e yönlendirilen öğrenci Quarto için
hiçbir uygulama materyali bulamıyor, bulduğu 20 soruluk alıştırma seti
ise **19 Kasım vizesinin kapsamı dışındaki** olasılık konularını
soruyordu.

13 Eylül denetiminde Quarto içeriği `15_modul/` olarak ayrıldı. Modül
numarasının oturum sırasını göstermemesi §0'a uygundur ve mevcut
numaraların hiçbiri değişmediği için hiçbir bağlantı kırılmadı.

Kural: bir modül klasörü, izlencede **tek bir oturuma** (veya ardışık
oturumlara) karşılık gelen tek bir konu paketi olmalıdır. `<ek>`
mekanizması (§2) aynı konunun birden fazla ders belgesine bölünmesi
içindir, **farklı konuların** aynı klasörde toplanması için değil.

**Açık kalan iş:** `15_modul/` şu an yalnızca ders notu içeriyor;
sunum, lab, alıştırma ve cevap anahtarı henüz üretilmedi.
