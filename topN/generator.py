"""
Output individual random numbers on each line until the specified size is reached.
"""
import random
import sys
from argparse import ArgumentParser


def generator(size, a, b):
  i = 0
  while i < size:
    number = random.randint(a, b)
    line = "%i\n" % number
    i += len(line)
    yield line


if __name__ == '__main__':
  parser = ArgumentParser(__file__, description=__doc__)
  parser.add_argument(
      '--size', '-s', type=int, default=100, help='Given in MB (defaults to 100MB)')
  parser.add_argument('--min', '-m', type=int, default=0,
                      help="Minimum value of the generated numbers (defaults to 0)")
  parser.add_argument('--max', '-M', type=int, default=10 ** 12,
                      help="Maximum value of the generated numbers (defaults to 1 billion)")
  parser.add_argument('--seed', '-S', type=int)
  parser.add_argument('--verbose', '-v', action='store_true')
  args = parser.parse_args()

  if args.min > args.max:
    parser.error("The minimum value must be lower than the maximum value.")

  if args.seed:
    random.seed(args.seed)

  bsize = args.size << 20  # MB
  lines = generator(bsize, args.min, args.max)
  for line in lines:
    sys.stdout.write(line)
    if args.verbose:
      sys.stderr.write(line)
