entrees_visibles = [
        couple([1,2]),
        couple([2,3])
]
entrees_invisibles = [
        couple([1,2]),
        couple([2,3])
]

def couple(l):
    return l[0],l[1]

@solution
def g(c):
  return c[1]
