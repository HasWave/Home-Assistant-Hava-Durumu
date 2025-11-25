# 🌤️ HasWave Hava Durumu

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Open-Meteo API ile hava durumu tahminlerini Home Assistant'a weather entity olarak ekler**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=HasWave&repository=HACS-Hava-Durumu&category=Integration" target="_blank">
  <img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.">
</a>

</div>

---

## 📋 Özellikler

* 🌍 **Open-Meteo API** - Ücretsiz ve güvenilir hava durumu API'si
* ✅ **Config Flow** - Kolay kurulum ve yapılandırma
* 📅 **7-16 Günlük Tahmin** - Detaylı günlük hava durumu tahminleri
* 🌡️ **Güncel Hava Durumu** - Anlık sıcaklık, nem, basınç, rüzgar bilgileri
* 🎨 **Weather Entity** - Home Assistant'ın native weather entity formatı
* 🔄 **Otomatik Güncelleme** - Belirli aralıklarla otomatik veri güncelleme
* 🌐 **Dünya Çapında** - Herhangi bir konum için hava durumu
* 🏠 **Otomatik Konum** - Home Assistant konumunu otomatik kullanabilir

## 🚀 Hızlı Başlangıç

### 1️⃣ HACS ile Kurulum

1. Home Assistant → **HACS** → **Integrations**
2. Sağ üstteki **⋮** menüsünden **Custom repositories** seçin
3. Repository URL: `https://github.com/HasWave/Home-Assistant-Hava-Durumu`
4. Category: **Integration** seçin
5. **Add** butonuna tıklayın
6. HACS → Integrations → **HasWave Hava Durumu**'nu bulun
7. **Download** butonuna tıklayın
8. Home Assistant'ı yeniden başlatın

### 2️⃣ Manuel Kurulum

1. Bu repository'yi klonlayın veya indirin
2. `custom_components/haswave_hava_durumu` klasörünü Home Assistant'ın `config/custom_components/` klasörüne kopyalayın
3. Home Assistant'ı yeniden başlatın

### 3️⃣ Integration Ekleme

1. Home Assistant → **Settings** → **Devices & Services**
2. Sağ alttaki **+ ADD INTEGRATION** butonuna tıklayın
3. **HasWave Hava Durumu** arayın ve seçin
4. Yapılandırma formunu doldurun:
   - **Latitude**: Enlem (opsiyonel - boş bırakılırsa Home Assistant konumu kullanılır)
   - **Longitude**: Boylam (opsiyonel - boş bırakılırsa Home Assistant konumu kullanılır)
   - **Timezone**: Zaman dilimi (varsayılan: `Europe/Istanbul`)
   - **Forecast Days**: Tahmin günü (varsayılan: 7, maksimum: 16)
   - **Update Interval**: Güncelleme aralığı saniye (varsayılan: 3600 = 1 saat)
5. **Submit** butonuna tıklayın

**✅ Weather Entity Otomatik Oluşturulur:** Integration eklendiğinde `weather.haswave_hava_durumu` entity'si direkt Home Assistant'a eklenir. Hiçbir ek kurulum gerekmez!

**Not:** Konum bilgisi girilmezse, Home Assistant'ın ayarladığınız konum bilgisi (`Settings` → `General` → `Location`) otomatik kullanılır.

### 4️⃣ Konum Bulma

Konumunuzun koordinatlarını bulmak için:
- [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)
- Google Maps'te konumunuza sağ tıklayıp koordinatları kopyalayın
- [LatLong.net](https://www.latlong.net/)

## 📖 Kullanım

### Home Assistant Weather Entity

Integration otomatik olarak şu weather entity'yi oluşturur:

#### `weather.haswave_hava_durumu`

**State:** Hava durumu durumu (clear-day, clear-night, partlycloudy, cloudy, fog, rainy, snowy, lightning, etc.)

**Attributes:**
- `temperature` - Sıcaklık (°C)
- `humidity` - Nem (%)
- `pressure` - Basınç (hPa)
- `wind_speed` - Rüzgar hızı (km/h)
- `wind_bearing` - Rüzgar yönü (°)
- `apparent_temperature` - Hissedilen sıcaklık (°C)
- `cloud_coverage` - Bulut örtüsü (%)
- `forecast` - Günlük tahmin array'i
  - `datetime` - Tarih
  - `condition` - Hava durumu durumu
  - `temperature` - Maksimum sıcaklık (°C)
  - `templow` - Minimum sıcaklık (°C)
  - `precipitation` - Yağış miktarı (mm)
  - `precipitation_probability` - Yağış olasılığı (%)
- `latitude` - Enlem
- `longitude` - Boylam
- `elevation` - Yükseklik (m)
- `attribution` - Veri kaynağı

### Dashboard Kartı

#### Weather Card (Güncel)

```yaml
type: weather
entity: weather.haswave_hava_durumu
```

#### Weather Forecast Card

```yaml
type: weather-forecast
entity: weather.haswave_hava_durumu
forecast_type: daily
```

#### Örnek Dashboard Yapılandırması

```yaml
type: vertical-stack
cards:
  - type: weather
    entity: weather.haswave_hava_durumu
  - type: weather-forecast
    entity: weather.haswave_hava_durumu
    forecast_type: daily
```

### Otomasyon Örnekleri

#### Yağmur Uyarısı

```yaml
automation:
  - alias: "Yağmur Uyarısı"
    trigger:
      - platform: numeric_state
        entity_id: weather.haswave_hava_durumu
        attribute: forecast[0].precipitation_probability
        above: 70
    action:
      - service: notify.mobile_app
        data:
          message: "Bugün yağmur bekleniyor! Şemsiye almayı unutmayın."
```

#### Sıcaklık Uyarısı

```yaml
automation:
  - alias: "Yüksek Sıcaklık Uyarısı"
    trigger:
      - platform: numeric_state
        entity_id: weather.haswave_hava_durumu
        attribute: forecast[0].temperature
        above: 30
    action:
      - service: notify.mobile_app
        data:
          message: "Bugün sıcaklık 30°C'nin üzerinde olacak!"
```

#### Düşük Sıcaklık Uyarısı

```yaml
automation:
  - alias: "Düşük Sıcaklık Uyarısı"
    trigger:
      - platform: numeric_state
        entity_id: weather.haswave_hava_durumu
        attribute: forecast[0].templow
        below: 0
    action:
      - service: notify.mobile_app
        data:
          message: "Bugün don bekleniyor! Dikkatli olun."
```

## 🔧 Gelişmiş Kullanım

### Konum Ayarlama

Integration ayarlarından konum bilgisini güncelleyebilirsiniz. Konum boş bırakılırsa Home Assistant'ın genel ayarlarındaki konum kullanılır.

### Performans Optimizasyonu

* **Güncelleme Aralığı** değerini artırarak API çağrı sayısını azaltabilirsiniz (hava durumu verileri sık değişmediği için 1 saat yeterlidir)
* **Forecast Days** değerini azaltarak daha az veri çekebilirsiniz

### Sorun Giderme

#### Weather Entity Görünmüyor

* Integration'ın eklendiğini kontrol edin: **Settings** → **Devices & Services**
* Home Assistant'ı yeniden başlatın
* Entity'yi **Settings** → **Devices & Services** → **Entities** bölümünden kontrol edin
* Logları kontrol edin: **Settings** → **System** → **Logs**

#### Hava Durumu Verileri Güncellenmiyor

* Güncelleme aralığı değerini kontrol edin
* Open-Meteo API'nin erişilebilir olduğundan emin olun
* Logları kontrol edin: **Settings** → **System** → **Logs**

#### Yanlış Konum

* Integration ayarlarından `latitude` ve `longitude` değerlerini kontrol edin
* Koordinatların doğru formatta olduğundan emin olun (ondalık sayı)
* Zaman dilimini (`timezone`) doğru seçin

#### API Hataları

* İnternet bağlantınızı kontrol edin
* Open-Meteo API'nin çalıştığından emin olun: https://open-meteo.com/en/docs
* Rate limit aşılmış olabilir (çok sık güncelleme yapıyorsanız güncelleme aralığını artırın)

#### Integration Ekleme Hatası

* HACS üzerinden doğru şekilde yüklendiğinden emin olun
* Home Assistant'ı yeniden başlatın
* `custom_components` klasörünün doğru konumda olduğundan emin olun

## 📁 Dosya Yapısı

```
HACS-Hava-Durumu/
├── custom_components/
│   └── haswave_hava_durumu/
│       ├── __init__.py
│       ├── manifest.json
│       ├── const.py
│       ├── api.py
│       ├── weather.py
│       └── config_flow.py
├── hacs.json
└── README.md
```

## 🌐 Open-Meteo API

Bu entegrasyon [Open-Meteo](https://open-meteo.com/) API'sini kullanır. Open-Meteo:
- Ücretsiz ve açık kaynak
- API key gerektirmez
- Dünya çapında hava durumu verileri
- Yüksek çözünürlüklü hava modelleri
- 16 güne kadar tahmin

Daha fazla bilgi için: [Open-Meteo Documentation](https://open-meteo.com/en/docs)

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**HasWave**

🌐 [HasWave](https://haswave.com) | 📱 [Telegram](https://t.me/HasWave) | 📦 [GitHub](https://github.com/HasWave)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

Made with ❤️ by HasWave

