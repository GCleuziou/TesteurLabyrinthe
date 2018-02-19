var codeNode={}
var codemirrors={}

function marquerReussi(hash)
{
    let currentCM   = codemirrors[hash];
    let currentNode = codeNode[hash];
    currentCM.setOption('readOnly',true);
    currentNode.children("button").remove();
    let reussi=$("<div class='alert alert-success' role='alert'>Félicitations !!</div>");
    if(currentNode.children(".panel").length>0)
         currentNode.children(".panel").replaceWith(reussi);
    else
         currentNode.append(reussi);
}

function marquerARetenter(hash, reponse, language)
{
    let currentCM   = codemirrors[hash];
    let currentNode = codeNode[hash];
    let bouton = currentNode.children("button")[0]
    bouton.innerHTML="Envoyer";

    let titre="vide";
    let contenu="vide";
    let erreur='';
    for (_erreur in reponse["tentative"])
          erreur=_erreur;
    titre=erreur;
    contenu = $(`<ul class='list-group collapse' id='contenu-${hash}'/>`)
    for( x of reponse["tentative"][erreur])
        contenu.append($(`
                    <li class="list-group-item">
                    <code>${x}</code>
                    </li>
         `));
    let rate=$("<div class='panel panel-default'></div>");
    rate.append( $(`
                  <div class='panel-heading clearfix'>${titre}
                      <button class="btn btn-default pull-right" type="button" data-toggle="collapse"
                      data-target="#contenu-${hash}"
                      aria-expanded="false" aria-controls="contenu-${hash}" >
                        <span class="glyphicon glyphicon-eye-open "></span>
                      </button>
                    </div>`));
    rate.append(contenu)
    if(currentNode.children(".panel").length>0)
        currentNode.children(".panel").replaceWith(rate);
    else
        currentNode.append(rate);

}

function soumettreSolution(hash,language)
{

    let currentCM   = codemirrors[hash];
    let currentNode = codeNode[hash];
    let bouton = currentNode.children("button")[0]
    bouton.disabled=true;
    tutu = bouton.innerHTML='Patientez..';
//    fetch('https://www.univ-orleans.fr/iut-orleans/informatique/intra/ap/api/v1/tentative'+language+'/',
    fetch('https://www.univ-orleans.fr/iut-orleans/informatique/intra/ap/api/v1/tentative/',
    {
      mode        : 'cors',
      method      : 'POST',
      credentials : 'include',
      body        : JSON.stringify(
        {
          'contenu':currentCM.getValue(),
          'hash'   : hash
        }),
      headers     : {
          'content-type':'application/json'
        }
     })
     .then(reponse => {
        bouton.disabled=false;
        if (reponse.ok)
        {
          marquerReussi(hash);
        }
        else
        {
          reponse.json().then(reponse => marquerARetenter(hash,reponse,language))
        }
      })
    }


function remplirNoeudCode(noeud)
{
    let prototype=$(this).html();
    $(this).text("");
    let mode = {"python":"python","java":"text/x-java"}[$(this).attr('language')];
    c=CodeMirror(this, {
          value: prototype,
          mode:mode,
          lineNumbers: true,
          styleActiveLine: true,
          matchBrackets: true
        });

     var $bouton=$("<button/>", {
          text:'Envoyer',
          click: function(hash, language){return function(){soumettre(hash,language)}}($(this).attr('hash'), $(this).attr('language')),
          class:'btn btn-primary',
          type:'button'
     })
     codeNode[$(this).attr('hash')]=$(this);
     codemirrors[$(this).attr('hash')]=c;
     $(this).append($bouton);
}

function reponseToJson(reponse)
{
    return reponse.json();
}

function setInfosExercices()
{
  let exercices ="";
  for(let elem in codeNode)
   {
        exercices+=elem+";";
   }

   fetch("https://www.univ-orleans.fr/iut-orleans/informatique/intra/ap/api/v1/exerciceReussi/set/"+exercices+"/?format=json",
    {
      mode        :'cors',
      method      : 'GET',
      credentials : 'include',
      headers     : {
          'content-type':'application/json'
        }
     })
    .then( reponseToJson)
    .then( reponse=> {
          for(let elem of reponse.objects)
            codeNode[elem["hashCode"]].append($("<div class='alert alert-success' role='alert'>Déja Réussi !!</div>")); // <= MARQUER EXO REUSSI OU PAS !

     });
}

document.addEventListener("DOMContentLoaded", function(){
  window.soumettre = soumettreSolution;
  let zonesCode = $(".easypython");
  zonesCode.each(remplirNoeudCode);
  setInfosExercices();
  });
