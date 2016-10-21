document.addEventListener("DOMContentLoaded", function() {
   window.soumettre = function(hash){
		currentCM=codemirrors[hash]
		 fetch('http://localhost:8000/api/v1/tentative/',
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
        if (reponse.ok) {
    			currentCM.setOption('readOnly',true)
          alert("REUSSI")
        } else {
          alert("Rate")
        }
      })

		zoneExo=currentCM.parentNode
   }


	  zonesCode = document.getElementsByClassName("easypython");
    codemirrors={}
    for(elem of zonesCode){
			codemirrors[elem.parentNode.id] = CodeMirror( function(elt) {
					elem.parentNode.replaceChild(elt, elem);
		  },
			{
      value: elem.innerHTML,
      mode:"python"
   	});
	
	}

})
