# 🌤️ HasWave Hava Durumu

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**HasWave API ile hava durumu tahminlerini Home Assistant'a weather entity olarak ekler. Otomatik konum desteği ve 30 dakikada bir otomatik güncelleme.**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=HasWave&repository=Home-Assistant-Hava-Durumu&category=Integration" target="_blank">
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
3. `www/json/` klasöründeki JSON animasyon dosyalarını Home Assistant'ın `config/www/json/` klasörüne kopyalayın
4. `lordicon.js` dosyasını Home Assistant'ın `config/www/` klasörüne kopyalayın:
   ```bash
   # Linux/Mac
   curl -o config/www/lordicon.js https://cdn.lordicon.com/lordicon.js
   
   # Windows (PowerShell)
   Invoke-WebRequest -Uri "https://cdn.lordicon.com/lordicon.js" -OutFile "config\www\lordicon.js"
   ```
5. Home Assistant'ı yeniden başlatın

**Not:** `lordicon.js` dosyası animasyonlu kartlar için gereklidir. HACS ile kurulumda otomatik olarak kopyalanır.

### 3️⃣ Integration Ekleme

1. Home Assistant → **Settings** → **Devices & Services**
2. Sağ alttaki **+ ADD INTEGRATION** butonuna tıklayın
3. **HasWave Hava Durumu** arayın ve seçin
4. Yapılandırma formunu doldurun:
   - **İl (Opsiyonel)**: İl adı (örn: TEKİRDAĞ, İSTANBUL). Boş bırakılırsa Home Assistant konumu otomatik kullanılır
   - **İlçe (Opsiyonel)**: İlçe adı (örn: ÇORLU, KAPAKLI). Boş bırakılabilir
   - **Timezone**: Zaman dilimi (varsayılan: `Europe/Istanbul`)
   - **Forecast Days**: Tahmin günü (varsayılan: 7, maksimum: 16)
   - **Update Interval**: Güncelleme aralığı saniye (varsayılan: 1800 = 30 dakika)
5. **Submit** butonuna tıklayın

**✅ Weather Entity Otomatik Oluşturulur:** Integration eklendiğinde `weather.haswave_hava_durumu` entity'si direkt Home Assistant'a eklenir. Hiçbir ek kurulum gerekmez!

**✅ Otomatik Konum:** İl/İlçe belirtilmezse, Home Assistant'ın ayarladığınız konum bilgisi (`Settings` → `General` → `Location`) otomatik kullanılır.

**✅ Otomatik Güncelleme:** Hava durumu verileri varsayılan olarak her 30 dakikada bir otomatik güncellenir.

### 4️⃣ Konum Ayarları

**Otomatik Konum:** İl/İlçe belirtilmezse, Home Assistant'ın genel ayarlarındaki konum bilgisi otomatik kullanılır (`Settings` → `General` → `Location`).

**Manuel Konum:** Belirli bir il/ilçe için hava durumu görmek istiyorsanız, kurulum sırasında İl ve İlçe alanlarını doldurun.

## 📖 Kullanım

### Entegrasyon Nasıl Çalışır?

HasWave Hava Durumu entegrasyonu şu şekilde çalışır:

1. **Weather Entity Oluşturur**: Integration eklendiğinde `weather.haswave_hava_durumu` adında bir weather entity oluşturulur
2. **Open-Meteo API Kullanır**: Hava durumu verileri [Open-Meteo API](https://open-meteo.com/)'den çekilir (ücretsiz, API key gerektirmez)
3. **Otomatik Güncelleme**: Belirlediğiniz aralıklarla (varsayılan: 1 saat) otomatik olarak veriler güncellenir
4. **7-16 Günlük Tahmin**: Günlük hava durumu tahminleri `forecast` attribute'unda saklanır
5. **WMO Kodları**: API'den gelen WMO weather code'ları Home Assistant condition'larına dönüştürülür

**Oluşturulan Entity:**
- `weather.haswave_hava_durumu` - Ana weather entity (sensor değil, weather entity)

**Sensor Oluşturmaz:** Bu entegrasyon sensor oluşturmaz, sadece bir weather entity oluşturur. Weather entity'ler Home Assistant'ın native hava durumu formatıdır ve `weather-forecast` kartları ile kullanılabilir.

### Home Assistant Weather Entity

Integration otomatik olarak şu weather entity'yi oluşturur:

#### `weather.haswave_hava_durumu`

**State:** Hava durumu durumu (clear-day, clear-night, partlycloudy, cloudy, fog, rainy, snowy, lightning, etc.)

**Attributes:**
- `temperature` - Sıcaklık (°C) - **Ana sıcaklık bilgisi**
- `apparent_temperature` - Hissedilen sıcaklık (°C) - **Alt bilgi olarak gösterilir**
- `humidity` - Nem (%)
- `pressure` - Basınç (hPa)
- `wind_speed` - Rüzgar hızı (km/h) - **Birim otomatik gösterilir**
- `wind_bearing` - Rüzgar yönü (°)
- `cloud_coverage` - Bulut örtüsü (%)
- `forecast` - Günlük tahmin array'i (7-16 gün)
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

**Not:** Eğer "Unknown type encountered: weather" hatası alırsanız:
1. Settings → Devices & Services → Entities
2. "haswave" ile arayın
3. Weather entity'yi bulun ve gerçek entity ID'yi kopyalayın
4. Dashboard kartında bu entity ID'yi kullanın

#### Weather Forecast Card (5 Günlük Tahmin)

Met.no gibi 5 günlük tahmin göstermek için:

```yaml
type: weather-forecast
entity: weather.haswave_hava_durumu
forecast_type: daily
```

**Tüm Özellikler:**

```yaml
type: weather-forecast
entity: weather.haswave_hava_durumu
forecast_type: daily  # Günlük tahmin (daily) veya saatlik tahmin (hourly)
name: 5 Günlük Hava Durumu
show_current: true  # Güncel hava durumunu göster
show_forecast: true  # Tahmini göster
number_of_forecasts: 5  # Gösterilecek maksimum tahmin sayısı (1-7 arası)
```

**Özellik Açıklamaları:**
- `forecast_type: daily` - Günlük tahmin (varsayılan) ✅
- `forecast_type: hourly` - Saatlik tahmin (şu an desteklenmiyor, sadece günlük)
- `show_current: true` - Güncel hava durumunu ve tahmini birlikte göster ✅
- `show_current: false` - Sadece tahmini göster
- `show_forecast: false` - Sadece güncel hava durumunu göster
- `number_of_forecasts: 5` - Gösterilecek maksimum tahmin sayısı (1-7 arası) ✅

**Not:** Weather entity düzgün çalışıyorsa, weather-forecast kartı otomatik olarak tüm bu özellikleri destekler. Kart ayarlarında (⋮ menüsü) bu seçenekleri görebilirsiniz.

**Not:** Entity ID farklıysa (örneğin `weather.haswave_hava_durumu_xxxxx`), yukarıdaki entity ID'yi kullanın.

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

#### Button-Card ile Mevcut Hava Durumu (Animasyonlu)

Mevcut hava durumunu animasyonlu icon ile göstermek için:

```yaml
type: custom:button-card
entity: weather.haswave_hava_durumu
show_name: true
show_state: false
styles:
  card:
    - padding: 20px
    - background: |
        [[[
          const condition = states['weather.haswave_hava_durumu'].state;
          if (condition.includes('rainy') || condition.includes('pouring')) return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
          if (condition.includes('snowy')) return 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
          if (condition.includes('clear')) return 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)';
          if (condition.includes('cloudy') || condition.includes('partlycloudy')) return 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)';
          return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        ]]]
custom_fields:
  icon: |
    [[[
      return (function() {
        // Lord-icon script'ini dinamik olarak yükle (entegrasyon ile birlikte gelir)
        if (!window.lordiconLoaded) {
          const script = document.createElement('script');
          script.src = '/local/lordicon.js';
          script.type = 'module';
          document.head.appendChild(script);
          window.lordiconLoaded = true;
        }
        
        const condition = states['weather.haswave_hava_durumu'].state;
        const iconMapping = {
          'clear-day': '/local/json/sun.json',
          'clear-night': '/local/json/moon.json',
          'partlycloudy': '/local/json/cloudy-sun.json',
          'cloudy': '/local/json/clouds.json',
          'fog': '/local/json/fog.json',
          'rainy': '/local/json/sun-rain.json',
          'pouring': '/local/json/storm.json',
          'snowy': '/local/json/snow.json',
          'snowy-rainy': '/local/json/snow-rain.json',
          'lightning': '/local/json/storm.json',
          'lightning-rainy': '/local/json/storm.json'
        };
        const iconPath = iconMapping[condition] || '/local/json/cloud.json';
        return `<lord-icon src="${iconPath}" trigger="loop" style="width:80px;height:80px;filter: brightness(0) invert(1);"></lord-icon>`;
      })();
    ]]]
  temp: |
    [[[
      const temp = states['weather.haswave_hava_durumu'].attributes.temperature;
      return `<div style="font-size: 48px; font-weight: bold; color: white; margin-top: 16px;">${Math.round(temp || 0)}°</div>`;
    ]]]
  details: |
    [[[
      const attrs = states['weather.haswave_hava_durumu'].attributes;
      return `
        <div style="display: flex; justify-content: space-around; margin-top: 16px; font-size: 14px; color: rgba(255,255,255,0.9);">
          <div>💧 ${attrs.humidity || 0}%</div>
          <div>🌬️ ${Math.round(attrs.wind_speed || 0)} km/h</div>
          <div>📊 ${attrs.pressure || 0} hPa</div>
        </div>
      `;
    ]]]
```

#### Button-Card ile 5 Günlük Tahmin (JSON Iconları ile)

Met.no gibi 5 günlük tahmini tek kartta göstermek için button-card kullanabilirsiniz:

```yaml
type: custom:button-card
entity: weather.haswave_hava_durumu
show_name: true
show_state: false
styles:
  card:
    - padding: 16px
    - background: |
        [[[
          const condition = states['weather.haswave_hava_durumu'].state;
          if (condition.includes('rainy') || condition.includes('pouring')) return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
          if (condition.includes('snowy')) return 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
          if (condition.includes('clear')) return 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)';
          if (condition.includes('cloudy') || condition.includes('partlycloudy')) return 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)';
          return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        ]]]
custom_fields:
  forecast: |
    [[[
      return (function() {
        // Lord-icon script'ini dinamik olarak yükle (entegrasyon ile birlikte gelir)
        if (!window.lordiconLoaded) {
          const script = document.createElement('script');
          script.src = '/local/lordicon.js';
          script.type = 'module';
          document.head.appendChild(script);
          window.lordiconLoaded = true;
        }
        
        const forecastData = states['weather.haswave_hava_durumu'].attributes.forecast || [];
        const iconMapping = {
          'clear-day': '/local/json/sun.json',
          'clear-night': '/local/json/moon.json',
          'partlycloudy': '/local/json/cloudy-sun.json',
          'cloudy': '/local/json/clouds.json',
          'fog': '/local/json/fog.json',
          'rainy': '/local/json/sun-rain.json',
          'pouring': '/local/json/storm.json',
          'snowy': '/local/json/snow.json',
          'snowy-rainy': '/local/json/snow-rain.json',
          'lightning': '/local/json/storm.json',
          'lightning-rainy': '/local/json/storm.json'
        };
        
        let resultHtml = '<div style="display: flex; justify-content: space-around; margin-top: 16px; flex-wrap: wrap; gap: 12px;">';
        
        for (let idx = 0; idx < Math.min(5, forecastData.length); idx++) {
          const forecastDay = forecastData[idx];
          if (!forecastDay || !forecastDay.datetime) continue;
          
          const dayDate = new Date(forecastDay.datetime);
          const dayNameStr = dayDate.toLocaleDateString('tr-TR', { weekday: 'short' });
          const iconPath = iconMapping[forecastDay.condition] || '/local/json/cloud.json';
          
          resultHtml += `
            <div style="text-align: center; min-width: 70px; padding: 8px; background: rgba(255,255,255,0.1); border-radius: 8px;">
              <div style="font-size: 11px; color: rgba(255,255,255,0.9); margin-bottom: 8px; font-weight: 500;">${dayNameStr}</div>
              <lord-icon src="${iconPath}" trigger="hover" style="width:40px;height:40px;filter: brightness(0) invert(1);"></lord-icon>
              <div style="font-size: 13px; font-weight: bold; color: white; margin-top: 8px;">
                ${Math.round(forecastDay.temperature || 0)}°<span style="font-size: 11px; opacity: 0.8;">/${Math.round(forecastDay.templow || 0)}°</span>
              </div>
              ${forecastDay.precipitation ? `<div style="font-size: 10px; color: rgba(255,255,255,0.8); margin-top: 4px;">💧 ${Math.round(forecastDay.precipitation)}mm</div>` : ''}
            </div>
          `;
        }
        
        resultHtml += '</div>';
        return resultHtml;
      })();
    ]]]
```

**Not:** 
- Bu örnekler için [button-card](https://github.com/custom-cards/button-card) eklentisini yüklemeniz gerekir
- **Lord-icon entegrasyon ile birlikte gelir**: `lordicon.js` dosyası entegrasyon ile birlikte `/local/lordicon.js` olarak yüklenir
- **JSON animasyonları entegrasyon ile birlikte gelir**: `/local/json/` klasöründeki animasyonlar otomatik olarak kullanılabilir
- **Otomatik yükleme**: Button-card örnekleri lord-icon script'ini otomatik olarak yükler, ek kurulum gerekmez
- Animasyonlar hava durumuna göre otomatik olarak değişir (güneşli, yağmurlu, karlı, vb.)
- Sıcaklık ve hava durumu bilgileri gerçek zamanlı olarak güncellenir

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
