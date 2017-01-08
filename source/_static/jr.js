document.addEventListener("DOMContentLoaded",
function(){

  window.soumettre = function(hash, language){
    currentCM=codemirrors[hash]
    currentNode=codeNode[hash]
    currentNode.children("button")[0].disabled=true;
    t=currentNode.children("button")[0].innerHTML='Patientez..';
//    fetch('https://www.univ-orleans.fr/iut-orleans/informatique/intra/ap3/api/v1/tentative'+language+'/',
    fetch('http://localhost:8000/api/v1/tentative_'+language+'/',
    {
      mode:'cors',
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify(
        {
          'contenu':currentCM.getValue(),
          'hash': hash
        }),
        headers:{
          'content-type':'application/json'
        }
      })
      .then(reponse => {

        currentNode.children("button").disabled=false;

        if (reponse.ok) {
          currentCM.setOption('readOnly',true)
          reussi=$("<div class='alert alert-success' role='alert'>Félicitations !!</div>")
          currentNode.children("button").remove()
          if(currentNode.children(".panel").length>0)
             currentNode.children(".panel").replaceWith(reussi)
          else
            currentNode.append(reussi)
        } else {
          currentNode.children("button")[0].innerHTML="Envoyer";
          currentNode.children("button")[0].disabled=false;
          reponse.json().then(
            reponse=>{
              let titre="vide"
              let contenu="vide"
              let erreur=''
              for (_erreur in reponse["tentative_"+language])
                 erreur=_erreur

              titre=erreur
              contenu=$(`<ul class='list-group collapse' id='contenu-${hash}'/>`)
                for( x of reponse["tentative_"+language][erreur]) // ATTENTION : pas bon tenative => tentative_python ou tenative_java
                  contenu.append($(`
                    <li class="list-group-item">
                    <code>${x}</code>
                    </li>
                  `))

              rate=$("<div class='panel panel-default'></div>")
              rate.append( $(`
                  <div class='panel-heading clearfix'>${titre}
                      <button class="btn btn-default pull-right" type="button" data-toggle="collapse"
                      data-target="#contenu-${hash}"
                      aria-expanded="false" aria-controls="contenu-${hash}" >
                        <span class="glyphicon glyphicon-eye-open "></span>
                      </button>
                    </div>`))
          rate.append(contenu)
      //    rate=$("<div class='alert alert-warning alert-dismissible pull-left'
      //     role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>RATE</div>")
          if(currentNode.children(".panel").length>0)
             currentNode.children(".panel").replaceWith(rate)
          else
            currentNode.append(rate)        }
        )
        }
      })

      zoneExo=currentCM.parentNode
    }


    zonesCode = $(".easypython");
    codemirrors={}
    codeNode={}
    zonesCode.each(
      function(zone){
        let prototype=$(this).html()
        $(this).text("")
        c=CodeMirror(this, {
          value: prototype,
          mode:"python",
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
        codeNode[$(this).attr('hash')]=$(this)
        codemirrors[$(this).attr('hash')]=c
        $(this).append($bouton)
      }
    )
  })
