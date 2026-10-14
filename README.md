# AwtrixNG Playground

Experimental scripts for [AWTRIX NG](https://awtrix.de/) (32×8 LED matrix, e.g. Ulanzi TC001).
Some are original, some are modified versions of other authors' scripts. Each script's folder
says which, and credits the source.

## Scripts

| Script | Description | Based on |
| --- | --- | --- |
| [weather_rain_32x8](scripts/weather_rain_32x8/) | Weather with switchable temperature, humidity and rain/snow, each with a 15-hour colour forecast row | [Weather Script](https://awtrix.de/script/fGEhP0cZZd6E) by .hank_the_tank |

## Layout

```
AwtrixNG/
├── README.md
├── LICENSE
├── .gitignore
└── scripts/
    └── <script_name>/
        ├── <script_name>.ax
        ├── README.md
        └── preview.gif
```

## Licence and credits

- My own original work here is under the [MIT License](LICENSE).
- Scripts derived from other authors' work keep their credit in the script header and
  README. The MIT licence covers only my modifications. The licence of the original parts
  is up to the original author.
- Weather data: [Open-Meteo](https://open-meteo.com/). Firmware: Blueforcer / AWTRIX NG.

## Contributing

Issues and suggestions are welcome. This is a playground, so things may change.
