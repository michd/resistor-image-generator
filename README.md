## Resistor image generator

I got [nerdsniped](https://xkcd.com/356/) into making this.

Requires "Pillow".

This script generates a folder with a bunch of images following a given E-series of preferred numbers, along several decades.

See [E series of preferred numbers](https://en.wikipedia.org/wiki/E_series_of_preferred_numbers) on Wikipedia for more info.

All E-series (E3, E6, E12, E24, E96, and E192) are supported. Tolerances can be set to one of:

- 0.02%
- 0.05%
- 0.1%
- 0.25%
- 0.5%
- 1%
- 2%
- 5%
- 10%
- 20%

Tolerances are limited to the maximum tolerance for a given E-series.

Images will be placed in a directory named after the series in the current directory. Files are named with `<resistor value>_<tolerance>pct.png`. The resistor value is written in the convential way with suffixes: if the value is less than 1,000 ohms, `R`; if it's more than 1,000 ohms but less than 1,000,000: `k`; if it's more than 1,000,000: `M`

The script doesn't accept any arguments; to generate a different series or at a different tolerance, edit the last line of main.py.

You can also edit several of the variables to change the dimensions of the generated images. The maths are done in a way so it should be pretty adaptable.

Apologies for the somewhat messy code (particularly all the global variables). This was just a little fun project and I have no intent to build anything further from it.

