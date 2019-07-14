from . import util
from .env import ENV
from .git import GIT
from .program import Program

_ERROR_CHANGES_OVERWRITTEN = 'Your local changes would be overwritten'
_ERROR_NOT_GIT_REPOSITORY = (
    'fatal: not a git repository (or any of the parent directories): .git'
)
_ERROR_PROTECTED_BRANCHES = 'The branches %s are protected'


class GitProgram(Program):
    def require_git(self):
        if not util.find_git_root():
            self.error(_ERROR_NOT_GIT_REPOSITORY)
            self.exit()

    def require_clean_workspace(self):
        self.require_git()
        if GIT.is_workspace_dirty():
            self.error(_ERROR_CHANGES_OVERWRITTEN)
            self.exit()

    def require_unprotected_branches(self, *branches):
        pb = ENV.protected_branches()
        if set(pb.split(':')).intersection(branches):
            self.error(_ERROR_PROTECTED_BRANCHES % pb)
            self.exit()
