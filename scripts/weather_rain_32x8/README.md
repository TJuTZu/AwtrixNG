# Weather rain 32×8 (v4.0)

Weather app for AWTRIX NG on a 32×8 display. It shows the current weather icon, the moon
phase and one of three values (temperature, humidity, rain/snow). A 15-pixel colour row
below shows the hourly forecast for the value on screen.

![Preview](awtrix-20261014153005.gif)

## Credits

Based on **Weather Script v3.7** by **.hank_the_tank**:
https://awtrix.de/script/fGEhP0cZZd6E

Original credits: weather app by Hank_the_Tank / Codex, memory optimisation with support
from Blueforcer. Weather data: [Open-Meteo](https://open-meteo.com/) (no API key needed).

Modifications by TJuTZu (with Claude). The original author has been informed. The licence
of the derived code follows the original author's wishes. The repository's MIT licence
covers only my own additions.

## What I changed

- Three switchable values: temperature, humidity and rain/snow
- The 15 forecast pixels follow the value on screen
- Colour scales for humidity and rain/snow, with rain and snow coloured differently
- The Open-Meteo request also fetches humidity, precipitation and snowfall
- The `keep` response buffer is raised from 640 to 1100 bytes

## Display

| Area | Content |
| --- | --- |
| Left | Icon for the current weather |
| Centre | Current value (temperature, humidity or rain), coloured by its value |
| Right | Moon-phase icon |
| Bottom (x 8–22) | 15 pixels, one per hour, for the value on screen |

Enabled values slide through in this order: temperature → humidity → rain/snow. If all three
are switched off, temperature is shown anyway.

## Settings (Apps tab → gear button)

| Setting | Default | Description |
| --- | --- | --- |
| Latitude | 52.52 | Location (default is Berlin) |
| Longitude | 13.40 | Location (default is Berlin) |
| Temperature unit | C | `C` or `F`. Only the displayed number changes. Colours and forecast stay based on °C. |
| Refresh | 15 min | Weather request interval (15–60 min) |
| Show temperature | on | Show temperature and its forecast row |
| Show humidity | on | Show humidity and its forecast row |
| Show rain / snow | on | Show current precipitation and its forecast row |
| Swap after | 3 s | How long each value stays before sliding to the next (1–10 s) |

Saved settings are stored on the device. The middle button requests fresh data immediately.

## Colour scales

**Temperature (°C):** purple and dark blue (very cold) → light blue (cool) → green (mild)
→ yellow (warm) → orange and red (hot).

**Humidity:** orange at 20% (dry) → yellow at 35% → green at 50% → light green at 65%
→ blue at 80% → deep blue at 100%.

**Rain / snow (mm/h):**

| Type | Scale |
| --- | --- |
| Rain | dim blue at 0 → light blue at 0.2 → blue at 1 → violet at 3 → magenta at 6 and above |
| Snow | dim grey at 0 → grey-blue at 0.2 → pale blue-white at 1 → bright white at 3 and above (water equivalent) |

An hour counts as snow if at least half of its precipitation falls as snow (Open-Meteo gives
snowfall in cm. 7 cm equals 10 mm of water). The rain value is shown in mm/h with one
decimal, for example `0.3`. If that is too wide it drops the decimal.

You can change the colour stops in the `self.st` (temperature), `self.hs` (humidity),
`self.rs` (rain) and `self.ss` (snow) lists in `init()`.

## Required icons

Icons are not part of the script. Download them from the
[original Hub page](https://awtrix.de/script/fGEhP0cZZd6E) and upload them to the device.
This script uses 17 of them.

**Weather**

| ID | Condition |
| --- | --- |
| 53386 | Clear sky |
| 2286 | Partly cloudy |
| 53384 | Overcast |
| 17055 | Fog |
| 2720 | Rain or drizzle |
| 2289 | Snow and snow showers |
| 49300 | Rain showers |
| 29839 | Thunderstorm |
| 36637 | Unknown |

**Moon phases:** 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321

If an icon is missing, the script draws a yellow circle (weather) or a grey circle (moon).
The Hub page also lists `3363`, `49299` and `49301`. This script doesn't use them.

## Requirements

- AWTRIX NG with scripting enabled, firmware `1.0.10-dev` or newer (for the settings form)
- Wi-Fi and access to `http://api.open-meteo.com`
- The icons above stored on the device
- Tested on: `TC001 and AwtrixNG Version 1.2.2.`

## Troubleshooting

- **Only `...` is shown:** No valid data has been received yet. Check Wi-Fi, internet and the coordinates.
- **Red pixel at the bottom right:** The last successful update is more than about 20 minutes old.
- **Rain/snow row always looks like rain, or stays empty:** The response may be cut off by the `keep` buffer. Check the device log.
- **Out of memory or crashes:** Lower `keep` from 1100 to about 1000. Check that the rain/snow row still works afterwards.
- **`ERR:...`:** There is a script error. See the message in the web interface and the device log.

Not widely tested. I have only run it on TC001 and AwtrixNG Version 1.2.2.
