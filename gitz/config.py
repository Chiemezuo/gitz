from pathlib import Path
import sys

VERSION = '0.9.13'
HOME_PAGE = 'https://github.com/rec/gitz/blob/master/README.rst'

GITZ_DIRECTORY = Path(__file__).absolute().parent.parent
EXECUTABLE_DIRECTORY = Path(sys.argv[0]).absolute().parent

# In development and when running tests, GITZ_DIRECTORY and
# EXECUTABLE_DIRECTORY will be the same # but in a pip installation
# they will be different!


def _commands():
    def commands(d):
        return [f.name for f in d.iterdir() if f.name.startswith('git-')]

    return sorted(commands(GITZ_DIRECTORY) or commands(EXECUTABLE_DIRECTORY))


COMMANDS = _commands()
