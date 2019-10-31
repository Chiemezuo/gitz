from . import repo
from gitz.git import functions
from gitz.git import GIT
import unittest


class GitCopyTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT.new('one')
        GIT.copy('two', '-v')
        expected = {'origin': ['master', 'one', 'two'], 'upstream': ['master']}
        self.assertEqual(functions.remote_branches(), expected)
