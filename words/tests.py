import unittest
import os
from itertools import combinations_with_replacement


from query import search, levenshtein
from index import Trie, DEFAULT_FILENAME


WORDS_FILENAME = '/tmp/words'
WORDS_CONTENT = "aa ab bb bc c".replace(' ', "\n")
WORDS = WORDS_CONTENT.split()

class TestIndex(unittest.TestCase):

  def test_build(self):
    index = Trie.build(WORDS_FILENAME)
    self.assertTrue(index)

  def test_persistence(self):
    index = Trie.build(WORDS_FILENAME)
    self.assertTrue(index)

    index.dump(DEFAULT_FILENAME)
    self.assertTrue(os.path.isfile(DEFAULT_FILENAME))

    index2 = Trie.load(DEFAULT_FILENAME)
    self.assertEqual(index, index2)

  def test_adjacency_manual(self):
    tests = {
      'a': {'ab', 'aa', 'c'},
      'aa': {'ab'},
      'bb': {'bc', 'ab'},
      'cc': {'c', 'bc'},
      'c': {'bc'},
    }
    self._test_adjacency(tests)


  def test_adjacency_auto(self):
    tests = dict()
    combinations = []
    for n in range(4):
      combinations.extend(combinations_with_replacement("".join(WORDS), 3))
    for combination in combinations:
      cword = "".join(combination)
      adjacents = set()
      for word in WORDS:
        if word != cword and adjacency(word, cword):
          adjacents.add(word)
      tests[cword] = adjacents
    self._test_adjacency(tests)

  def _test_adjacency(self, tests):
    index = Trie.build(WORDS_FILENAME)
    for word, test_adjacents in tests.items():
      adjacents = index.adjacents(word)
      msg = "adj('%s') = %s, it should be %s" % (word, adjacents, test_adjacents)
      self.assertEqual(adjacents, test_adjacents, msg)


class TestQuery(unittest.TestCase):
  def test_levenshtein(self):
    a = 'a'
    tests = [('a', 0), ('b', 1), ('ab', 1), ('ba', 1), ('aaa', 2), ('bbb', 3)]
    for b, test in tests:
      result = levenshtein(a, b)
      msg = "lev('%s', '%s') = %i, it should be %i" % (a, b, result, test)
      self.assertEqual(result, test, msg)

  def test_search(self):
    index = Trie.build(WORDS_FILENAME)
    tests = [
      ['a', 'c'],
      ['a', 'ab', 'bb', 'bc', 'c'],
      ['a', 'aa', 'ab', 'bb', 'bc', 'c'],
    ]
    paths = list(search(index, 'a', 'c'))
    self.assertEqual(paths, tests)

    #limit
    paths2 = list(search(index, 'a', 'c', 2))
    self.assertEqual(paths2, tests[:2])


def adjacency(a, b):
  lendiff = len(a) - len(b)

  if lendiff is 0:
    distance = 0
    for i in range(len(a)):
      distance += a[i] != b[i]
      if distance > 1:
        return False
    return True

  if abs(lendiff) is 1:
    if lendiff > 0:
      a, b = b, a
    for i in range(len(a)):
      if a[i] != b[i]:
        for j in range(i, len(a)):
          if a[j] != b[j+1]:
            return False
    return True

  return False

if __name__ == '__main__':
  with open(WORDS_FILENAME, 'wt') as file:
    file.writelines(WORDS_CONTENT)
  unittest.main()
  os.remove(WORDS_FILENAME)
