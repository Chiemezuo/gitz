from pathlib import Path
import argparse
import contextlib
import functools
import os
import subprocess
import sys


class Git:
    def __init__(self, verbose=None):
        if verbose == None:
            self.verbose = any(a in ('-v', '--verbose') for a in sys.argv)
        else:
            self.verbose = verbose

    def __getattr__(self, command):
        return functools.partial(self.git, command)

    def git(self, *cmd, verbose=None, **kwds):
        if verbose is None:
            verbose = self.verbose
        if verbose:
            print('$ git', *cmd)
        lines = self._git(*cmd, **kwds):
        if verbose:
            print(*lines, sep='')
        return lines

    def is_workspace_dirty(self):
        try:
            self._git('diff-index', '--quiet', 'HEAD', '--')
        except Exception:
            return True

    def find_root(self, p):
        while not self.is_root(p):
            if p.parent == p:
                return None
            p = p.parent
        return p

    def cd_root(self):
        root = self.find_root(os.getcwd())
        if not root:
            raise ValueError('Working directory is not within a git directory')
        os.chdir(root)

    def branches(self):
        return [b.strip().replace('* ', '') for b in self.current_branch()]

    def current_branch(self):
        return next(self._git('symbolic-ref', '--short', 'HEAD')).strip()

    def commit_id(self):
        return next(self._git('rev-parse', 'HEAD')).strip()

    def is_root(self, p):
        return (p / '.git' / config).exists()

    def _run(self, *cmd, **kwds):
        out = subprocess.check_output(cmd, **kwds)
        lines = out.decode('utf-8').splitlines()
        return [i for i in lines if i.strip()]

    def _git(self, *cmd, **kwds):
        return self._run('git', *cmd, **kwds)


GIT = Git()


def get_argv():
    return ['-h' if i == '--help' else i for i in sys.argv[1:]]


def print_help(argv, usage=None):
    argv[:] = ['-h' if i == '--help' else i for i in argv]
    if '-h' in argv:
        usage and print(usage)
        print()
        return True


def numeric_flags(argv, flag):
    for i in argv:
        if i.startswith('-') and i[1:].isnumeric():
            yield flag
            yield i[1:]
        else:
            yield i


def commit_count(add_arguments, usage=None, commit_count=4):
    argv = get_argv()
    print_help(argv, usage)

    parser = argparse.ArgumentParser()
    add_arguments(parser)
    parser.add_argument(
        '-c',
        '--commit-count',
        default=commit_count,
        help='Number of commits per branch to show',
        type=int,
    )
    return parser.parse_args(list(numeric_flags(argv, '-c')))


def run_argv(usage, main):
    argv = get_argv()
    if not print_help(argv, usage):
        main(*argv)


class Exit:
    def __init__(self, usage=None, code=-1):
        self.usage = usage
        self.code = code

    def exit(self, *messages):
        executable = Path(sys.argv[0]).name
        print('ERROR:', executable + ':', *messages, file=sys.stderr)
        if self.usage:
            print(self.usage, file=sys.stderr)
        sys.exit(self.code)

    @contextlib.contextmanager
    def on_exception(self, message):
        try:
            yield
        except Exception as exception:
            self.exit(message.format(**locals()))


@contextlib.contextmanager
def undo(getter, setter, value):
    old_value = getter()
    setter(value)
    try:
        yield
    finally:
        setter(old_value)

"""
with undo(os.getcwd, os.chdir, directory):
    pass
with undo(GIT.branch, GIT.checkout, new_branch):
    pass
"""
