from pathlib import Path

PROMPT = '/code/sandbox$ '

BACKSPACE = '\x08\x1b[K'
RETURN = '\r\n'
CONTROL_L = '\x1b[H\x1b[2J'

FILE = Path(__file__)
ROOT = FILE.parents[2]

DOC_DIR = ROOT / 'doc'
SVG_DIR = DOC_DIR / 'movies'
CAST_DIR = ROOT / 'cast'
GENERATED_CAST_DIR = DOC_DIR / 'cast'
SCRIPT_DIR = ROOT / 'gitz_doc/cast/scripts'

SVG_SUFFIX = '.svg'
CAST_SUFFIX = '.cast'
SCRIPT_SUFFIX = '.sh'

HEADER = {'version': 2, 'width': 80, 'height': 32}


def cast_file(command):
    return (CAST_DIR / command).with_suffix(CAST_SUFFIX)


def generated_cast_file(command):
    return (GENERATED_CAST_DIR / command).with_suffix(CAST_SUFFIX)


def svg_file(command):
    return (SVG_DIR / command).with_suffix(SVG_SUFFIX)


def script_file(command):
    return (SCRIPT_DIR / command).with_suffix(SCRIPT_SUFFIX)


def cast_files():
    yield from (f for f in CAST_DIR.iterdir() if f.suffix == CAST_SUFFIX)


def script_files():
    yield from (f for f in SCRIPT_DIR.iterdir() if f.suffix == SCRIPT_SUFFIX)
