# IST2083 — Temel İstatistik ve R ile Veri Analizi

**Marmara Üniversitesi, Siyasal Bilgiler Fakültesi · 2026–2027 Güz**\
Prof. Dr. Hakan Mehmetcik · Perşembe 09:30–12:30 · RTE.S1.138

Bu depo dersin tüm materyallerini barındırır: ders notları, sunumlar, alıştırmalar, cevap anahtarları ve veri setleri.

------------------------------------------------------------------------

## Hızlı başlangıç

Derse hiç R kurmadan başlıyorsanız sırayla:

1.  [**R ve RStudio Kurulum Rehberi**](R_RStudio_Kurulum_Rehberi.pdf) — R, RStudio, Git ve gerekli paketlerin kurulumu.
2.  [**GitHub Kullanım Kılavuzu**](GitHub_Kullanim_Kilavuzu.pdf) — bu deponun bilgisayarınıza indirilmesi ve **her hafta güncellenmesi.**
3.  [**Ders İzlencesi**](izlence/IST2083-izlence-2026-2027-guz.pdf) — konular, tarihler, değerlendirme ve kaynaklar.
4.  [**R Hızlı Referans**](R-Hizli-Referans.pdf) — dönem boyunca öğrenilen R sözdizimini tek yerde toplayan, her hafta büyüyen başvuru belgesi. Bir sözdizimini unuttuğunuzda önce buraya bakın.

Bilgisayarınıza hiçbir şey kurmak istemiyorsanız GitHub Codespaces seçeneği de vardır; kılavuzda anlatılmıştır.

------------------------------------------------------------------------

## Kurulum gerektirmeyen yol: Codespaces

Bilgisayarınıza R ve RStudio kurmak istemiyorsanız, bu depoyu tarayıcıda çalıştırabilirsiniz: yukarıdaki yeşil **Code** düğmesi → **Codespaces** → **Create codespace on main**. R, Quarto ve dersin tüm paketleri hazır gelir. Ayrıntı: `.devcontainer/README.md`.

Kendi bilgisayarınıza kurmayı tercih ederseniz `R_RStudio_Kurulum_Rehberi.pdf` belgesini izleyin.

## Ders programı

| Oturum | Tarih | Konu | Modül |
|---:|----|----|----|
| 1 | 1 Ekim | Giriş: istatistiğin anlamı; R, RStudio, GitHub | `01_modul/` |
| 2 | 8 Ekim | R'da veri türleri, veri yapıları ve temel fonksiyonlar | `02_modul/` |
| — | 15 Ekim | *Ders yapılmaz* | — |
| 3 | 22 Ekim | Veri işleme: `dplyr`, `tidyr`; Quarto ile raporlama | `05_modul/`, `15_modul/` |
| — | 29 Ekim | *Cumhuriyet Bayramı* | — |
| 4 | 5 Kasım | Veri görselleştirme: `ggplot2` | `03_modul/` |
| 5 | 12 Kasım | Tanımlayıcı istatistik | `04_modul/` |
| — | 19 Kasım | **ARA SINAV** — kapsam: 1.–5. oturumlar | — |
| 6 | 26 Kasım | Olasılık, rastgele değişkenler ve dağılımlar | `06_modul/`, `08_modul/` |
| 7 | 3 Aralık | Örnekleme ve Merkezi Limit Teoremi | `07_modul/` |
| T | *Telafi* | Tahmin ve güven aralıkları | `09_modul/` |
| 8 | 10 Aralık | Hipotez testi I: p-değeri ve t-testleri | `10_modul/` |
| 9 | 17 Aralık | Hipotez testi II: ki-kare ve ANOVA | `10_modul/` |
| 10 | 24 Aralık | Korelasyon, basit ve çoklu regresyon | `11_modul/`, `12_modul/` |
| 11 | 31 Aralık | Lojistik regresyon; çoklu ve sıralı lojistik regresyon | `13_modul/`, `14_modul/` |
| — | 4–17 Ocak 2027 | **FİNAL SINAVI** (tarih bölümce ilan edilir) | — |

Soldaki numara **oturum** (takvimdeki ders günü), sağdaki `NN_modul/` ise depodaki **konu paketidir**. İkisi bire bir eşleşmez: 3. oturumda iki modül işlenir (`05_modul/` + `15_modul/`), 10. modül iki oturuma yayılır (8. ve 9. oturum). Modül numaraları dönem boyunca değişmez.

Ayrıntı ve okuma atamaları için izlenceye bakınız.

------------------------------------------------------------------------

## Değerlendirme

|                             |         |
|-----------------------------|---------|
| Ara Sınav (Vize)            | **%40** |
| Yarıyıl Sonu Sınavı (Final) | **%60** |

Proje, ödev, kısa sınav ve katılım notu **yoktur.** Her oturumun ardından yayımlanan alıştırmalar ve cevap anahtarları **notlandırılmaz**; kendinizi sınamanız içindir. Sınav soruları bu alıştırmalarla aynı biçimde kurgulanır.

------------------------------------------------------------------------

## Depo yapısı

```         
IST2083/
├── izlence/         Ders izlencesi
├── 01_modul/ …      Modül klasörleri: ders notu, sunum, lab, alıştırma,
│                    cevap anahtarı (01–15; numara sırası oturum sırası değildir)
├── data/            Tüm veri setleri (tek merkez)
├── images/          Görseller
├── my_work/         SİZİN çalışma klasörünüz: güncellemeler buraya dokunmaz
├── update.R         Materyalleri güncelleyen betik: source("update.R")
├── scripts/         Şekil ve veri üretim betikleri (derse katılmak için gerekmez)
├── docs/            Materyal yazım standardı (yazar notu)
├── GitHub_Kullanim_Kilavuzu.pdf, R_RStudio_Kurulum_Rehberi.pdf, R-Hizli-Referans.pdf
├── IST2083.Rproj    RStudio proje dosyası — çalışmaya bunu açarak başlayın
└── README.md
```

**Klasör numaraları ile oturum numaraları aynı değildir.** Klasör adları dersin ilk yılından gelen sıralamayı korur; hangi oturumda hangi klasörün işleneceğini yukarıdaki tablodan görebilirsiniz.

## Veri dosyalarını okuma

Tüm veri setleri `data/` klasöründedir ve `here` paketiyle çağrılır:

``` r
library(here)
veri <- read.csv(here("data", "example_data.csv"))
```

`here()`, proje kökünü `IST2083.Rproj` dosyasından bulur. Bu sayede kod hem sizde hem bizde, hem Windows'ta hem macOS'ta aynı şekilde çalışır. **Kendi bilgisayarınıza özel mutlak yol yazmayın** (`C:/Users/...` veya `~/Desktop/...` gibi).

## Ders materyallerini alma ve güncelleme

**İlk kez (bir defa):** RStudio → *File → New Project → Version Control → Git* → Repository URL:

```         
https://github.com/Proximalist/IST2083-public.git
```

**Çalışma kuralı:** Ders dosyalarını doğrudan düzenlemeyin. Üzerinde çalışmak istediğiniz dosyayı önce `my_work/` klasörüne kopyalayın ve orada çalışın.

**Her derste, başlamadan önce (güncelleme):** RStudio'da projeyi açıp Console'a şunu yazın:

``` r
source("update.R")
```

Notlar:

- "Commit", "Push" ve "Pull" düğmelerini kullanmanıza gerek yoktur.
- Bu depoya yükleme (push) yapamazsınız; bu normaldir.
- Yanlışlıkla orijinal bir dosyayı düzenlerseniz endişelenmeyin: `update.R` değişikliklerinizi `my_work/yedek_...` klasörüne yedekler ve dosyayı orijinal haline getirir.
- Adım adım anlatım ve hata çözümleri için **GitHub Kullanım Kılavuzu**'na bakınız.

## Ders ortamı

İki seçenekten birini kullanabilirsiniz:

- **RStudio (yerel)** — dersin ana anlatım ortamı. Kurulum için Kurulum Rehberi'ne bakınız.
- **GitHub Codespaces (bulut)** — tarayıcıda çalışır, kurulum gerektirmez; bir GitHub hesabı gerekir. Kılavuzda anlatılmıştır.

## Soru ve sorun bildirme

- **Ders içeriğiyle ilgili sorular:** hakan.mehmetcik\@marmara.edu.tr
- **Teknik sorunlar** (kurulum, paket hatası, çalışmayan kod): GitHub hesabınız varsa bu deponun **Issues** sekmesini kullanın; böylece aynı sorunu yaşayan arkadaşlarınız da cevabı görür. Hesabınız yoksa aynı bilgileri yukarıdaki e-posta adresine gönderin.

Issue açarken hatayı üreten **en kısa kod parçasını** ve **hata mesajının tamamını** yapıştırın; ekran görüntüsü yerine metin tercih edilir.
