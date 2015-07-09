from functools import reduce

# Input: an array of numbers with one and only one number that appears an odd number of times.
# Output: the number that appears an odd number of times
array = [2, 3, 2, 3, 5, 7, 3, 7, 3]

def solver1():
  '''
  map approach
  complexity:
    computational: O(N)
    space: map
  '''
  output = dict()
  for x in array:
    if x in output:
      output[x] += 1
    else:
      output[x] = 1
  for k,v in output.items():
    if v % 2 is 1:
      return k

def solver2():
  '''
  set approach
  complexity:
    computational: O(N)
    space: set
  '''
  output = set()
  for x in array:
    if x in output:
      output.remove(x)
    else:
      output.add(x)
  return output.pop()

def solver3():
  '''
  XOR approach
  complexity:
    computational: O(N)
    space: no extra data structure needed
  '''
  output = reduce(lambda a, b: a ^ b, array)
  return output

###

solution = 5
for solver in (solver1, solver2, solver3):
  result = solver()
  print(solver.__name__, result)
  assert result == solution
