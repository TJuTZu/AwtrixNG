# Weather Forecast for AWTRIX NG

An [AWTRIX NG](https://github.com/Blueforcer/awtrix3) script for 32×8 LED matrix clocks. It shows the current weather as an animated 8×8 icon that drifts across the display, and rotates through temperature, rain and wind. A one-pixel-high colour strip along the bottom shows a 32-hour forecast for whichever value is on screen.

Weather data comes from [Open-Meteo](https://open-meteo.com/). No API key is needed.

> **Status:** version 8.0. TODO: add the devices and firmware versions you have tested on, and add screenshots or photos.

## Features

- **One animated icon per weather type.** Sun, partly cloudy, cloud, fog, drizzle, rain, heavy rain, sleet, snow and thunder. At night the sun is replaced by the moon in its current phase.
- **Drifting background icon.** The icon enters from the left edge, leaves at the right edge and starts again. The speed is adjustable.
- **Rotating values.** Temperature, rain and wind each get their own show time and can be switched on or off separately.
- **32-hour forecast strip.** The bottom row has one pixel per hour, coloured by the value that is currently displayed.
- **Rain shown as `current / 32 h total`**, for example `0.3 / 12.4`, with no unit text. Each number has the colour of its amount.
- **Wind speed with a 5-pixel direction arrow** that has a 3-pixel arrowhead. The arrow can point to where the wind blows or where it comes from.
- **Units:** °C or °F, wind in m/s, km/h, mph or knots, rain in mm or inches.
- **Rain from the current conditions.** If the weather code says clear or cloudy but rain is falling right now, the icon switches to a rain or snow icon.
- **Stale-data indicator.** A red pixel in the top-right corner means the last successful update is too old.

## How it looks

```text
 32 px wide
┌────────┬────────────────────────┐
│ 8x8    │  value (rotates)       │   rows 0-6
│ icon   │  5°C / 0.3 / 12.4 / 7→ │
│ drifts │                        │
│ across │                        │
├────────┴────────────────────────┤
│ 32-hour colour forecast strip   │   row 7
└─────────────────────────────────┘
```

The icon moves behind the text. By default the text has a black outline so that it stays readable on top of the icon. The outline can be turned off.

### Rotating values

| Value | Example | Colour |
|---|---|---|
| Temperature | `5°C`, `-12°F` | Temperature scale |
| Rain | `0.3 / 12.4` | Rain scale for the current rate, rain scale for the 32 h total |
| Wind | `7` and an arrow | Wind speed scale |

- **Temperature** is rounded to whole degrees and limited to −50…+50 °C. The sign is shown only below zero. The colours always follow the Celsius value, so the strip looks the same in °C and °F.
- **Rain** has two numbers: the rain falling now and the total for the next 32 hours. The values are in mm with one decimal, or in inches with two decimals. If the numbers do not fit, leading zeros are dropped and the gaps shrink. The `/` is grey.
  - **Auto mode** shows rain only when the 32-hour total reaches the threshold set in `minrain`. If it does not, rain is skipped in the rotation.
  - **Always on** shows the rain value even when it is `0.0 / 0.0`.
- **Wind** is the speed as a whole number followed by a 5×5 pixel arrow with eight directions. The speed and the arrow have the same colour.

If all three values are switched off, the temperature is shown anyway.

### Forecast strip

The bottom row (y = 7) has one pixel per hour for the next 32 hours, starting from the current hour. It follows the value on screen, and during the slide between two values it switches to the incoming one.

| Strip | Colours based on |
|---|---|
| Temperature | Hourly temperature, on the temperature scale |
| Rain | Hourly precipitation. Rain and snow have separate colour scales. |
| Wind | Hourly wind speed, on the wind scale |

An hour counts as snow when at least half of its water comes as snow. Open-Meteo reports snowfall in cm, and the script converts it to water equivalent with cm / 0.7 = mm.

### Colour scales

Colours are interpolated between the stops.

**Temperature (°C)**

| °C | −12 | −6 | −1 | 0 | 4 | 10 | 15 | 21 | 27 | 32 | 38 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Colour | pink | violet | indigo | pale pink | cyan | green | lime | yellow | orange | red | dark red |

**Rain (mm/h)**: dim blue (0), light blue (0.2), blue (1), violet (3), magenta (6).
**Snow (mm/h, water equivalent)**: dim grey (0), grey-blue (0.2), light blue-white (1), white (3).
**Wind (m/s)**: dull blue (0), cyan (3), green (6), yellow (10), orange (14), red (18), magenta (25), white (33).

Wind colours are always computed from m/s, so changing the wind unit does not change the colours. The rain colours are always computed from mm.

## Weather icons

The icon is chosen from the WMO weather code returned by Open-Meteo.

| Weather code | Icon |
|---|---|
| 0, 1 | `WxSun` (day) or `WxMoon0`…`WxMoon7` (night) |
| 2 | `WxSunPart` or `WxMoon0Part`…`WxMoon7Part` |
| 3 | `WxCloud` |
| 45, 48 | `WxCloudFog` |
| 51–55 | `WxCloudDrizzle` |
| 56, 57, 66, 67 | `WxCloudSleet` |
| 61, 63, 80, 81 | `WxCloudRain` |
| 65, 82 | `WxCloudHeavy` |
| 71–77, 85, 86 | `WxCloudSnow` |
| 95–99 | `WxCloudThunder` |

**Rain override.** Weather models do not always agree with the precipitation values. If the code is 0–3 but the current precipitation is above zero, the icon is chosen from the precipitation instead:

| Current precipitation | Icon |
|---|---|
| Snow is at least half of it | `WxCloudSnow` |
| below 0.3 mm | `WxCloudDrizzle` |
| 0.3 mm to below 3 mm | `WxCloudRain` |
| 3 mm or more | `WxCloudHeavy` |

**Moon phase** is calculated from the date, so no network access is needed for it. The night icon is used when Open-Meteo reports `is_day = 0`. The lit side of the moon is drawn as seen from the northern hemisphere.

If an icon file is missing, a grey circle is drawn in its place and the script keeps running.

### Why each icon is a complete picture

AWTRIX NG GIFs keep the previous frame's pixels where a frame is transparent, and stacking several transparent GIFs is not documented to work. For that reason each weather type is one GIF that paints all 64 pixels. Sun and moon fill the whole 8×8 tile. There are 26 icons, about 8 KB in total, and every animation uses 16 frames with a 100 ms delay.

## Installation

### 1. Create the icons

`make_weather_icons.py` generates all 26 GIFs. It needs only Python 3 and has its own GIF writer.

```bash
python3 make_weather_icons.py icons
# optional contact sheet of every frame (needs Pillow):
python3 make_weather_icons.py icons --preview
```

Upload all `Wx*.gif` files to the `/ICONS` folder of the clock, for example through the web interface.

### 2. Install the script

Add `weather_forecast` (the script file in this repository, TODO: confirm file name) to your AWTRIX NG scripts and set your latitude and longitude. The default location is Helsinki.

### 3. Refresh by hand

Pressing the `select` button fetches new data immediately. Use it after changing the settings that are read at fetch time (see the notes below).

## Settings

| Setting | Default | Description |
|---|---|---|
| `lat`, `lon` | 60.1699, 24.9384 (Helsinki) | Location |
| `every` | 15 min | Refresh interval, 15–60 min |
| `speed` | 1 px/s | Icon speed, 0–10 px/s. 0 keeps the icon still at the left edge. |
| `outline` | on | Black outline around text and arrow |
| `showtemp` | on | Show temperature |
| `ttime` | 4 s | Temperature show time |
| `unit` | C | Temperature unit: `C` or `F` |
| `showrain` | on | Show rain |
| `rtime` | 3 s | Rain show time |
| `rainalways` | off | Off = auto (see below), on = always show rain |
| `minrain` | 0.2 mm | Auto mode threshold for the 32 h total, always in mm |
| `rainunit` | mm | Rain unit: `mm` or `in` |
| `showwind` | on | Show wind |
| `wtime` | 3 s | Wind show time |
| `windunit` | ms | Wind speed unit: `ms`, `kmh`, `mph` or `kn` |
| `winddir` | To | `To`: the arrow points where the wind blows. `From`: the arrow points where it comes from. |

Notes:

- **Read at each fetch:** `showtemp`, `showrain`, `showwind`, `unit`, `windunit`, `winddir`, `rainalways`, `minrain`.
- **Read at start-up:** `ttime`, `rtime`, `wtime`, `speed`, `outline`, `every`, `rainunit`. Save the script again to apply them.
- Each value is shown for its own show time, followed by a 400 ms slide to the next one. With the default times, a full rotation of temperature, rain and wind takes 11.2 s.
- One full pass of the icon takes (32 + 8) pixels, which is 40 s at the default speed.

## How it works

The script makes one HTTP request per refresh to Open-Meteo:

- **Current:** temperature, weather code, day/night, precipitation, snowfall, wind speed and wind direction
- **Hourly, 32 hours:** temperature, precipitation, snowfall and wind speed
- The wind speed is always requested in m/s and converted for display, so the colours do not depend on the chosen unit.

Details of the implementation:

- The response is trimmed on the device. The script asks the HTTP client to start from the `"current":` block and keep 1700 bytes. The largest response we calculated for this request is about 1480 bytes from that point on, so the buffer is large enough.
- The values are read with regular expressions, not a JSON parser, to keep memory use low.
- The icon moves with the clock. Its position advances only while the app is on screen.
- If a request fails or the answer is incomplete, the script tries again after 60 seconds instead of waiting for the whole refresh interval.
- If the last successful update is older than the refresh interval plus 5 minutes, the pixel in the top-right corner turns red.
- The first time the script runs, `...` is shown until the first successful fetch.

## Troubleshooting

- **`heap too fragmented to compile`**. The clock does not have a large enough block of free memory. Restart the clock and save the script right away. If the same script is already installed, saving a new version over it needs less memory than a new install. If that is not enough, remove the comments, or turn off the `outline` option and delete the `tx()` outline code.
- **Grey circle instead of the icon.** The icon file is missing or its name does not match. Names are case-sensitive.
- **The sun shows while it rains.** Check what the model returns for your location:

  ```text
  http://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&current=temperature_2m,weather_code,is_day,precipitation,snowfall&timezone=auto
  ```

  If `weather_code` is 0–2 and `precipitation` is `0.00`, the model reports dry weather and the icon is correct. If `precipitation` is above zero and the sun still shows, press `select` to refresh the data and check the settings.
- **A moon icon shows during the day.** `is_day` is 0 from Open-Meteo. Check the coordinates.
- **Wrong arrow direction.** Switch `winddir` between `To` and `From`.
- **Testing other weather.** Pick a location where the weather is what you want to see. To force a certain icon, set `self.code` just before `self.build()` in `on_body()`, for example `self.code = 95` for thunder. Remove the line afterwards.

## Limitations

- The weather data is model data, not a measurement at your location.
- The forecast strip has one pixel per hour and starts from the current hour. Its first pixel is the forecast for this hour, not a measured value.
- The arrow has eight directions, because a 5×5 pixel arrow cannot show finer steps.
- Rain amounts are shown with the precision of one decimal in mm, so very small amounts appear as `0.0`.

## Credits and licence

- Based on **Weather Script 3.7** by `.hank_the_tank` from the AWTRIX Hub: <https://awtrix.de/script/fGEhP0cZZd6E>
- Rewritten and extended by TJuTZu with Claude (Anthropic).
- Weather data by [Open-Meteo.com](https://open-meteo.com/), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Open-Meteo's free API is for non-commercial use, so check their terms before using it commercially.
- Licence: TODO. The original author asked that derived code follows their wishes, so check the licence of the original script before choosing one.
