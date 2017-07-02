# coding: utf8
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
#    def getExerciceJava(self,pathFichierModuleEns):
#        with open(pathFichierModuleEns) as fichier:
#            contenu=''.join(fichier.readlines())
#            headers = {'content-type': 'application/json'}
#            payload={'moduleEns':contenu, 'enonce':"toto",'commentaires':"",'type':"java"}
#            res=requests.post("http://localhost:8000/api/v1/gestion_exercice_java/", data=json.dumps(payload), headers=headers)
#            return res.json()

#    def getExercicePython(self,pathFichierModuleEns):
#        with open(pathFichierModuleEns) as fichier:
#            contenu=''.join(fichier.readlines())
#            headers = {'content-type': 'application/json'}
#            payload={'moduleEns':contenu, 'enonce':"toto",'type':self.options["language"]}
#            res=requests.post("http://localhost:8000/api/v1/gestion_exercice/", data=json.dumps(payload), headers=headers)
#            dico = res.json()
#            if 'traceback' in dico:
#                print(dico["traceback"])
#            return dico
#    def getExercice(self, language, pathFichierModuleEns):
#         if language=="python":
#              return self.getExercicePython(pathFichierModuleEns)
#         if language=="java":
#             res=self.getExerciceJava(pathFichierModuleEns)
#             return res
#         else:
#             return "Unknown programming language"
    def getExercice(self,pathFichierModuleEns):
        with open(pathFichierModuleEns) as fichier:
            contenu=''.join(fichier.readlines())
            headers = {'content-type': 'application/json'}
            payload={'moduleEns':contenu, 'enonce':"toto",'type':self.options["language"]}
            res=requests.post("http://localhost:8000/api/v1/gestion_exercice/", data=json.dumps(payload), headers=headers)
            dico = res.json()
            if 'traceback' in dico:
                print(dico["traceback"])
            return dico

        """
        {'titre': 'mafonctino',
        'enonce': 'toto',
        'hashCode': '23f83f469056e5351613c4f6dc71c72b',
        'metaInfos':
           {
              'entrees_visibles': [[1, 2], [2, 3]],
              'arguments': ['x', 'y'],
              'solutions_visibles': [['1, 2', '1'], ['2, 3', '2']],
              'nom_solution': 'mafonctino',
              'messages': ['Solutions et entrees, tout y est !'],
              'temps': 0.005748748779296875,
              'solutions_invisibles': [[[1, 2], 1], [[2, 3], 2]],
              'entrees_invisibles': [[1, 2], [2, 3]]},
              'resource_uri': '/api/v1/gestion_exercice/23f83f469056e5351613c4f6dc71c72b/',
              'commentaires': '',
              'moduleEns': 'entrees_visibles = [\n        (1,2),\n        (2,3)\n]\nentrees_invisibles = [\n        (1,2),\n        (2,3)\n]\n\n@solution\ndef mafonctino(x,y):\n  return  x\n', 'auteur': '', 'date': '2016-10-21T09:28:42.557085', 'metaInfos': '{"solutions_invisibles": [[[1, 2], 1], [[2, 3], 2]], "messages": ["Solutions et entr\\u00e9es, tout y est !"], "arguments": ["x", "y"], "temps": 0.005748748779296875, "entrees_invisibles": [[1, 2], [2, 3]], "entrees_visibles": [[1, 2], [2, 3]], "nom_solution": "mafonctino", "solutions_visibles": [["1, 2", "1"], ["2, 3", "2"]]}'}
        """

    has_content = True
    required_arguments = 1
    optional_arguments = 0

    option_spec = {
        "language": directives.unchanged,
        "uuid": directives.unchanged, # TODO si defini le prendre comme hash
    }

    def run(self):
        print("OPTIONS:" + str(self.options))
        env = self.state.document.settings.env
        (relative_filename, absolute_filename)=env.relfn2path(self.arguments[0])

        #donnees= self.getExercice(self.options["language"], absolute_filename) if env.app.config.easypython_production else {
        donnees= self.getExercice(absolute_filename) if env.app.config.easypython_production else {
        'hashCode': '1234',
        'metaInfos':
           {
              'arguments': ['argument_bidon', 'argument_bidon'],
              'solutions_visibles': [["exemple bidon", "sortie bidon"], ["exemple bidon", "sortie bidon"]],
              'nom_solution': 'fonction_bidon',
            }
        }
        if(self.options["language"]=="python"):
            zoneExercice=EasyPythonNode()
            exemples=Exemples()
            exemples["exemples"]=donnees["metaInfos"]["solutions_visibles"]
            zoneExercice["prototype_solution"]="def " + donnees["metaInfos"]["nom_solution"] + "("+','.join(donnees["metaInfos"]["arguments"])+"):\n    return None"
            zoneExercice["hash"]= donnees["hashCode"]
            zoneExercice["language"]=self.options["language"]
            return [exemples, zoneExercice]
        if(self.options["language"]=="java"):
            zoneExercice=EasyPythonNode()
            zoneExercice["prototype_solution"]="Votre classe.."
            zoneExercice["hash"]= donnees["hashCode"]
            zoneExercice["language"]=self.options["language"]
            return [zoneExercice]

def visit_exemples_node(self, node):
        self.body.append("<ul class='list-group'>")
        for (entree,sortie) in node["exemples"]:
            self.body.append("<li class='list-group-item'> Sur l'entr&eacute;e <code>" + str(entree) + "</code> votre solution doit renvoyer <code>" + str(sortie) + "</code>.</li>")
        self.body.append("</ul>")

def visit_easypython_node(self, node):
        self.body.append("<div hash='"+node["hash"]+"' language='"+node["language"]+"' class='easypython clearfix'>")
        self.body.append(node["prototype_solution"])
        self.body.append("</div>")

def depart_easypython_node(self, node):
    pass

def latex_departure(self, node):
    pass
def visit_latex(self,node):
    pass

def setup(app):
    app.add_config_value('easypython_production', False, 'html')
    app.add_node(EasyPythonNode, html=(visit_easypython_node, depart_easypython_node), latex=(visit_latex, latex_departure))
    app.add_node(Exemples, html=(visit_exemples_node, depart_easypython_node),latex=(visit_latex, latex_departure))

    app.add_directive('easypython', EasyPythonDirective)

    return {'version': '0.1'}   # identifies the version of our extension
