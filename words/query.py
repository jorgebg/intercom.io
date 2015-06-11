import heapq
import collections
import functools
from argparse import ArgumentParser

from index import DEFAULT_FILENAME, Trie
from tools import measure



def search(graph, start, goal, limit=None):
  Node = collections.namedtuple('Node', ['word', 'path'])

  stack = []
  heapq.heappush(stack, (0, Node(start, [start])))

  while stack:
    cost, current = heapq.heappop(stack)

    if current.word == goal:
      break

    for adjacent in graph.adjacents(current.word):
      if adjacent not in current.path:
        priority = cost + levenshtein(goal, adjacent)
        path = current.path + [adjacent]
        if adjacent == goal:
          yield path
          if limit is 1:
            stack = None
            break
          elif limit:
            limit -= 1
        else:
          heapq.heappush(stack, (priority, Node(adjacent, path)))


@functools.lru_cache()
def levenshtein(s1, s2):
  if len(s1) < len(s2):
    return levenshtein(s2, s1)

  if len(s2) == 0:
    return len(s1)

  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
    current_row = [i + 1]
    for j, c2 in enumerate(s2):
      insertions = previous_row[j + 1] + 1
      deletions = current_row[j] + 1
      substitutions = previous_row[j] + (c1 != c2)
      current_row.append(min(insertions, deletions, substitutions))
    previous_row = current_row

  return previous_row[-1]



if __name__ == '__main__':
  parser = ArgumentParser(__file__, description=__doc__)
  parser.add_argument('START')
  parser.add_argument('GOAL')
  parser.add_argument('--limit', '-l',
    type=int, metavar="N",
    help="Limit number of paths to find (no limit by default)")
  parser.add_argument('--index', '-t',
    default=DEFAULT_FILENAME, metavar="filename",
    help="Index file name (defaults to '%s')" % DEFAULT_FILENAME)
  parser.add_argument('--verbose', '-v', action='store_true')
  args = parser.parse_args()

  try:
    with measure("Index loaded", args.verbose):
      index = Trie.load(args.index)
  except:
    parser.error("Index file not found. Please build the index first running `python index.py`.")

  with measure("Search finished", args.verbose):
    for path in search(index, args.START, args.GOAL, args.limit):
      print(" -> ".join(path))
