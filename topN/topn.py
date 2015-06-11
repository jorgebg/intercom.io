"""
Output N largest numbers from the input, highest first.
"""

from argparse import ArgumentParser
from bisect import insort_left as insort
from sys import stdin, stdout, stderr


def topn(N, iterator):
  if N is 1:
    return [max(iterator)]

  items = []
  for i, n in enumerate(iterator):
    if i < N:
      insort(items, n)
    elif n > items[0]:
      del items[0]
      insort(items, n)

  return items


if __name__ == '__main__':

  parser = ArgumentParser(__file__, description=__doc__)
  parser.add_argument('N', type=int, help="Amount of numbers to extract from the list.")
  args = parser.parse_args()

  iterator = map(int, stdin)
  try:
    result = topn(args.N, iterator)
  except (ValueError, TypeError):
    parser.error('Invalid number')

  for number in reversed(result):
    print(number)
