# Türkçe POS Tagging'de Merkezleme Kuramı ile Belirsizlik Azaltma

## 🎯 Ne Yapıyoruz? (Basit Anlatım)

Bilgisayara Türkçe cümleler veriyoruz. Bilgisayar her kelimeyi etiketliyor: "Bu bir isim, bu bir fiil, bu bir zamir..." gibi.

**Problem:** Bazen bilgisayar aynı kelime için iki farklı etiket önerebiliyor. Mesela:
- "**O** süt aldı" cümlesindeki **"O"** kelimesi:
  - 🤔 Bir **zamir** mi? (he/she anlamında)
  - 🤔 Yoksa **isim** mi? (literal "O" harfi)

**Çözüm:** Merkezleme kuramını kullanıyoruz! 

Merkezleme kuramı şöyle düşünüyor:
> "Önceki cümlede 'Ahmet' vardı. Eğer bu 'O' kelimesi bir zamir ise, Ahmet'ten bahsediyor olmalı. O zaman cümleler birbiriyle bağlantılı, söylem tutarlı. Ama eğer 'O' bir isim ise, bambaşka bir şeyden bahsediyoruz demektir. O zaman cümleler kopuk."

Bilgisayar her iki seçeneği deniyor ve **hangisi cümleleri daha tutarlı hale getiriyorsa onu seçiyor!**
## 🧪 Test Dosyaları

### 1. **demo_stanza_centering.py** - 9 Hata Türü Analizi 🆕 GELİŞTİRİLDİ
Merkezleme kuramının farklı parser hatalarını nasıl tespit ettiğini gösterir.

**GELİŞTİRİLMİŞ ÖRNEKLERLE SONUÇLAR (v2.0):**

| Hata Türü | Centering Neyi Fark Eder? | Örnek | Sonuç |
|-----------|---------------------------|-------|-------|
| **Koreferans** 🆕 | Sayı uyumsuzluğu (-25 ceza) | "Öğrenciler. O oturdu." | ✅ **Başarılı** (2>1) |
| **Topic drift** | Cb tamamen kaybolur | "Ahmet okuyor. Hava güzel." | ✅ **Başarılı** (2>1) |
| **Overconfidence** 🆕 | Animacy uyumsuzluğu (-20 ceza) | "Taş oynadı. O yoruldu." | ✅ **Başarılı** (2>1) |
| **LLM hatası** | Akıcı ama merkezsiz | "Ahmet yedi. Afiyet olsun doydu." | ✅ **Başarılı** (2>1) |
| POS hatası | Zamir çözümü kopar | "O süt aldı" vs "O anda süt aldı" | ⚖️ Eşit (1=1) |
| Role hatası | Özne düşer | Pasif: "Mektup yazıldı" | ⚖️ Eşit (2=2) |
| Attachment | Varlık kaybolur | "Ayşe'nin kedisi" vs "Ayşe kedisinin" | ⚖️ Eşit (2=2) |
| Chunking | Öbek parçalanır | "Yazılım mühendisi. Yazılım güzel." | ⚖️ Eşit (1=1) |
| Segmentation | Cf kaotikleşir | Yanlış cümle sınırı | ⚖️ Eşit (1=1) |

**Başarı Oranı:** 4/9 (%44) Başarılı, 5/9 (%56) Belirsiz | **İyileşme: +100%** (2/9 → 4/9)

**Çalıştırma:**
```bash
python demo_stanza_centering.py
```

**🆕 YENİ ÖZELLİKLER (v2.0):**
- ✅ **Sayı uyumu kontrolü:** Tekil/çoğul zamirleri bileşik isimlerde doğru eşleştirme
- ✅ **Animacy (canlılık) skoru:** Cansız varlıklara şahıs zamiri ağır ceza (-20)
- ✅ **Noun phrase chunking:** Bileşik isimler (örn: "öğrenciler_sınıfa") tek varlık olarak işleniyor
- ✅ **Güçlendirilmiş ceza sistemi:** Sayı uyumsuzluğu -25, animacy uyumsuzluğu -20

**Ana Bulgular:**
- ✅ **Söylem kopukluğu** tespitinde güçlü (Topic drift, LLM hatası)
- ✅ **Semantik tutarlılık** tespitinde güçlü (Koreferans, Overconfidence) 🆕
- ⚖️ **Yapısal detaylarda** henüz zayıf (Chunking, Pasif yapı, Attachment)
- 📈 **İyileşme:** %22 → %44 başarı oranı (+100%)

**Teknik Detaylar:**
- Threshold: 5 (zamir çözümlemesi için minimum skor)
- Animacy bonusu: +15 (canlı varlık), -20 (cansız varlık)
- Sayı uyumu: +15 (uyumlu), -25 (uyumsuz)
- Bileşik isim tespiti: `is_plural()` ilk kelimeyi kontrol eder

Detaylı analiz: [GELISMIS_ORNEK_ANALIZ.md](GELISMIS_ORNEK_ANALIZ.md)

### 2. **test_pos_error_centering.py** - POS Hatası Demo
Simüle edilmiş POS hatalarında merkezleme kuramının reranking başarısını gösterir.

**Çalıştırma:**
```bash
python test_pos_error_centering.py
```
## Amaç
Türkçe bağımlılık çözümlemede UAS/LAS ölçmek ve **Centering Theory** temelli yeniden sıralama (reranking) ile sonuçları iyileştirme fikrini denemek.

## Yöntem
1. **Akademik standart veri** olarak UD Turkish IMST test seti kullanıldı.
2. **Temel ayrıştırıcı**: Stanza (tokenize+pos+depparse).
3. **Karşılaştırmalı ayrıştırıcı**: UDPipe (spaCy-UDPipe ile).
4. **Centering tabanlı rerank**: İki ayrıştırıcının çıktıları, her cümle için centering geçiş skoruyla karşılaştırıldı ve daha yüksek skor seçildi.
5. UAS/LAS, seçilen parse’lar ile altın ağaçlara karşı hesaplandı.

## 🧪 Somut Örnek: Merkezleme Kuramı Nasıl Çalışıyor?

İki cümlemiz var:
1. **"Ahmet markete gitti."**
2. **"O süt aldı."**

İki farklı bilgisayar programı (parser) bu cümleleri etiketliyor:

### 📊 Parser A'nın Tahmini:
```
Cümle 1: Ahmet → PROPN (özel isim) ✅
         markete → NOUN (isim) ✅
         gitti → VERB (fiil) ✅

Cümle 2: O → PRON (zamir) ✅
         süt → NOUN (isim) ✅
         aldı → VERB (fiil) ✅
```

**Merkezleme kuramı ne diyor?**
- Cümle 1'deki en önemli şey: **Ahmet** (özne)
- Cümle 2'deki "O" zamir → Ahmet'e işaret ediyor! 
- **Bağlantı kuruldu!** Söylem tutarlı ✅
- **Skor: 2/3** (Smooth-Shift - yumuşak geçiş)

### 📊 Parser B'nin Tahmini:
```
Cümle 1: Ahmet → PROPN (özel isim) ✅
         markete → NOUN (isim) ✅
         gitti → VERB (fiil) ✅

Cümle 2: O → NOUN (isim) ❌ (HATA!)
         süt → NOUN (isim) ✅
         aldı → VERB (fiil) ✅
```

**Merkezleme kuramı ne diyor?**
- Cümle 1'deki en önemli şey: **Ahmet** (özne)
- Cümle 2'deki "O" → isim olarak etiketlenmiş, zamir değil
- **Bağlantı kurulamadı!** "O" bambaşka bir şey sanılıyor ❌
- **Skor: 1/3** (Rough-Shift - sert geçiş, kopuk söylem)

### 🎯 Sonuç:
```
Parser A Skoru: 2
Parser B Skoru: 1

✅ Merkezleme kuramı → Parser A'yı seçti (doğru olanı!)
```

**Öğretmen Özeti:** İki öğrenci aynı soruya farklı cevap verdi. Merkezleme kuramı, cümlelerin birbiriyle nasıl bağlandığına bakarak hangisinin doğru cevap verdiğini buldu!

## Merkezleme Kuramını Nasıl Kullandık?
- Her cümle için ayrıştırıcı çıktısından **forward centers (Cf)** çıkarıldı: isimler/özel isimler/ zamirler, bağımlılık ilişkilerine göre ağırlıklandırıldı (özne > nesne > diğerleri).
- Bir önceki cümlenin Cf listesiyle karşılaştırarak **backward center (Cb)** ve **preferred center (Cp)** belirlendi.
- İki cümle arasındaki geçiş tipi (Continue/Retain/Smooth-Shift/Rough-Shift) çıkarıldı ve **skorlandı**.
- Aynı cümle için Stanza ve UDPipe parse’ları bu centering skoruyla karşılaştırıldı; **daha yüksek skorlu parse** seçilerek UAS/LAS hesaplandı.
### POS Tagging Belirsizliğini Azaltma
Merkezleme kuramı, POS etiketlerini **söylemsel tutarlılıkla** sınayarak yapısal belirsizlikleri azaltır:
- İki parser'dan gelen POS etiketleri, söylemsel merkezleri (Cf) farklı şekilde belirler.
- Her iki POS seçeneği için centering geçiş skoru hesaplanır.
- **Daha tutarlı söylemsel yapı** üreten (yüksek centering skoru) POS etiketleri seçilir.
- Sonuç: Söylemsel olarak daha uyumlu POS etiketlemesi.
## Sonuçlar (UD Turkish IMST test)

### Dependency Parsing (UAS/LAS)
- **Stanza**: UAS 92.65 / LAS 89.19
- **UDPipe**: UAS 77.53 / LAS 57.90
- **Centering rerank**: UAS 92.59 / LAS 89.02

> Not: Bu koşulda rerank, Stanza'yı geçemedi. Geliştirme setinde centering ağırlıklarını optimize etmek ve daha güçlü ikinci parser eklemek muhtemel iyileştirme yollarıdır.

### POS Tagging (Belirsizlik Azaltma)
- **Stanza**: POS Accuracy 98.43%
- **UDPipe**: POS Accuracy 94.46%
- **Centering rerank**: POS Accuracy 98.43%

> Merkezleme kuramı, iki parser'ın POS etiketlerini söylemsel tutarlılıkla sınayarak en iyi seçimi yapıyor. Stanza'nın POS performansı zaten çok yüksek olduğundan rerank aynı seviyeyi korudu.

## Çalıştırma
- **Türkçe POS etiketleme testi**: [tr_pos_test.py](tr_pos_test.py)
- **Merkezleme kuramı Türkçe örnekleri**: [test_centering_turkish.py](test_centering_turkish.py)
- **Hatalı POS'ta merkezleme testi**: [test_pos_error_centering.py](test_pos_error_centering.py)
- **6 belirsizlik türü testi**: [test_ambiguity_types.py](test_ambiguity_types.py) ⭐ YENİ!
- **Dependency parsing rerank**: [evaluate_ud_tr_rerank.py](evaluate_ud_tr_rerank.py)
- **POS tagging rerank**: [evaluate_pos_centering.py](evaluate_pos_centering.py)
- **Tek parser değerlendirmesi**: [evaluate_ud_tr.py](evaluate_ud_tr.py)

Her script, gerekli verileri otomatik indirir ve sonuçları konsola yazar.

## 🎓 Önemli Dosyalar

### Test ve Demo Scriptleri:
- **[test_pos_error_centering.py](test_pos_error_centering.py)**: Hatalı POS etiketlerini merkezleme kuramının nasıl yakaladığını gösterir (yukarıdaki örnek!)
- **[test_ambiguity_types.py](test_ambiguity_types.py)**: 6 farklı belirsizlik türünü test eder ⭐ YENİ!
  - POS Tagging, Bağımlılık, Koreferas, NP Chunking, Özne-Nesne, PP-Attachment
  - **Sonuç: 5/6 test başarılı!** Merkezleme kuramı söylem tabanlı belirsizlikleri etkili şekilde çözüyor
- **[test_centering_turkish.py](test_centering_turkish.py)**: Türkçe cümlelerde zamir çözümlemesi ve söylem analizi örnekleri
- **[tr_pos_test.py](tr_pos_test.py)**: Basit Türkçe POS etiketleme demosu

### Değerlendirme Scriptleri:
- **[evaluate_ud_tr.py](evaluate_ud_tr.py)**: Stanza ile temel UAS/LAS değerlendirmesi
- **[evaluate_ud_tr_rerank.py](evaluate_ud_tr_rerank.py)**: Stanza + UDPipe + centering ile dependency parsing reranking
- **[evaluate_pos_centering.py](evaluate_pos_centering.py)**: Centering ile POS belirsizlik azaltma (reranking)

## 🔬 Teknik Detaylar

### Zamir Çözümlemesi (Pronoun Resolution)
Merkezleme kuramının en önemli özelliği! Türkçe zamirleri tespit edip önceki cümlelerdeki varlıklara bağlıyoruz:

- **Desteklenen zamirler**: o, onlar, bu, bunlar, şu, şunlar, kendisi, kendileri
- **Sayı uyumu**: Çoğul zamirler (-ler/-lar/-lere/-lara ekli) isimlere, tekil zamirler tekil isimlere öncelikli bağlanır
- **⚠️ Kritik**: Sadece **POS=PRON** olan kelimeler zamir çözümlemesine girer!

### Salience Skorlaması (Önem Hesaplama)
Her kelimeye "ne kadar önemli" skoru veriyoruz:

```
Bağımlılık rolü:
  - Özne (nsubj): +4 puan
  - Nesne (obj): +3 puan
  - Diğer (obl): +2 puan

POS etiketi:
  - Zamir (PRON): +3 puan
  - Özel isim (PROPN): +2 puan
  - İsim (NOUN): +1 puan

Pozisyon: Cümle başındaki kelimeler daha önemli
```

### Geçiş Tipleri ve Skorları
Cümleler arasındaki geçişleri 4 kategoriye ayırıyoruz:

| Geçiş Tipi | Açıklama | Skor |
|------------|----------|------|
| **Continue** | Aynı merkez devam ediyor | 3 ⭐⭐⭐ |
| **Retain** | Merkez korunuyor ama odak değişti | 2 ⭐⭐ |
| **Smooth-Shift** | Merkez değişti ama tutarlı | 2 ⭐⭐ |
| **Rough-Shift** | Beklenmeyen merkez değişimi | 1 ⭐ |

**Yüksek skor = Tutarlı söylem = Doğru POS etiketlemesi!**

## 🔍 Merkezleme Kuramı Başka Hangi Belirsizlikleri Azaltır?

### 1. 📎 Bağımlılık Belirsizliği (Attachment Ambiguity)

**Problem:** Bir kelime cümlede birden fazla yere bağlanabilir.

```
"Ahmet çayı içerken okuduğu kitabı bitirdi."
```

**Belirsizlik:** "içerken" hangi fiile bağlı?
- Seçenek A: "okuduğu" → "Çay içerken okuma olayı"
- Seçenek B: "bitirdi" → "Çay içerken bitirme olayı"

**Merkezleme Kuramı:**
- Önceki cümle: "Ahmet kitap okuyordu." → Merkez: **kitap**
- Seçenek A: Cb = kitap, Cp = kitap → **Continue** (skor: 3)
- Seçenek B: Cb = kitap, Cp = çay → **Rough-Shift** (skor: 1)
- ✅ Seçenek A daha tutarlı!

### 2. 🔗 Koreferas Belirsizliği (Coreference Resolution)

**Problem:** Zamir veya anafora birden fazla antecedent'e işaret edebilir.

```
Cümle 1: "Ahmet, Ali'ye kitap verdi."
Cümle 2: "O çok sevindi."
```

**Belirsizlik:** "O" kim?
- Seçenek A: O = Ahmet (veren kişi)
- Seçenek B: O = Ali (alan kişi)

**Merkezleme Kuramı:**
- Cümle 1 merkezleri: [ahmet (özne, yüksek salience), ali (dolaylı nesne), kitap]
- Seçenek A: "O" → ahmet → Cb=ahmet, Cp=ahmet → **Continue** (skor: 3)
- Seçenek B: "O" → ali → Cb=ali, Cp=ali → **Smooth-Shift** (skor: 2)
- ✅ Özne genellikle daha yüksek salience → Ahmet tercih edilir

> **Not:** Türkçe'de pragmatik bağlam önemli - "sevindi" fiili genellikle alan kişiye işaret eder, bu örnekte Ali. Merkezleme kuramı tek başına yeterli olmayabilir, semantik bilgi gerekebilir.

### 3. 📦 İsim Öbeği Sınırları (NP Chunking)

**Problem:** Hangi kelimelerin bir isim öbeği oluşturduğu belirsiz.

```
"Eski ev sahibi geldi."
```

**Belirsizlik:**
- Seçenek A: [Eski ev] [sahibi] → "Eski evin sahibi"
- Seçenek B: [Eski] [ev sahibi] → "Önceki ev sahibi kişi"

**Merkezleme Kuramı:**
- Önceki cümle: "Ev çok eskiydi." → Merkez: **ev**
- Seçenek A: Cb = ev (öbekten çıkarıldı)
- Seçenek B: Cb = YOK (ev sahibi tek token)
- ✅ Seçenek A önceki söylemle bağlantı kuruyor!

### 4. ⚖️ Özne-Nesne Belirsizliği (Türkçe Serbest Sözdizimi)

**Problem:** Türkçe'de kelime sırası esnek, özne/nesne karışabilir.

```
"Kediye köpek baktı."
```

**Belirsizlik:**
- Seçenek A: Özne=köpek, Nesne=kedi → "Köpek kediye baktı"
- Seçenek B: Özne=kedi, Nesne=köpek → "Kedi köpeğe baktı" (ters)

**Merkezleme Kuramı:**
- Önceki cümle: "Köpek bahçede oynuyordu." → Merkez: **köpek**
- Seçenek A: Cb=köpek (özne), Cp=köpek → **Continue** (skor: 3)
- Seçenek B: Cb=köpek (nesne, düşük salience) → **Retain/Shift** (skor: 2)
- ✅ Özne pozisyonu daha yüksek salience → Seçenek A tercih edilir

### 5. 🎯 Edatsal İfade Bağlantısı (PP-Attachment)

**Problem:** Edatlı ifade hangi kelimeye bağlı?

```
"Ahmet markette kadına çiçek verdi."
```

**Belirsizlik:** "markette" nereye bağlı?
- Seçenek A: "verdi" fiiline → "Markette verme olayı gerçekleşti"
- Seçenek B: "kadın"a → "Marketteki kadın"

**Merkezleme Kuramı:**
- Önceki cümle: "Ahmet markete gitti." → Merkez: **market**
- Seçenek A: Forward Centers = [ahmet, kadın, çiçek, market(obl)]
- Seçenek B: Forward Centers = [ahmet, "marketteki kadın" (öbek), çiçek]
- Seçenek A'da "market" ayrı varlık → Cb kurulabilir
- ✅ Önceki söylemle tutarlılık kontrol edilir

### 6. 💬 Sözcük Anlamı Belirsizliği (Word Sense Disambiguation)

**Problem:** Aynı kelime farklı anlamlarda kullanılabilir.

```
Cümle 1: "Ahmet kapıyı açtı."
Cümle 2: "Kapı eski ve gıcırtılıydı."
Cümle 3: "Şimdi onu tamir etmeli."
```

**Belirsizlik:** Cümle 3'teki "onu" → "kapı" mı "Ahmet" mi?

**Merkezleme Kuramı:**
- Cümle 2 merkezleri: [kapı (özne, yüksek salience)]
- Seçenek A: "onu" → kapı → Cb=kapı, Cp=kapı → **Continue** (skor: 3)
- Seçenek B: "onu" → ahmet → Cb=YOK → **Rough-Shift** (skor: 1)
- ✅ En yakın yüksek salience'lı varlık tercih edilir

### 📊 Özet Tablo

| Belirsizlik Tipi | Merkezleme Kuramı Nasıl Yardımcı Olur? | Örnek | Test Sonucu |
|------------------|----------------------------------------|-------|-------------|
| **POS Tagging** | Zamir çözümlemesi için doğru etiket gerekir | "O" → PRON vs NOUN | ✅ Başarılı (2>1) |
| **Dependency Attachment** | Tutarlı merkez devamlılığı sağlayan bağlantı seçilir | "içerken" hangi fiile bağlı? | ✅ Berabere (bağlam gerekli) |
| **Coreference** | Yüksek salience'lı varlıklar tercih edilir | "O" → Ahmet vs Ali | ✅ Özne tercihi (2/3) |
| **NP Chunking** | Önceki söylemle bağlantı kuran öbek seçilir | [Eski ev] vs [ev sahibi] | ⚠️ Berabere (1=1) |
| **Role Ambiguity** | Özne pozisyonu daha yüksek skor alır | Özne=köpek vs kedi | ✅ Başarılı (2>1) |
| **PP-Attachment** | Söylem bağlamıyla tutarlı bağlantı | "markette" nereye bağlı? | ✅ Berabere (2=2) |
| **Word Sense** | En yakın merkeze işaret eden anlam seçilir | "onu" → kapı vs Ahmet | - (test edilmedi) |

**Test Sonuçları ([test_ambiguity_types.py](test_ambiguity_types.py)):**
- ✅ **5/6 test beklenen sonucu verdi**
- POS Tagging, Özne-Nesne belirsizliği %100 başarılı
- Bağımlılık, Koreferas, PP-Attachment: Her iki seçenek de makul (berabere)
- NP Chunking: İyileştirme gerekli (compound detection)

**Genel Prensip:** Merkezleme kuramı, **söylem tutarlılığını** ölçerek belirsizlikleri çözümler. Cümleler arası bağlantı ne kadar güçlüyse, o seçenek o kadar doğrudur!
| **PP-Attachment** | Söylem bağlamıyla tutarlı bağlantı | "markette" nereye bağlı? |
| **Word Sense** | En yakın merkeze işaret eden anlam seçilir | "onu" → kapı vs Ahmet |

**Genel Prensip:** Merkezleme kuramı, **söylem tutarlılığını** ölçerek belirsizlikleri çözümler. Cümleler arası bağlantı ne kadar güçlüyse, o seçenek o kadar doğrudur!