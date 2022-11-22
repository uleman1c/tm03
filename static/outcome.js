document.addEventListener('DOMContentLoaded', function(){ 
  
  if((e = document.querySelector("#requestid")) !== null){
    
    getOutcomeExecuted();

  }
     

});

function getOutcomeExecuted() {

  var req = new XMLHttpRequest();

  var url = "../reqexec/";
  req.open("GET", url, true);
  req.setRequestHeader('requestid', e.value);

  req.onreadystatechange = function () {

    if (this.readyState != 4)
      return;

    if (this.status != 200) {

      setTimeout(getOutcomeExecuted, 5000);

    } else {

      if (JSON.parse(this.response).executed) {

        getOutcome();

      } else {

        setTimeout(getOutcomeExecuted, 1000);

      }

    }

  };

  req.send();
}


function getOutcome() {

  var req = new XMLHttpRequest();

  var url = "../getOutcome/";
  req.open("GET", url, true);
  req.onreadystatechange = function () {

    if (this.readyState != 4)
      return;

    if (this.status != 200) {

      console.log(this.responseText);

    } else {

      jr = JSON.parse(this.response);

      if (jr.result) {

        var ep = document.querySelector("#orders");
        
        ep.querySelector("#loading").style.display = 'none';

        jr.outcome.forEach(element => {

          ep.innerHTML = ep.innerHTML + '<div class="row">'
            + '<a href="/prnform?id=' + element.Распоряжение + '" class="col-1 themed-grid-col">'
            + '<img src="/static/print.png" style="width: 100%"></img>'
            + '</a>'
            + '<div class="col-9 themed-grid-col" data-id1c="' + element.Распоряжение + '">' + element.ПолучательСтр + ", " + element.РаспоряжениеСтр + ', ' + element.Комментарий + '</div>'
            + '<div class="col-2 themed-grid-col" style="text-align: center;">' + element.ДатаОтгрузки + '</div>'
          + '</div>';

        });

        if(!jr.outcome){
          ep.querySelector("#noneorders").style.display = 'block';
        }

      } else {

        console.log(jr.message);

      }

    }

  };

  req.send();
}

