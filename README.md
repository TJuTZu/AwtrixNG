# AwtrixNG Playground

Experimental scripts for [AWTRIX NG](https://awtrix.de/) (32×8 LED matrix, e.g. Ulanzi TC001).
Some are original, some are modified versions of scripts from other authors. Each script's
folder says which, and credits the source.

## Scripts

| Script | Description | Based on |
| --- | --- | --- |
| [weather_rain_32x8](scripts/weather_rain_32x8/) | Weather with switchable temperature, humidity and rain/snow, each with a 15-hour colour forecast row | [Weather Script](https://awtrix.de/script/fGEhP0cZZd6E) by .hank_the_tank |

## Repository layout

```
AwtrinNG/
├── README.md
├── LICENSE
├── .gitignore
└── scripts/
    └── <script_name>/
        ├── <script_name>.ax
        ├── README.md
        └── preview.gif
```

## Usage

1. Copy the `.ax` file to your AWTRIX NG (web interface → scripts) or use the Hub installer.
2. Upload the icons listed in the script's README. They are not part of the script.
3. Open the Apps tab, press the gear button on the script's row and set its options.

Each script was tested on AWTRIX NG firmware `<version>`. Fill in your version.

## Licence and credits

- Original work in this repository is under the [MIT License](LICENSE).
- Scripts derived from other authors' work keep their credit in the script header and
  README. The MIT licence applies to my modifications only. The licence of the original
  parts is up to the original author.
- Weather data: [Open-Meteo](https://open-meteo.com/). Firmware: Blueforcer / AWTRIX NG.

## Contributing

Issues and suggestions are welcome. This is a playground, so things may change.
