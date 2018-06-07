==============
TP exemple
==============

Mastermind 
___________
.. include:: exercices/exemple_mastermind.rst



Python
_______

Pour la suite, vous aurez besoin de savoir définir une fonction python. Par exemple, la fonction suivante permet de faire la somme de deux entiers passés en argument : ::

  def ajoute(x,y):
    return x+y

On peut appeler la fonction de cette manière : ::

  >> x=ajoute(3,4)
  >> print(x)
  >> 7

L'exercice suivant vous propose d'essayer !

.. include::  exercices/produit.rst


Les conditionnelles en python se font par exemple de la manière suivante : ::

  def compte(x):
    if x==0:
      return "Zero"
    if x==1:
      return "Un"
    if x>1:
    	return "Je ne sais pas compter au delà de un"
    else:
        return "Je ne sais pas compter en dessous de zéro"


.. include:: exercices/max.rst
.. include:: exercices/min.rst


En python on peut parcourir les listes avec une boucle for, par exemple ::
  
  def contient2(liste):
    for elem in liste:
      if elem == 2:
        return True
    return False

On peut appeler la fonction de cette manière : ::

  >> x=contient2([1,2,3,4,5])
  >> print(x)
  >> True



.. include:: exercices/somme.rst


Et pour finir, un défi :
________________________

.. include:: exercices/twisted_fate.rst


Exemple en JAVA :
__________________
.. include:: exercices/essai_java.rst

Exemple Generique :
___________________
.. include:: exercices/exo_generique.rst

Exemple IJVM :
___________________
.. include:: exercices/exo_ijvm.rst
Exemple MySQL :
___________________
.. include:: exercices/exo_mysql.rst
