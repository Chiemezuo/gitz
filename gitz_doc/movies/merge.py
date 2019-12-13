from . import constants
from gitz.program import safe_writer


def main(commands):
    for c in commands:
        mfile = constants.movies_file(c)
        mtime = mfile.exists() and mfile.stat().st_mtime or 0
        symbol = '.' if mtime else '?'
        generated = True

        for fn in constants.generated_svg_file, constants.recorded_svg_file:
            file = fn(c)
            if file.exists():
                if file.stat().st_mtime > mtime:
                    with safe_writer.safe_writer(mfile) as mf:
                        mf.write(file.read_text())
                    symbol = 'g' if generated else 'r'
                break
            generated = False

        print(symbol, mfile)
