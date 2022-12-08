var triesCount = 0;
var leftovers = []

document.addEventListener('DOMContentLoaded', function(){ 
  
  if((e = document.querySelector("#requestid")) !== null){
    
    getLeftoversExecuted();

  }
     

});

function getLeftoversExecuted() {

  if(triesCount < 20){

    triesCount = triesCount + 1;

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

        var ep = document.querySelector("#products_menu");
        
        ep.querySelector("#loading").classList.add('hidden');
        ep.querySelector("#reload").classList.remove('hidden');

        leftovers = jr.leftovers;



        showLeftovers();

        // if(!jr.leftovers){
        //   ep.querySelector("#zeroleftovers").style.display = 'block';
        // }

      } else {

        console.log(jr.message);

      }

    }

  };

  req.send();
}

function showLeftovers() {

  if(leftovers){

    document.querySelectorAll('#gooditem').forEach(gelement => {

      gelement.querySelector('#goodsLeftover').value = 0;

      leftovers.forEach(element => {

        if (element.productid == gelement.querySelector('#goodsFilter').getAttribute('id1c')){
            if(element.characteristicid == gelement.querySelector('#сharacteristicsFilter').getAttribute('id1c')) {

            gelement.querySelector('#goodsLeftover').value = element.quantity;

          }
        }
      });

      
    });

  }  
}

function requestPost(url, data, resultCallBack) {
    
  var req = new XMLHttpRequest();

  req.open("POST", url, true);

  req.onreadystatechange = function () {

      if (this.readyState != 4)
          return;

      // button.innerHTML = 'Готово!';
      if (this.status != 200) {
          //setTimeout(onError, 1000);
          // alert(this.status + ': ' + this.statusText);
      } else {
          
          resultCallBack(req.responseText);
          //onLoad();
      }

  };

  req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  req.send(JSON.stringify(data));

  //return req.responseText;
}



function reloadLeftovers(){

  requestPost('?sgl=1', [], function (response_text) {
    
    res = JSON.parse(response_text);

    if(res.result){

      document.querySelector("#requestid").value = res.requestid;

      var ep = document.querySelector("#products_menu");
        
      ep.querySelector("#loading").classList.remove('hidden');
      ep.querySelector("#reload").classList.add('hidden');

      triesCount = 0;

      getLeftoversExecuted();
      

    }


  });

}