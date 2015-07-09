# Input: an array of numbers and a math function
# Output: the indexes of the pairs of numbers that matches the function provided

array = [-2, 0, 8, 4, 4, 7, 9, 14]
match = lambda a, b: a+b==12

def solver1():
  '''
  complexity:
    computational: O(N) + O(N) = O(N^2)
  '''
  n = len(array)
  output = set()
  for i in range(0, n): # O(N)
    for j in range(i+1, n): # O(N)
      if array[i] + array[j] == 12:
        output.add((i,j))
  return output


solution = {(2, 3), (2, 4), (0, 7)}

for solver in (solver1,):
  result = solver()
  print(solver.__name__, result)
  assert result == solution
