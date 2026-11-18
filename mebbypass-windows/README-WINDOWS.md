# mebbypass — Windows

Pardus sürümünün aynı çekirdeği. Linux dosyaları duruyor; Windows'ta
sistem proxy'si kayıt defterinden, Firefox `user.js` ile, arayüz
tkinter ile çalışır. Ek paket yok: Python 3.9+ yeterli.

## Kurulum

1. [python.org](https://www.python.org/downloads/windows/) → Python 3 kur.
2. Kurulumda **Add python.exe to PATH** kutusunu işaretle.
3. Bu klasörü istediğin yere çıkar (örneğin `C:\mebbypass`).

## Çalıştırma (çift tık)

| Dosya | Ne yapar |
|---|---|
| `BASLAT.bat` | Proxy'yi açar, Windows + Firefox proxy'sini ayarlar |
| `DURDUR.bat` | Proxy'yi kapatır, eski proxy ayarını geri yükler |
| `GUI.bat` | Pencere (başlat / durdur / teşhis) |
| `TEST.bat` | Kısa bağlantı testi |
| `TANI.bat` | Teşhis raporu — masaüstüne `.md` |
| `DURUM.bat` | Çalışıyor mu? |
| `LOG.bat` | Son log satırları |
| `GERI-AL.bat` | Yalnız sistem proxy'sini eski haline çevirir |

Hepsi `mebbypass.bat` üzerinden gider:

```bat
mebbypass.bat
mebbypass.bat stop
mebbypass.bat gui
mebbypass.bat tani
mebbypass.bat start -p 9090
```

Proxy ayağa kalkınca ve işlem bitince (Ctrl+C, durdurma, test, teşhis
veya pencere kapanışı) terminalde şu satır yazar:

```text
fatih cracked by Venathra Team
```

Pencere hemen kapanmasın diye bir tuş beklenir.

## Ne değişti (Linux bozulmadan)

- `TCP_NODELAY`: Windows küçük TLS parçalarını tek pakette birleştirir;
  bu olmadan SNI parçalama işe yaramaz.
- Sistem proxy: `Internet Settings` (Edge, Chrome). Eski değer
  `%USERPROFILE%\.mebbypass\win-proxy-yedek.json` içine yazılır.
- Firefox: her profilin `user.js` dosyasına işaretli blok eklenir,
  kapatınca silinir.
- Arayüz: `mebbypass\gui_win.py`. GTK dosyası Pardus için yerinde.
- Açılışta başlat: Başlangıç klasörüne `mebbypass-autostart.bat`.

Log: `%USERPROFILE%\.mebbypass\log.txt`

Firefox veya Edge açıksa proxy'yi görsün diye tarayıcıyı bir kez
kapatıp aç. Firefox "Sistem proxy ayarlarını kullan" da durabilir;
`user.js` elle proxy yazar, bir sonraki açılışta geçer.
