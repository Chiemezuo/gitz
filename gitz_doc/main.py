from . import command_pages
from . import doc_index
from . import get_command_help
from . import manpages
from . import readme
from .cast import generated_movies
from .cast import recorded_movies
from gitz.program import ARGS
from gitz.program import PROGRAM

SYMBOLS = (
    ('command_pages', command_pages),
    ('doc_index', doc_index),
    ('generated_movies', generated_movies),
    ('manpages', manpages),
    ('readme', readme),
    ('recorded_movies', recorded_movies),
)


def add_arguments(parser):
    parser.add_argument('sections', nargs='*', help='Sections')


def main():
    help = get_command_help.get_command_help()
    sections = ARGS.sections
    for s, module in SYMBOLS:
        if not sections or any(s.startswith(i) for i in sections):
            module.main(help)
            print(s, 'done')


if __name__ == '__main__':
    PROGRAM.start()
