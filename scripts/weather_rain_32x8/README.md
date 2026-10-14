# Weather rain 32×8 (v4.0)

A weather app for AWTRIX NG on a 32×8 display. It shows current weather, the moon phase,
and one of three values with a 15-hour colour forecast row underneath.

![Preview](preview.gif)

## Credits

Based on **Weather Script v3.7** by **.hank_the_tank** (AWTRIX Hub):
https://awtrix.de/script/fGEhP0cZZd6E

Weather app: Hank_the_Tank / Codex. Memory optimisation: with support from Blueforcer.
Weather data: [Open-Meteo](https://open-meteo.com/) (no API key needed).

Modifications by TJuTZu. The original author has been informed. Licence for the derived
code follows the original author's wishes. The MIT licence of this repository covers my
own additions only.

## What I changed

- Three switchable values: temperature, humidity and rain/snow
- The 15 bottom pixels (one per hour) follow the value on screen
- Humidity and rain/snow have their own colour scales
- The Open-Meteo request also fetches hourly humidity, precipitation, snowfall and current precipitation
- The `keep` response buffer is raised from 640 to 1100 bytes

## Display

| Area | Content |
| --- | --- |
| Left | Icon for current weather |
| Centre | Current value (temperature, humidity or rain) |
| Right | Moon-phase icon |
| Bottom | 15 pixels, one per hour, for the displayed value |

The enabled values rotate in this order: temperature, humidity, rain/snow. Each has the same
slide animation. If all three are off, temperature is shown anyway.

## Colour scales

**Temperature:** purple and dark blue (very cold), light blue (cool), green (mild), yellow (warm), orange and red (hot).

**Humidity:** orange (dry, about 20%), yellow, green (about 50%), blue (80% and above), deep blue (100%).

**Rain / snow** (mm/h):

| Type | Scale |
| --- | --- |
| Rain | Dry hours are dim blue, then light blue, blue, violet and magenta at 6 mm/h or more |
| Snow | Grey-blue up to bright white at about 3 mm/h water equivalent. Dry hours are dim grey. |

An hour counts as snow if at least half of its precipitation falls as snow. The rain value
is shown in mm/h with one decimal, for example `0.3`. If that is too wide, it drops the decimal.

The colour stops are in the `self.hs` (humidity), `self.rs` (rain) and `self.ss` (snow)
lists in `init()`.

## Settings (Apps tab → gear button)

| Setting | Default | Description |
| --- | --- | --- |
| Latitude | 52.52 | Location (default is Berlin) |
| Longitude | 13.40 | Location (default is Berlin) |
| Show temperature | on | Show temperature and its forecast row |
| Show humidity | on | Show humidity and its forecast row |
| Show rain / snow | on | Show current precipitation and its forecast row |

Saving new settings restarts the script. The middle button refreshes the weather data immediately.

## Required icons

Icons are not part of the script. Upload them to the device separately. They are attached to
the [original Hub page](https://awtrix.de/script/fGEhP0cZZd6E).

**Weather:**

| ID | Condition |
| --- | --- |
| 53386 | Clear sky |
| 2286 | Partly cloudy |
| 53384 | Overcast |
| 17055 | Fog |
| 2720 | Rain or drizzle |
| 2289 | Snow |
| 49300 | Rain showers |
| 29839 | Thunderstorm |
| 36637 | Unknown |

**Moon phases:** 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321

If a weather icon is missing, a small yellow sun is drawn. There is no fallback for a
missing moon icon.

## Requirements

- AWTRIX NG with scripting enabled and firmware 1.0.10-dev or newer (for the settings form)
- Wi-Fi and access to `api.open-meteo.com`
- The icons above on the device

## Troubleshooting

- **Only `...` is shown:** No valid data has been received yet. Check Wi-Fi, internet and the coordinates.
- **Red pixel at the bottom right:** The data is more than about 20 minutes old.
- **Out of memory or script crashes:** Lower `keep` from 1100 to about 1000.
- **`ERR:...`:** There is a script error. Check the message in the web interface and the device log.

## Status

Not widely tested. I have only run it on TC001 and AwtrixNG Version 1.2.2.
