
def plus1(x):
    return x+1


entrees_visibles = [
        (1,plus1(1)),
        (2,3)
]
entrees_invisibles = [
        (1,2),
        (2,3)
]


def f(x,y):
  return y

@solution
def g(x,y):
  return f(x,y)
