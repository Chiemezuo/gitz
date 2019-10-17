from . import parser
from . import runner
from pathlib import Path
import collections
import sys
import traceback

_ERROR_PROTECTED_BRANCHES = 'The branches %s are protected'


class _Program:
    ALLOW_NO_RUN = True

    def __init__(self):
        self.code = -1
        self.executable = Path(sys.argv[0]).name
        self.argv = sys.argv[1:]
        self.called = collections.Counter()

    def start(self, context=None):
        if context is None:
            context = vars(sys.modules['__main__'])
        self.args, self.log = parser.parse(self, **context)
        no_run = self.ALLOW_NO_RUN and self.args.no_run
        runner.RUN.start(self.log, no_run)
        runner.RUN_INFO.start(self.log)

        self.run_info = runner.RUN_INFO
        self.run = runner.RUN

        exe = self.executable.replace('-', '_')
        main = context.get(exe) or context.get('main')
        if not main:
            self.exit('No method named', exe, 'or main in', self.executable)

        try:
            main()

        except Exception as e:
            self.log.verbose(traceback.format_exc(), file=sys.stderr)
            self.exit('%s: %s' % (e.__class__.__name__, e))

    def exit(self, *messages):
        if messages:
            self.error(*messages)
        sys.exit(self.code)

    def error(self, *messages):
        self._error(messages, 'error')

    def error_if(self, errors, message, singular='branch', plural='branches'):
        if errors:
            s = singular if len(errors) == 1 else plural
            self._error([message, s, ', '.join(errors)], 'error')
            return True

    def message(self, *messages):
        self.log.message(*messages)

    def _error(self, messages, category):
        caption = self.executable + ':'
        self.called[category] += 1
        caption = category.upper() + ': ' + caption
        self.log.error(caption, *messages, file=sys.stderr)


PROGRAM = _Program()
