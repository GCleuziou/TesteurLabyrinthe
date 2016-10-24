entrees_visibles=[
        (23),
        (25),
        (26),
]
entrees_invisibles=[
        (2668),
        (2666),
        (2667),
]

@solution
def nombreDEtagesDuPlusHautChateau(nombreDeCartes):
  n=-1 #numero de l'étage
  e=-1 #nombre de cartes à cet étage
  s=0 # somme de toutes les cartes
  while(s<=nombreDeCartes):
    n=n+1
    e=e+3
    s=s+e
  return n

