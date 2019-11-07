from . import command_pages  # noqa: F401
from . import doc_index  # noqa: F401
from . import get_command_help  # noqa: F401
from . import manpages  # noqa: F401
from . import movies  # noqa: F401
from . import readme  # noqa: F401
from gitz.program import ARGS
from gitz.program import PROGRAM

SYMBOLS = 'doc_index command_pages readme manpages movies'.split()


def add_arguments(parser):
    parser.add_argument('sections', nargs='*', help='Sections')


def main():
    help = get_command_help.get_command_help()
    sections = ARGS.sections
    for s in SYMBOLS:
        if not sections or any(s.startswith(i) for i in sections):
            globals()[s].main(help)
            print(s, 'done')


if __name__ == '__main__':
    PROGRAM.start()
