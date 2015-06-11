import pickle
import os
import collections
from argparse import ArgumentParser

from tools import measure, findwords

DEFAULT_FILENAME = "index/trie.pickle"


class Trie(collections.UserDict):

  def __init__(self, char=None, word=None):
    self.char = char
    self.word = word
    super().__init__()

  def insert(self, word):
    node = self
    for char in word:
      if char not in node:
        node[char] = Trie(char)
      node = node[char]
    node.word = word

  def dump(self, filename):
    with open(filename, 'wb') as file:
      pickle.dump(self, file)

  @classmethod
  def build(cls, filename):
    root = Trie()
    with open(filename) as file:
      for line in file:
        word = line.strip()
        root.insert(word)
    return root

  @classmethod
  def load(cls, filename):
    with open(filename, 'rb') as file:
      root = pickle.load(file)
    return root

  def adjacents(self, word):
    adjacents = set()

    columns = len(word) + 1
    firstrow = list(range(columns))
    stack = [(v, firstrow) for v in self.values()]

    while stack:
      node, lastrow = stack.pop()
      row = [lastrow[0] + 1]
      for i in range(1,columns):
        addcost = row[i - 1] + 1
        delcost = lastrow[i] + 1
        subcost = lastrow[i - 1] + (word[i - 1] != node.char)
        row.append(min(addcost, delcost, subcost))

      if min(row) <= 1:
        stack.extend((v, row) for v in node.values())

      if node.word and node.word != word and row[-1] <= 1:
        adjacents.add(node.word)

    return adjacents


if __name__ == '__main__':
  default_dict = findwords()

  parser = ArgumentParser(__file__, description=__doc__)
  parser.add_argument('--dict', '-d',
                      default=default_dict, metavar="filename",
                      help="Dictionary file name (defaults to '%s')" % default_dict)
  parser.add_argument('--index', '-i',
                      default=DEFAULT_FILENAME, metavar="filename",
                      help="Index file name (defaults to '%s')" % DEFAULT_FILENAME)
  parser.add_argument('--verbose', '-v', action='store_true')
  args = parser.parse_args()

  with measure("Trie built", args.verbose):
    root = Trie.build(args.dict)

  with measure("Index saved", args.verbose):
    path = os.path.dirname(args.index)
    if not os.path.exists(path):
      os.makedirs(path)
    root.dump(args.index)
