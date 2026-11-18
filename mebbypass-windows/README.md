<div align="center">

# 🛰️ mebbypass

[![sürüm](https://img.shields.io/badge/s%C3%BCr%C3%BCm-0.1.2-blue)](#)
[![python](https://img.shields.io/badge/Python-3.9%2B-informational?logo=python&logoColor=white)](https://www.python.org)
[![platform](https://img.shields.io/badge/platform-Pardus%20ETAP%2023%20%7C%20Debian%2012-green)](#)
[![arayüz](https://img.shields.io/badge/aray%C3%BCz-GTK3-purple)](#)
[![lisans](https://img.shields.io/badge/lisans-MIT-yellow)](LICENSE)

**MEB/f@tih okul ağı filtrelerini sunucusuz aşan, yerel HTTP proxy.**
Windows doğrudan çalışır; sunucu, VPS, VPN ya da
pip paketi **gerekmez** — yalnızca Python 3 standart kitaplığı.
Windows için aynı klasördeki `BASLAT.bat` / `GUI.bat` dosyalarına bakın
(`README-WINDOWS.md`).

**A serverless local HTTP proxy that bypasses MEB/f@tih school network
filtering (Turkey) via SNI camouflage, DNS-over-HTTPS and TLS ClientHello
fragmentation — with a GTK interface, self-diagnostics and an installable
.deb package.**

</div>

---

## ⚠️ Önemli: Kullanım Koşulları

> **Bu araç kesinlikle eğitim amaçlıdır.** Okul ağının internet filtrelerini
> aşmak; öğrenme, araştırma ve eğitsel içeriğe erişim için tasarlanmıştır.
> **Kötü niyetli kullanım yasaktır**: ağ tarama, bant genişliği sömürüsü,
> engelli içeriklere erişim veya ağın kurallarını ihlal eden her türlü
> davranış bu aracın kapsamı dışındadır.
> **Olası kötü niyetli kullanımdan doğacak her sonucun sorumluluğu aracı
> kullanan kişiye aittir.** Ağınızın okul yönetmeliğini kontrol edin;
> araç, yönetmelik ihlallerinden hukuki bir koruma sağlamaz.
>
> *This tool is strictly for educational purposes. Malicious use is
> prohibited, and the user is fully responsible for any misuse.*

---

## ✨ Ne yapar?

| Katman | Teknik | Ne işe yarar? |
|:---:|---|---|
| 🧭 | **DoH DNS** | Ad çözümleme okulun (filtreli) DNS'ine sorulmadan Google/Cloudflare DoH ile yapılır |
| 🎭 | **SNI kamufle** | Bağlantı gerçek IP'ye kurulur; TLS ClientHello'daki SNI, MEB'de izinli bir domain (WhatsApp/Google/MEB…) olarak gönderilir. CDN'ler uyumsuz SNI'yı kabul ettiği için **sertifika yüklemeye gerek yoktur** |
| ✂️ | **ClientHello parçalama** | DPI'yı şaşırtmak için ilk TLS kaydı 8 baytlık segmentlere bölünür (istenirse kapatılır) |

Ayrıca: GTK3 **grafik arayüzü** (tepsi desteğiyle), **otomatik teşhis
sistemi** (masaüstüne Markdown rapor yazar), **gsettings/Firefox
entegrasyonu** (önceki ayarları yedekleyip geri yükler), **otomatik yedek
port** (8080 doluysa 8081, 8888, 9090, 3128, 8443, 1080 sırayla denenir),
**tek örnek koruması** (aynı anda iki proxy/arayüz açılamaz) ve 8 adım
**deneysel teknik testi** (boş SNI, DoT, QUIC, ECH, IPv6…).


*meb internet filtresi kırma · fatih ağı proxy · okul interneti bypass ·
pardus etap 23 · akıllı tahta internet · sni bypass · sni kamufle ·
domain fronting · dpi bypass · tls fragmentation · clienthello parçalama ·
dns over https · doh proxy · eba · eba.gov.tr · meb gov tr ·
youtube okulda açma · türkiye sansür bypass · school internet bypass
turkey · turkey censorship · smart board proxy · mebbypass*
