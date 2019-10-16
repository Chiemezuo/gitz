from . import repo
from gitz import config
from gitz.program import PROGRAM
import unittest


class GitGitzTest(unittest.TestCase):
    maxDiff = 100000

    @repo.test
    def test_all(self):
        self.assertEqual(PROGRAM.git_info.gitz(), RESULTS)

    @repo.test
    def test_version(self):
        for v in 'v', 've', 'version':
            self.assertEqual(PROGRAM.git_info.gitz(v), [config.VERSION])

    @repo.test
    def test_commands(self):
        for c in 'c', 'com', 'commands':
            self.assertEqual(PROGRAM.git_info.gitz(c), list(config.COMMANDS))

    @repo.test
    def test_executable_directory(self):
        # The configs for the child process and for us are different!
        for d in 'e', 'exec', 'executable_directory':
            self.assertEqual(
                PROGRAM.git_info.gitz(d),
                [str(config.LIBRARY_DIRECTORY.parent)],
            )

    @repo.test
    def test_library_directory(self):
        for d in 'l', 'lib', 'library_directory':
            self.assertEqual(
                PROGRAM.git_info.gitz(d), [str(config.LIBRARY_DIRECTORY)]
            )

    @repo.test
    def test_defaults(self):
        for d in 'd', 'def', 'defaults':
            self.assertEqual(PROGRAM.git_info.gitz(d), DEFAULTS)

    @repo.test
    def test_error(self):
        with self.assertRaises(ValueError):
            PROGRAM.git_info.gitz('var')

        with self.assertRaises(ValueError):
            PROGRAM.git_info.gitz('Com')


COMMANDS = '\n'.join('    ' + i for i in config.COMMANDS)
HOME_PAGE = config.HOME_PAGE
EXECUTABLE_DIRECTORY = str(config.LIBRARY_DIRECTORY.parent)
LIBRARY_DIRECTORY = str(config.LIBRARY_DIRECTORY)
VERSION = config.VERSION

RESULTS = """\
Commands:
{COMMANDS}

Defaults:
    GITZ_ORIGIN = ['origin']
    GITZ_PROTECTED_BRANCHES = ['develop', 'master', 'release']
    GITZ_PROTECTED_REMOTES = ['upstream']
    GITZ_REFERENCE_BRANCHES = ['develop', 'master']
    GITZ_UPSTREAM = ['upstream', 'origin']

Executable directory:
    {EXECUTABLE_DIRECTORY}

Home page:
    {HOME_PAGE}

Library directory:
    {LIBRARY_DIRECTORY}

Version:
    {VERSION}
""".format(
    **globals()
).splitlines()

DEFAULTS = """\
GITZ_ORIGIN = ['origin']
GITZ_PROTECTED_BRANCHES = ['develop', 'master', 'release']
GITZ_PROTECTED_REMOTES = ['upstream']
GITZ_REFERENCE_BRANCHES = ['develop', 'master']
GITZ_UPSTREAM = ['upstream', 'origin']
""".splitlines()
