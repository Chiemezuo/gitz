from . import dirs
from .. import config
from docutils.core import publish_file, default_description
from docutils.writers import manpage
import datetime
import io

# Taken from rst2man.py

DESCRIPTION = ('Generates unix manual pages for gitz. ' + default_description)
HEADINGS = 'Positional arguments', 'Optional arguments'

FMT = '.TH GIT-{command} 1 "{date}" "Gitz {version}" "Gitz Manual"\n'


def main(commands):
    for command in commands:
        src = (dirs.DOC / command).with_suffix('.rst')
        dest = (dirs.MAN / command).with_suffix('.1')

        # Simplify the RST a bit so rst2man understands it
        contents = fix_rst(src)

        publish_file(
            writer=manpage.Writer(),
            source=io.StringIO(contents),
            source_path=str(src),
            destination=dest.open('w'),
        )

        # Fix the results
        with dest.open() as fp:
            lines = fix_manpage(fp)

        with dest.open('w') as fp:
            fp.writelines(lines)


def fix_rst(src):
    lines = []
    in_examples = False
    examples = []

    def pop_example_stack():
        for example in examples[1:]:
            lines.extend((example, '    (same)', ''))
        examples.clear()

    for line in src.open():
        line = line[:-1]
        lines.append(line)
        if line in HEADINGS:
            lines.append('=' * len(line))
        elif not in_examples:
            in_examples = (line == 'EXAMPLES')
        elif line.startswith('`'):
            if examples:
                lines.pop()
            examples.append(line)
        elif not line.strip():
            pop_example_stack()
    if examples[1:]:
        lines.append('')
    pop_example_stack()

    return '\n'.join(lines) + '\n'


def fix_manpage(lines):
    lines = list(lines)
    for i, line in enumerate(lines):
        if line.startswith('.TH'):
            command = line.split()[2].strip(':')
            date = format(datetime.datetime.now(), '%d %B, %Y')
            version = config.VERSION
            lines[i] = FMT.format(**locals())

        elif line.startswith('git '):
            lines[i] = line.replace(r' \-', '')
            return lines