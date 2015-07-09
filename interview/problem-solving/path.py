from itertools import product

# Input: a matrix with empty squares and obstacle squares
# Output: the path from a starting point to the end point

matrix = [[0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 0],
          [0, 1, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 1],
          [0, 0, 0, 1, 1, 1]]


# matrix = [[0, 0, 0, 0, 0, 0],
#           [0, 0, 1, 0, 0, 0],
#           [0, 1, 1, 1, 0, 0],
#           [0, 0, 0, 1, 0, 0],
#           [0, 0, 0, 0, 1, 1],
#           [0, 0, 0, 1, 1, 1]]

X = Y = 6

start = (4, 1)
end = (2, 4)

###

obstacles = {(x, y) for x in range(X) for y in range(Y) if matrix[x][y]}

def square(x, y):
  return 0 <= x < X and 0 <= y < Y and (x,y) not in obstacles


def neighbours(x, y):
  d = (-1, 0, +1)
  result = []
  for dx, dy in product(d, d):
    _x, _y = (x + dx, y + dy)
    if square(_x, _y):
      result.append((_x, _y))
  return result

###


def solver1():
  '''
  Breadth First Search
  '''
  path = (start,)
  queue = [path]
  discovered = {start}
  while queue:
    path = queue.pop()
    for n in neighbours(*path[-1]):
      if n == end:
        return path + (n,)
      if n not in discovered:
        queue.insert(0, path + (n,))
        discovered.add(n)


def solver2():
  '''
  Dijkstra
  '''
  raise NotImplementedError()


def solver3():
  '''
  A*
  '''
  raise NotImplementedError()


###

solution = ((4, 1), (3, 2), (2, 3), (2, 4))
for solver in (solver1, solver2, solver3):
  result = solver()
  print(solver.__name__, result)
  assert result == solution
