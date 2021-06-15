# Tablecloth Generator
## _A tool to create tableclothes for the /mjg/ League easily_

| [![Screenshot](https://raw.githubusercontent.com/vg-mjg/tablecloth-generator/main/screenshot.png)]()  | [![Screenshot-2](https://raw.githubusercontent.com/vg-mjg/tablecloth-generator/main/screenshot-2.png)]()  | [![Screenshot-3](https://raw.githubusercontent.com/vg-mjg/tablecloth-generator/main/screenshot-3.png)]()  |
|:-:|:---:|:---:|
| *Blank version with no settings*  | *Preview window*  | *Team configuration screen*  |

This simple tool just lets you pick up the teams in their according seat and then generate the tablecloth. No PAINT.net required. Easy, right?

## Features
- No layer selection
- Pick the teams in their respective seating
- Generate and copy to your majsoul plus folder

## Installation

Download it from [releases](https://github.com/vg-mjg/tablecloth-generator/releases/), extract and run the .exe file.

*Will there be Linux releases?*

Probably not, unless someone else compiles it. You're welcome to do it in a Pull Request.

## Development

It was tested and compiled on Python 3.9. It is recommended to use [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/) for testing/compiling.

```sh
mkvirtualenv tablecloth-generator
```

Then run the `requirements.txt` to install the dependencies.

```sh
pip install -r requirements.txt
```

Finally run the `generator.py`:

```sh
python generator.py
```

#### Building for source

First rename `Tablecloth generator.spec.template` to `Tablecloth generator.spec`. Then edit the empty paths (marked as `<YOUR PATH>` and `<YOUR PYTHON/VIRTUALENV PATH>`). Then, add the optimization lines:

**(For Windows)**
```sh
set PYTHONOPTIMIZE=1
```
**(For Linux)**
```sh
PYTHONOPTIMIZE=1
```

Finally run it through `pyinstaller`:

```sh
pyinstaller "Tablecloth generator.spec"
```

## License

MIT

## TO-DO
- Improve the speed in which generates the Tablecloth.
- Fix the bug which only allows it first to generate as a .png.

## Contribute
Problems? Suggestions? Create an issue or. Pull requests are always welcomed.
