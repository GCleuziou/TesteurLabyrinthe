from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.compat import make_admonition
from sphinx.locale import _
from docutils.parsers.rst import directives
import os
import requests
import json

os.environ['NO_PROXY'] = 'localhost'


class EasyPythonNode(nodes.Element):
    pass

class Exemples(nodes.Admonition, nodes.Element):
    pass


class EasyPythonDirective(Directive):


    def getExercice(self,pathFichierModuleEns):
        with open(pathFichierModuleEns) as fichier:
            contenu=''.join(fichier.readlines())   
            headers = {'content-type': 'application/json'}
            payload={'moduleEns':contenu, 'enonce':"toto",'commentaires':""}
            res=requests.post("http://localhost:8000/api/v1/gestion_exercice/", data=json.dumps(payload), headers=headers)
            print(res.text)
            return res.json()
        """
        {'titre': 'mafonctino',
        'enonce': 'toto',
        'hashCode': '23f83f469056e5351613c4f6dc71c72b',
        'resultats_ens': 
           {
              'entrees_visibles': [[1, 2], [2, 3]],
              'arguments': ['x', 'y'],
              'solutions_visibles': [['1, 2', '1'], ['2, 3', '2']],
              'nom_solution': 'mafonctino',
              'messages': ['Solutions et entrées, tout y est !'], 
              'temps': 0.005748748779296875, 
              'solutions_invisibles': [[[1, 2], 1], [[2, 3], 2]], 
              'entrees_invisibles': [[1, 2], [2, 3]]}, 
              'resource_uri': '/api/v1/gestion_exercice/23f83f469056e5351613c4f6dc71c72b/',
              'commentaires': '',
              'moduleEns': 'entrees_visibles = [\n        (1,2),\n        (2,3)\n]\nentrees_invisibles = [\n        (1,2),\n        (2,3)\n]\n\n@solution\ndef mafonctino(x,y):\n  return  x\n', 'auteur': '', 'date': '2016-10-21T09:28:42.557085', 'resultatsEns': '{"solutions_invisibles": [[[1, 2], 1], [[2, 3], 2]], "messages": ["Solutions et entr\\u00e9es, tout y est !"], "arguments": ["x", "y"], "temps": 0.005748748779296875, "entrees_invisibles": [[1, 2], [2, 3]], "entrees_visibles": [[1, 2], [2, 3]], "nom_solution": "mafonctino", "solutions_visibles": [["1, 2", "1"], ["2, 3", "2"]]}'}
        """

    has_content = True
    required_arguments = 1
    optional_arguments = 2

    option_spec = {
        "language": directives.unchanged,
        "uuid": directives.unchanged, # TODO si défini le prendre comme hash
    }
    def run(self):
        env = self.state.document.settings.env
        zoneExercice=EasyPythonNode()
        exemples=Exemples()
        exemples["exemples"]=[("123","34"), ("45","52")]

        zoneExercice["numero_exercice"]=7
        (relative_filename, absolute_filename)=env.relfn2path(self.arguments[0])
        donnees=self.getExercice(os.path.join(env.srcdir,relative_filename))
        zoneExercice["prototype_solution"]=donnees["resultats_ens"]["nom_solution"]

        return [exemples, zoneExercice]

def visit_exemples_node(self, node):
        self.body.append("<div>")
        for (entree,sortie) in node["exemples"]:
            self.body.append("<p> Sur l'entrée " + str(entree) + " votre solution doit renvoyer " + str(sortie) + " </p>")

def visit_easypython_node(self, node):

        self.body.append("<div class='easypython'>")
        self.body.append(node["prototype_solution"])
        self.body.append("</div>")

def depart_easypython_node(self, node):
    pass


def setup(app):
    app.add_node(EasyPythonNode, html=(visit_easypython_node, depart_easypython_node))
    app.add_node(Exemples, html=(visit_exemples_node, depart_easypython_node))

    app.add_directive('easypython', EasyPythonDirective)

    return {'version': '0.1'}   # identifies the version of our extension

