import random
import unittest
from topn import topn
from generator import generator

random.seed(1)


class TestTopN(unittest.TestCase):

  def test_wrongtopn(self):
    with self.assertRaises(TypeError):
      topn(3, [5, 'foo', 'bar', 7])

  def test_top1(self):
    self._test_top(1, range(5))

  def test_topn(self):
    self._test_top(3, range(-9, 10))
    self._test_top(5, [2] * 10 + [6] * 2)

  def test_topn_large(self):
    numbers=random.sample(range(-10 ** 6, 10 ** 6), 10 ** 6)
    self._test_top(10, numbers)

  def _test_top(self, n, iterator):
    numbers=list(iterator)
    numbers.sort()
    solution=numbers[-n:]
    random.shuffle(numbers)
    self.assertEqual(topn(n, numbers), solution)

  def test_generator(self):
    numbers=list(generator(1024, 0, 42))
    self.assertEqual(len(numbers), 369, 'Different length for the same seed')

if __name__ == '__main__':
  unittest.main()
