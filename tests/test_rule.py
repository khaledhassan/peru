import unittest

from peru import cache
from peru import rule

import shared


class RuleTest(unittest.TestCase):

    def setUp(self):
        self.cache_dir = shared.create_dir()
        self.cache = cache.Cache(self.cache_dir)
        self.content = {'a': 'foo', 'b/c': 'bar'}
        self.content_dir = shared.create_dir(self.content)
        self.content_tree = self.cache.import_tree(self.content_dir)
        self.entries = self.cache.ls_tree(self.content_tree, recursive=True)

    def test_copy(self):
        # A file copied into a directory should be placed into that directory.
        # A directory or file copied into a file should overwrite that file.
        copies = {'a': ['x', 'b', 'b/c'], 'b': ['a', 'y']}
        tree = rule.copy_files(self.cache, self.content_tree, copies)
        shared.assert_tree_contents(self.cache, tree, {
            'a/c': 'bar',
            'b/a': 'foo',
            'b/c': 'foo',
            'x':   'foo',
            'y/c': 'bar',
        })

    def test_move(self):
        # Same semantics as copy above. Also, make sure that move deletes move
        # sources, but does not delete sources that were overwritten by the
        # target of another move.
        moves = {'a': 'b', 'b': 'a'}
        tree = rule.move_files(self.cache, self.content_tree, moves)
        shared.assert_tree_contents(self.cache, tree, {
            'a/c': 'bar',
            'b/a': 'foo',
        })
