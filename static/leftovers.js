document.addEventListener('DOMContentLoaded', function(){ 
  
  if((e = document.querySelector("#requestid")) !== null){
    
    getLeftoversExecuted();

  }
     

});

function getLeftoversExecuted() {

  var req = new XMLHttpRequest();

  var url = "../reqexec/";
  req.open("GET", url, true);
  req.setRequestHeader('requestid', e.value);

  req.onreadystatechange = function () {

    if (this.readyState != 4)
      return;

    if (this.status != 200) {

      setTimeout(getLeftoversExecuted, 5000);

    } else {

      if (JSON.parse(this.response).executed) {

        getLeftovers();

      } else {

        setTimeout(getLeftoversExecuted, 1000);

      }

    }

  };

  req.send();
}


function getLeftovers() {

  var req = new XMLHttpRequest();

  var url = "../getleftovers/";
  req.open("GET", url, true);
  req.onreadystatechange = function () {

    if (this.readyState != 4)
      return;

    if (this.status != 200) {

      console.log(this.responseText);

    } else {

      jr = JSON.parse(this.response);

      if (jr.result) {

        var ep = document.querySelector("#products");
        
        document.querySelector("#loading").style.display = 'none';

        jr.leftovers.forEach(welement => {

          ep.innerHTML = ep.innerHTML
            + '<h3 class="text-center" style="font-size: 2rem;">Остатки по складу ' + welement.warehouse + '</h3>'
            + '<div class="row">'
            + '<div class="col-10 themed-grid-col" style="text-align: center">Номенклатура</div>'
            + '<div class="col-2 themed-grid-col" style="text-align: center">Количество</div>'
            + '</div>';

        welement.leftovers.forEach(element => {

            productstr = element.product;
            if(element.characteristic){
              productstr = productstr + ' (' + element.characteristic + ')';
            }

            ep.innerHTML = ep.innerHTML + '<div class="row">'
              + '<div class="col-10 themed-grid-col">' + productstr + '</div>'
              + '<div class="col-2 themed-grid-col">' + element.quantity + '</div>'
            + '</div>';
          });

        });

        if(!jr.leftovers){
          ep.querySelector("#zeroleftovers").style.display = 'block';
        }

      } else {

        console.log(jr.message);

      }

    }

  };

  req.send();
}

