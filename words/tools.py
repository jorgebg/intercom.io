import time
import sys
import os
from contextlib import contextmanager

def findwords():
  for path in ["/usr/share/dict/words", "/usr/dict/words"]:
    if os.path.isfile(path):
      default_dict = path
      break
  else:
    default_dict = "words"

  return default_dict

@contextmanager
def measure(msg, verbose=False, stream=sys.stderr):
  start = time.time()
  yield
  end = time.time()
  if verbose:
    stream.write(msg + " in %g s\n" % (end - start))
