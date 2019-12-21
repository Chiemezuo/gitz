from . import constants
from . import render
from . import script_runner
from .. import worker
from gitz.program import safe_writer
from pathlib import Path
from test import repo

COMMITS = 'one', 'two', 'three', 'four', 'five'
ROOT = Path(__file__).parent
PARALLELISM = 5


def main(commands):
    if PARALLELISM:
        worker.work_on(_one_movie, commands, PARALLELISM, print)
    else:
        for command in commands:
            print(*_one_movie(command))


def _one_movie(command):
    target = constants.command_file(command, 'svg')
    source = constants.command_file(command, 'sh')
    cast_file = constants.command_file(command, 'cast')
    if not source.exists():
        return ('?', target)

    if target.exists():
        src = tuple(f for f in ROOT.iterdir() if f.suffix == '.py')
        newest = max(f.stat().st_mtime for f in src + (source,))
        if target.stat().st_mtime >= newest:
            return '.', target

    safe_writer.make_parents(target)
    with repo.clone_context():
        cast = script_runner.run(source)
        cast.write(cast_file)
        render.render(cast, target)

    return '+', target
