# GÜN: Blokzincir Tabanlı Güvenli Uydu Haberleşme Ağı (ISL) 🛰️🔗

## 📖 Proje Hakkında
**GÜN**, uydu ağlarında özellikle **Inter-Satellite Link (ISL)** üzerinden gerçekleştirilen haberleşmenin güvenliğini artırmak amacıyla geliştirilmiş bir protokol ve simülasyon aracıdır.  
Bu projede, uydu-uydu ve uydu-yer istasyonu arasındaki veri iletiminde bütünlük, doğrulama ve değiştirilemezlik (immutability) sağlayan yenilikçi bir yaklaşım sergilenmektedir.

## 🛠️ Sistem Mimarisi

### 1. Blokzincir Katmanı (Blockchain Core)
Sistem, yetkili uydular tarafından onaylanan bir **Proof of Authority (PoA)** yapısını temel alır:
* **Blok Yapısı:** Her blok; index, zaman damgası, işlemler, önceki blok hash'i ve doğrulayıcı kimliğini içerir.
* **Güvenlik:** Bloklar arası bağlantı **SHA-256** algoritması ile hashlenerek veri bütünlüğü korunur.
* **Doğrulama:** Sadece önceden tanımlanmış yetkili uydular blok ekleme yetkisine sahiptir.

### 2. Güvenli Anahtar Yönetimi (Key Manager)
Uydular arasındaki veri iletimini şifrelemek için dinamik oturum anahtarları kullanılır:
* **AES Şifreleme:** Simülasyonda **Fernet (AES)** tabanlı kriptografik anahtarlar üretilir.
* **Zincir Üstü Doğrulama:** Üretilen anahtarların hash değerleri blokzincire kaydedilir; deşifreleme öncesi yerel anahtarın doğruluğu zincirdeki kayıtla karşılaştırılır.
* **Zaman Sınırı:** Her anahtarın bir geçerlilik süresi (expiration) bulunur.

### 3. Yörünge ve Link Analizi (MATLAB)
Proje, teorik uydu mekaniği hesaplamaları ile desteklenmiştir:
* **Slant Range Hesaplama:** LEO (600 km) irtifadaki uydular için bakış açısına bağlı mesafe değişimi analiz edilir.
* **Matematiksel Model:** Hesaplamalarda aşağıdaki formül kullanılmıştır:

$$
d = R_e \cdot \left(\sqrt{\left(\frac{R_s}{R_e}\right)^2 - \cos^2(\epsilon)} - \sin(\epsilon)\right)
$$

*(Burada $d$: Slant Range, $R_e$: Dünya yarıçapı, $R_s$: Uydu yarıçapı, $\epsilon$: Bakış açısıdır.)*

## 💻 Simülasyon Senaryosu
`simulation.py` dosyası üzerinden interaktif bir terminal arayüzü sunulur:
1. **Anahtar Talebi:** Bir uydu, diğer uydu ile iletişim kurmak için anahtar talep eder.
2. **Blok Onayı:** Doğrulayıcı uydu (validator), işlemi onaylayarak blokzincire ekler.
3. **Şifreli İletişim:** Anahtarlar doğrulandıktan sonra uçtan uca şifreli mesaj iletimi gerçekleştirilir.
4. **Görselleştirme:** **NetworkX** kütüphanesi ile uydu ağı ve anahtar alışverişi görselleştirilir.

## 📂 Dosya İçerikleri
* `blockchain_core.py`: Blokzincir yapısının temel sınıfları.
* `key_manager.py`: Kriptografik anahtar yönetimi ve hash işlemleri.
* `simulation.py`: Senaryo bazlı haberleşme simülasyonu.
* `elevation_analysis.m`: Yörünge analiz grafikleri için MATLAB scripti.

## 🎓 Akademik Bağlam
Bu çalışma **Necmettin Erbakan Üniversitesi**, Havacılık ve Uzay Mühendisliği Bölümü bünyesinde  
“Teknoloji ve İnovasyon” dersi kapsamında proje olarak geliştirilmiştir.

---
*Geliştiren: Fatma Gül Koçak*
