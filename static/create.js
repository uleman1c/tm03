function checkoutRecipeOrder(){

    var contractor_id1c = document.querySelector('#contractor').getAttribute('id1c'); 
    var endproduct_id1c = document.querySelector('#endProductFilter').getAttribute('id1c');
    var endproducttext = document.querySelector('#endProductText').value;
    var endproductquantity = document.querySelector('#endProductQuantity').value;

    if (contractor_id1c 
        && endproductquantity 
        && (endproduct_id1c || endproducttext)){

        var url = "/add_recipeorder/";
        var data = {};
        data.contractor = contractor_id1c;
        data.comment = document.querySelector('#comment').value;
        data.endproduct = endproduct_id1c;
        data.endproducttext = endproducttext;
        data.colorNumber = document.querySelector('#colorNumber').value;
        data.endproductquantity = endproductquantity;

        $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "../recipeorders/";
             },
             error: function(){
                 console.log("error")
             }
         })

    } else {

        arWarning = []
        if(!contractor_id1c) {
            arWarning.push('заполнить контрагента');
        }

        if(!endproduct_id1c && !endproducttext) {
            arWarning.push('выбрать продукцию из справочника или заполнить вручную');
        }

        if(!endproductquantity) {
            arWarning.push('заполнить количество');
        }

        strWarning = "";
        arWarning.forEach(function(warnItem){

            strWarning = strWarning + (!strWarning ? "" : ", ") + warnItem;
            
        });

        wt = document.querySelector('#warning_text');
        wt.style = 'border-radius: 0.3rem; font-size: calc(1rem + 0.5vh); background-color: red; margin-top: 2%; color: white; text-align: center; display: block';
        wt.innerHTML = 'Необходимо ' + strWarning;

    }

}


function checkoutRecipe(){

    var aGoods = document.querySelectorAll('#goods #gooditem');

    arG = [];

    aGoods.forEach(function(goodItem){

        gq = goodItem.querySelector('#goodsQuantity');
        gf = goodItem.querySelector('#goodsFilter');
        cf = goodItem.querySelector('#сharacteristicsFilter');

        if(gf.getAttribute('id1c') && gq.value){

            arG.push({'name': gf.value, 'id1c': gf.getAttribute('id1c'), 'cid1c': cf.getAttribute('id1c'), 'quantity': gq.value}); 
        }
    });

    if (document.querySelector('#contractor').value 
        && document.querySelector('#endProductQuantity').value 
        && arG.length > 0){

        var url = "/add_recipe/";
        var data = {};
        data.contractor = document.querySelector('#contractor').getAttribute('id1c');
        data.comment = document.querySelector('#comment').value;
        data.endproduct = document.querySelector('#endProductFilter').getAttribute('id1c');
        data.endproducttext = document.querySelector('#endProductText').value;
        data.colorNumber = document.querySelector('#colorNumber').value;
        data.endproductquantity = document.querySelector('#endProductQuantity').value;

        el_orderid = document.querySelector('#orderid');
        data.orderid = el_orderid ? el_orderid.value : '';

        data.length = arG.length;
        data.goods = arG;

        $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "../recipes/";
             },
             error: function(jqXHR, exception){
                 console.log("error")
             }
         })



    }

}


function selectGood(numstr, id1c, name){

    var gl = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #goodsList');

    gl.innerHTML = "";

    var gf = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #goodsFilter');

    gf.value = name;
    gf.setAttribute('id1c', id1c);

    var gf = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #сharacteristicsFilter');

    gf.value = '';
    gf.setAttribute('id1c', '00000000-0000-0000-0000-000000000000');


    showLeftovers();

}

function selectEndProduct(id1c, name){

    var gl = document.querySelector('#endProduct #goodsList');

    gl.innerHTML = "";

    var gf = document.querySelector('#endProduct #endProductFilter');

    gf.value = name;
    gf.setAttribute('id1c', id1c);



}


function keyUpEndProductFilter() {
    var t = document.querySelector('#endProduct #endProductFilter').value;
    var url = "/goodsfilter/";
    var data = {};
    data.search_filter = t;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {

            var gl = document.querySelector('#endProduct #goodsList');

            gl.innerHTML = "";

            for (datavalue in data.products) {

                value = data.products[datavalue];

                curFullName = value.fullname.replaceAll('"', '&#34;');

                var li = document.createElement("li");
                li.innerHTML = '<li>'
                        + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                            + '<div style="float: left; width: 100%">'
                                + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" onClick="selectEndProduct(\'' + value.id1c + '\', \'' + curFullName + '\')" style="white-space: normal" >' + curFullName + '</a>'
                            + '</div>'
                        + '</div>'
                    + '</li>';
                gl.appendChild(li);

            }


         },
         error: function(){
             console.log("error")
         }
     })

}

function keyUpGoodsFilterWOB(numstr) {
    var t = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #goodsFilter').value;
    var url = "/goodsfilter/";
    var data = {};
    data.search_filter = t;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {

            var gl = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #goodsList');

            gl.innerHTML = "";

            for (datavalue in data.products) {

                value = data.products[datavalue];

                curFullName = value.fullname.replaceAll('"', '&#34;');

                var li = document.createElement("li");
                li.innerHTML = '<li>'
                        + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                            + '<div style="float: left; width: 100%">'
                                + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" onClick="selectGood(' + numstr + ', \'' + value.id1c + '\', \'' + curFullName + '\')" style="white-space: normal" >' + curFullName + '</a>'
                            + '</div>'
                        + '</div>'
                    + '</li>';
                gl.appendChild(li);

            }


         },
         error: function(){
             console.log("error")
         }
     })

}

function selectCharactreristic(numstr, id1c, name){

    //alert(id1c + ' ' + name);


    var gl = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #сharacteristicsList');

    gl.innerHTML = "";

    var gf = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #сharacteristicsFilter');

    gf.value = name;
    gf.setAttribute('id1c', id1c);

    showLeftovers();

}


function keyUpCharactreristicWOB(numstr) {

    var product_id1c = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #goodsFilter').getAttribute('id1c');

    if (product_id1c) {

        var t = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #сharacteristicsFilter').value;
        var url = "/characteristicsfilter/";
        var data = {};
        data.search_filter = t;
        data.product = product_id1c;

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {

                var gl = document.querySelector('#gooditem[data-numstr="' + numstr + '"] #сharacteristicsList');

                gl.innerHTML = "";
    
                for (datavalue in data.characteristics){

                    value = data.characteristics[datavalue];

                    var li = document.createElement("li");
                    li.innerHTML = '<li>'
                            + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                                + '<div style="float: left; width: 100%">'
                                    + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" onclick="selectCharactreristic(' + numstr + ', \'' + value.id1c + '\', \'' + value.name + '\')" style="white-space: normal" data-id1c="' + value.id1c + '">' + value.name + '</a>'
                                + '</div>'
                            + '</div>'
                        + '</li>';
                    gl.appendChild(li);
                    }
            },
            error: function () {
                console.log("error")
            }
        })
    }
}



var numstr = 1;

function addGoodItem(e) {

    $("#goods").append(
        '<div id="gooditem" data-numstr="' + numstr + '">'
        +'<div style="float: left; width: 50%">'
            +'<input type="search" style="font-size:  normal" id="goodsFilter" class="form-control" onkeyup="keyUpGoodsFilterWOB(' + numstr + ')" autocomplete="false" placeholder="Номенклатура..." id1c="00000000-0000-0000-0000-000000000000">'
        +'<ul id="goodsList" class="list-unstyled mb-0 dropdownscrolllist"></ul>'
        +'</div>'
        +'<div style="float: left; width: 25%">'
            +'<input type="search" id="сharacteristicsFilter" class="form-control" onkeyup="keyUpCharactreristicWOB(' + numstr + ')" autocomplete="false" placeholder="Характеристика..." id1c="00000000-0000-0000-0000-000000000000">'
            +'<ul id="сharacteristicsList" class="list-unstyled mb-0 dropdownscrolllist"></ul>'
        +'</div>'
        +'<input type="number" id="goodsQuantity" class="form-control" style="width: 15%; float: left;" autocomplete="false" placeholder="Количество...">'
        +'<input readonly type="number" id="goodsLeftover" class="form-control" style="width: 5%; float: left;" autocomplete="false" placeholder="0">'
        +'<a href="#" onclick="delGoodItem(' + numstr + ')" id="checkout_order" class="btn btn-danger" style="width: 5%;">-</a>'
    +'</div>');







    numstr = numstr + 1;

}

function delGoodItem(numstr) {

    if(document.querySelector('#goods').childElementCount > 1){

        var gl = document.querySelector('#gooditem[data-numstr="' + numstr + '"]');

        document.querySelector('#goods').removeChild(gl);

    }
}


function getFileWS(filename, idname, ssize){

    var link = document.createElement('a');
     link.download = filename;
 
     var pos = 0;
 
     const part_size = 120000;
 
     var blobs = [];
 
     document.querySelector("#tablecolumnfilesize").innerHTML = "Размер " + Math.floor(pos * 100 / ssize) + "%";
 
     const chatSocket = new WebSocket(
         (window.location.protocol == 'https:' ? 'wss' : 'ws') + '://'
         + window.location.host
         + '/ws/files/' 
     );
 
     chatSocket.onopen = function(e){
 
         chatSocket.send(JSON.stringify({
             'file_name': idname,
             'pos': pos
         }));
     };
 
     chatSocket.onmessage = function(e) {
 
         blobs.push(e.data);
 
         if(e.data.size < part_size){
 
             link.href = URL.createObjectURL(new Blob(blobs, {type: "application/zip"}));
     
             link.click();
             
             URL.revokeObjectURL(link.href);             
 
             chatSocket.close();
 
             document.querySelector("#tablecolumnfilesize").innerHTML = "Размер";
 
         }
         else{
 
             pos = pos + part_size;
 
             document.querySelector("#tablecolumnfilesize").innerHTML = "Размер " + Math.floor(pos * 100 / ssize) + "%";
 
             chatSocket.send(JSON.stringify({
                 'file_name': idname,
                 'pos': pos
             }));
     
 
         }
 
     };
 
     chatSocket.onclose = function(e) {
         //console.error('Chat socket closed unexpectedly');
     };
 
 }
 
 function getFileByParts(filename, idname, ssize){

    var link = document.createElement('a');
     link.download = filename;
 
     var pos = 0;
 
     const part_size = 120000;
 
     var blobs = [];
 
     document.querySelector("#tablecolumnfilesize").innerHTML = "Размер " + Math.floor(pos * 100 / ssize) + "%";
 
     var req = new XMLHttpRequest();

     var url = "../gfbp/";
     req.open("GET", url, true);
     req.responseType = "arraybuffer";
     req.setRequestHeader('id', idname);
     req.setRequestHeader('pos', pos);
 
     req.onreadystatechange = function () { // (3)
 
         if (this.readyState != 4) return;
 
         // button.innerHTML = 'Готово!';
 
         if (this.status != 200) {
 
             setTimeout(onError, 1000);
             // alert(this.status + ': ' + this.statusText);
 
         } else {
 
            blobs.push(req.response);
 
            if(req.response.byteLength < part_size){
    
                link.href = URL.createObjectURL(new Blob(blobs, {type: "application/zip"}));
        
                link.click();
                
                URL.revokeObjectURL(link.href);             
    
                document.querySelector("#tablecolumnfilesize").innerHTML = "Размер";
    
            }
            else{
 
                pos = pos + part_size;
    
                document.querySelector("#tablecolumnfilesize").innerHTML = "Размер " + Math.floor(pos * 100 / ssize) + "%";
    
                 req.open("GET", url, true);
                req.responseType = "arraybuffer";
                req.setRequestHeader('id', idname);
                 req.setRequestHeader('pos', pos);
                    req.send();
    
            }
        
         }
 
     }
 
     req.send();
  
/*      chatSocket.onopen = function(e){
 
         chatSocket.send(JSON.stringify({
             'file_name': idname,
             'pos': pos
         }));
     };
 
     chatSocket.onmessage = function(e) {
 
         blobs.push(e.data);
 
         if(e.data.size < part_size){
 
             link.href = URL.createObjectURL(new Blob(blobs, {type: "application/zip"}));
     
             link.click();
             
             URL.revokeObjectURL(link.href);             
 
             chatSocket.close();
 
             document.querySelector("#tablecolumnfilesize").innerHTML = "Размер";
 
         }
         else{
 
             pos = pos + part_size;
 
             document.querySelector("#tablecolumnfilesize").innerHTML = "Размер " + Math.floor(pos * 100 / ssize) + "%";
 
             chatSocket.send(JSON.stringify({
                 'file_name': idname,
                 'pos': pos
             }));
     
 
         }
 
     };
 
     chatSocket.onclose = function(e) {
         //console.error('Chat socket closed unexpectedly');
     };
 */ 
 }
 
 function addCatalog(){

    var filename = prompt("Добавить папку", "Новая папка");

    if(filename){

        var url = "/addfolder/";
        var data = {};
        data.filename = filename;
        data.parent_id = $('#parent_id').val();
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {

                location.href = "/files?parent_id=" + data.parent_id;

            },
            error: function(){
                console.log("error")
            }
        })
    }

}

function addFile(){

    var filename = prompt("Добавить файл", "Новый файл");

    if(filename){

        $('#editidname').attr('data-idname', newUid());
        $('#editidname').html(filename);

        $('#editidname').attr("data-isnew", true);

        $('#edittext').val('');

        $('#popupet').show();

    }

}




function setToBasket(idname){

    var url = "/settobasket/";
    var data = {};
    data.idname = idname;
     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {

            location.href = "/files?parent_id=" + data.parent_id;

        },
         error: function(){
             console.log("error")
         }
     })

}

function saveFile(){

    var idname = $('#editidname').attr('data-idname');
    var filename = $('#editidname').html();

    var is_new = $('#editidname').attr("data-isnew");

    var req = new XMLHttpRequest();

    var data = $('#edittext').val();

    var url = "";
    req.open("POST", url, false);
    req.setRequestHeader('id', newUid());
    req.setRequestHeader('parentid', $('#parent_id').val());
    req.setRequestHeader('filename', encodeURIComponent(filename));
    req.setRequestHeader('part', 0);
    req.setRequestHeader('size', data.length);

    req.send(data);

    req.onreadystatechange = function () { // (3)

        if (this.readyState != 4) return;

        // button.innerHTML = 'Готово!';

        if (this.status != 200) {

            setTimeout(onError, 1000);
            // alert(this.status + ': ' + this.statusText);

        } else {

            onLoad();

        }

    }    


    if(!is_new){
        setToBasket(idname);
    }

    location.reload();

}



function rename(idname, filename){

    var filename = prompt("Переименовать", filename);

    if(filename){

        var url = "/filerename/";
        var data = {};
        data.filename = filename;
        data.idname = idname;
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {

                location.href = "/files?parent_id=" + data.parent_id;

            },
            error: function(){
                console.log("error")
            }
        })
    }
}

function str2ab(str) {
    var buf = new ArrayBuffer(str.length * 2); // 2 bytes for each char
    var bufView = new Uint16Array(buf);
    for (var i = 0, strLen = str.length; i < strLen; i++) {
      bufView[i] = str.charCodeAt(i);
    }
    return buf;
  }

function editText(idname, filename){

    var url = "/getfile/?id=" + idname;
    $.ajax({
        url: url,
        type: 'POST',
        cache: true,
        success: function (data) {

            $('#editidname').attr("data-idname", idname);
            $('#editidname').html(filename);
            $('#popupet').show();

            $('#edittext').html(data);

        },
        error: function(){
            console.log("error")
        }
    })



}

function createExternalLink(idname, filename){

    var url = "/el/";
    var eluid = newUid();
    var data = {};
    data.eluid = eluid;
    data.idname = idname;
    $.ajax({
        url: url,
        type: 'POST',
        cache: true,
        data: data,
        success: function (data) {

            reltext = "https://downloadfilesdrive.site:8005/files/" + eluid + "=download";

            $('#externallinkfile').attr("data-idname", idname);
            $('#externallinkfile').html(filename);
            $('#externallinkidname').html(reltext);
            $('#popupexternallink').show();    

            navigator.clipboard.writeText(reltext)
            .then(() => {
                $('#externallinkcopied').show(); 
            })
            .catch(err => {
              console.log('Something went wrong', err);
            });            


        },
        error: function(){
            console.log("error")
        }
    })



}

function showReminder(idname, filename){

    document.querySelector('#reminderfile').innerHTML = filename;
    document.querySelector('#reminderfileid').innerHTML = idname;
    document.querySelector('#popupreminder').style.display = 'block';

}


function createReminder(){

    var filename = document.querySelector('#reminderfile').innerHTML;
    var idname = document.querySelector('#reminderfileid').innerHTML;
    var comments = document.querySelector('#editremindertext').value;
    var remind = document.querySelector('#datetimereminder').value;

    var curDate = new Date(remind)
    var strDate = curDate.toISOString().replaceAll('-', '').replaceAll(':', '').replaceAll('T', '').substr(0, 14);

    var url = "/remind/";
    var eluid = newUid();
    var data = {};
    data.comments = comments;
    data.idname = idname;
    data.remind = strDate;
    $.ajax({
        url: url,
        type: 'POST',
        cache: true,
        data: data,
        success: function (data) {

            if(data.success){

                window.location.reload();
                //document.querySelector('#popupreminder').style.display = 'none';
            } else {
                alert(data.message);
            }
        },
        error: function(){
            console.log("error")
        }
    })

}


function addUploadLink(){

    if(!$('#parent_id').val()){

        alert('Нужно зайти в папку');

    } else {

        var url = "/ul/";
        var eluid = newUid();
        var data = {};
        data.eluid = eluid;
        data.parentid = $('#parent_id').val();
        $.ajax({
            url: url,
            type: 'POST',
            cache: true,
            data: data,
            success: function (data) {

                if(!data.success) {
                    alert('Не удалось создать ссылку загрузки')
                } else {

                    reltext = "https://uploadfilesdrive.site:8003/files/" + eluid;

                    $('#externallinkfile').attr("data-idname", '');
                    $('#externallinkfile').html('');
                    $('#externallinkidname').html(reltext);
                    $('#popupexternallink').show();    

                    navigator.clipboard.writeText(reltext)
                    .then(() => {
                        $('#externallinkcopied').show(); 
                    })
                    .catch(err => {
                    console.log('Something went wrong', err);
                    });            
                }

            },
            error: function(){
                console.log("error")
            }
        })
    }


}

function newUploadLinkId(parent_id){

    var url = "/ul/";
    var eluid = newUid();
    var data = {};
    data.eluid = eluid;
    data.parentid = parent_id;
    $.ajax({
        url: url,
        type: 'POST',
        cache: true,
        data: data,
        success: function (data) {

            if(!data.success) {
                alert('Не удалось создать ссылку загрузки')
            } else {

                addUploadLinkId(parent_id);
                    
            }

        },
        error: function(){
            console.log("error")
        }
    })                   

}


function addUploadLinkId(parent_id){

    var url = "/ulbyparentid/";
    var data = {};
    data.parent_id = parent_id;

    $.ajax({
        url: url,
        type: 'GET',
        cache: true,
        data: data,
        success: function (data) {

            if(!data.success) {
                alert('Не удалось получить ссылку загрузки')
            } else {

                if(data.id) {

                    reltext = "https://uploadfilesdrive.site:8003/files/" + data.id;

                    document.querySelector('#createnewuploadlink').addEventListener('click', function(event) {
                        newUploadLinkId(parent_id);
                    });

                    $('#externallinkfileid').html(parent_id);
                    $('#externallinkfile').attr("data-idname", '');
                    $('#externallinkfile').html('');
                    $('#externallinkidname').html(reltext);
                    $('#externallinkenabled').html('expired ' + data.enabled);
                    $('#popupexternallink').show();    

                    navigator.clipboard.writeText(reltext)
                    .then(() => {
                        $('#externallinkcopied').show(); 
                    })
                    .catch(err => {
                    console.log('Something went wrong', err);
                    });            

                } else {

                    newUploadLinkId(parent_id);



                }
            }

        },
        error: function(){
            console.log("error")
        }
    });
            
/*
    var url = "/ul/";
    var eluid = newUid();
    var data = {};
    data.eluid = eluid;
    data.parentid = parent_id;
    $.ajax({
        url: url,
        type: 'POST',
        cache: true,
        data: data,
        success: function (data) {

            if(!data.success) {
                alert('Не удалось создать ссылку загрузки')
            } else {

                reltext = "https://uploadfilesdrive.site:8003/files/" + eluid;

                $('#externallinkfile').attr("data-idname", '');
                $('#externallinkfile').html('');
                $('#externallinkidname').html(reltext);
                $('#popupexternallink').show();    

                navigator.clipboard.writeText(reltext)
                .then(() => {
                    $('#externallinkcopied').show(); 
                })
                .catch(err => {
                console.log('Something went wrong', err);
                });            
            }

        },
        error: function(){
            console.log("error")
        }
    })
*/

}


function keyUpContractor(e) {
	
	var t = $('#contractor').val();
    var url = "/contractorsfilter/";
    var data = {};
    data.search_filter = t;
     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {
            $("#contractors").empty();

            $.each(data.contractors, function(key, value) {
                $("#contractors").append('<option value="' + value.name + '" data-id1c="' + value.id1c + '"></option>');
            })
         },
         error: function(){
             console.log("error")
         }
     })
}

function keyUpContractorL(e) {
	
	var t = $('#contractor').val();
    var url = "/contractorsfilter/";
    var data = {};
    data.search_filter = t;
     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {

             if(data.mobile_mode)
                font_size = 'xxx-large'
             else
                font_size = 'normal'

            $("#contractorsList").empty();

            $.each(data.contractors, function(key, value) {

                $("#contractorsList").append(
                    '<li>'
                        + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                            + '<div style="float: left; width: 100%">'
                                + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" onclick="onContractorClick(\'' + value.name + '\', \'' + value.id1c + '\')" style="font-size: ' + font_size + '; white-space: normal" data-id1c="' + value.id1c + '">' + value.name + '</a>'
                            + '</div>'
                        + '</div>'
                    + '</li>');

            })
         },
         error: function(){
             console.log("error")
         }
     })
}

function onContractorClick(name, id1c){

   $('#contractor').val(name);
   $('#contractor').attr('id1c', id1c);

   $("#contractorsList").empty();

}


function keyUpWarehouse(e) {
    var t = $('#warehouse').val();
    var url = "/warehousesfilter/";
    var data = {};
    data.search_filter = t;
     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {

             if(data.mobile_mode)
                font_size = 'xxx-large'
             else
                font_size = 'normal'

            $("#warehouseList").empty();

            $.each(data.warehouses, function(key, value) {

                $("#warehouseList").append(
                    '<li>'
                        + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                            + '<div style="float: left; width: 100%">'
                                + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" onclick="onWarehouseClick(\'' + value.name + '\', \'' + value.id1c + '\')" style="font-size: ' + font_size + '; white-space: normal" data-id1c="' + value.id1c + '">' + value.name + '</a>'
                            + '</div>'
                        + '</div>'
                    + '</li>');

            })
         },
         error: function(){
             console.log("error")
         }
     })
}

function onWarehouseClick(name, id1c){

   $('#warehouse').val(name);
   $('#warehouse').attr('id1c', id1c);

   $("#warehouseList").empty();

}

function keyUpProduct(e) {
    var t = $('#product').val();
    var url = "/goodsfilter/";
    var data = {};
    data.search_filter = t;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {

             if(data.mobile_mode)
                font_size = 'xxx-large'
             else
                font_size = 'normal'

             $("#productList").empty();

            $.each(data.products, function(key, value) {
                $("#productList").append(
                    '<li>'
                        + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                            + '<div style="float: left; width: 100%">'
                                + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" onclick="onProductClick(\'' + value.fullname + '\', \'' + value.id1c + '\')" style="font-size: ' + font_size + '; white-space: normal" data-id1c="' + value.id1c + '">' + value.fullname + '</a>'
                            + '</div>'
                        + '</div>'
                    + '</li>');
            })
         },
         error: function(){
             console.log("error")
         }
     })
}

function onProductClick(name, id1c){

   $('#product').val(name);
   $('#product').attr('id1c', id1c);

   $('#сharacteristic').val('');
   $('#сharacteristic').attr('id1c', '');

   $('#warehouseСell').val('');
   $('#warehouseСell').attr('id1c', '');

   $("#productList").empty();

}

function keyUpCharactreristic(e) {

    if ($('#product').val()
        && $('#product').attr('id1c')) {

        var t = $('#сharacteristic').val();
        var url = "/characteristicsfilter/";
        var data = {};
        data.search_filter = t;
        data.product = $('#product').attr('id1c');

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {

                 if(data.mobile_mode)
                    font_size = 'xxx-large'
                 else
                    font_size = 'normal'


                $("#сharacteristicList").empty();

                $.each(data.characteristics, function (key, value) {

                    $("#сharacteristicList").append(
                        '<li>'
                            + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                                + '<div style="float: left; width: 100%">'
                                    + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" onclick="onCharacteristicClick(\'' + value.name + '\', \'' + value.id1c + '\')" style="font-size: ' + font_size + '; white-space: normal" data-id1c="' + value.id1c + '">' + value.name + '</a>'
                                + '</div>'
                            + '</div>'
                        + '</li>');
                    })
            },
            error: function () {
                console.log("error")
            }
        })
    }
}

function onCharacteristicClick(name, id1c){

   $('#сharacteristic').val(name);
   $('#сharacteristic').attr('id1c', id1c);

   $("#сharacteristicList").empty();

}

function keyUpWarehouseCell(e) {

    if ($('#warehouse').val()
        && $('#warehouse').attr('id1c')) {

        var t = $('#warehouseСell').val();
        var url = "/warehousecellsfilter/";
        var data = {};
        data.search_filter = t;
        data.warehouse = $('#warehouse').attr('id1c');

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {

                 if(data.mobile_mode)
                    font_size = 'xxx-large'
                 else
                    font_size = 'normal'


                $("#warehouseСellList").empty();

                $.each(data.warehousecells, function (key, value) {

                    $("#warehouseСellList").append(
                        '<li>'
                            + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                                + '<div style="float: left; width: 100%">'
                                    + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" onclick="onWarehouseCellClick(\'' + value.name + '\', \'' + value.id1c + '\')" style="font-size: ' + font_size + '; white-space: normal" data-id1c="' + value.id1c + '">' + value.name + '</a>'
                                + '</div>'
                            + '</div>'
                        + '</li>');
                    })
            },
            error: function (e1, e2, e3) {
                console.log("error")
            }
        })
    }
}

function onWarehouseCellClick(name, id1c){

   $('#warehouseСell').val(name);
   $('#warehouseСell').attr('id1c', id1c);

   $("#warehouseСellList").empty();

}


function delBthClick(e){
    if($("#quan_" + e).html() != '')
        addToBasket(e, -1)
}

function addBthClick(e) {
    addToBasket(e, 1)
}

function addToBasket(e, quantity){
    console.log(e)
    var url = "/add_to_basket/";
    var data = {};
    data.product_id1c = e;
    data.product_quantity = quantity;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {
             //console.log(data)
             $("#quan_" + e).html(data.quantity);
             $("#basket").html("Корзина (" + data.basket_quantity + ")");
         },
         error: function(){
             console.log("error")
         }
     })

}

function keyUpGoodsFilter(e) {
    var t = $('#goodsFilter').val();
    var url = "/goodsfilter/";
    var data = {};
    data.search_filter = t;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {

             if(data.mobile_mode)
                font_size = 'xxx-large'
             else
                font_size = 'normal'

            $("#goodsList").empty();

            $.each(data.products, function(key, value) {
                var tt = value.title;
                $("#goodsList").append(
                    '<li>'
                        + '<div class="p-2" style="float: left; width: 100%; display: flex; align-items: center">'
                            + '<div style="float: left; width: 65%">'
                                + '<a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#" style="font-size: ' + font_size + '; white-space: normal" >' + value.fullname + '</a>'
                            + '</div>'
                            + '<div style="float: left; width: 35%; height: 100%; display: flex; align-items: center">'
                                + '<button id="del_' + value.id1c + '" onClick="delBthClick(\'' + value.id1c + '\')" class="btn btn-danger" style="font-size: ' + font_size + '; float: left; width: 30%">-</button>'
                            + '<div id="quan_' + value.id1c + '" style="float: left; width: 40%; font-size: ' + font_size + '; text-align: center">' + value.quantity
                            + '</div>'
                                + '<button id="add_' + value.id1c + '" onClick="addBthClick(\'' + value.id1c + '\')" class="btn btn-success" style="font-size: ' + font_size + '; float: left; width: 30%">+</button>'
                            + '</div>'
                        + '</div>'
                    + '</li>');
            })
         },
         error: function(){
             console.log("error")
         }
     })

}

function onInputContractor(event){
    var val = document.getElementById("contractor").value;
    var opts = document.getElementById('contractors').childNodes;
    var found = false
    for (var i = 0; i < opts.length; i++) {
      if (opts[i].value === val) {

        document.getElementById("output").value = opts[i].dataset.id1c;

        found = true

        break;
      }
    }
    if(!found)
        document.getElementById("contractor").value = "";
}

function checkoutOrder(e){

    if ($('#contractor').val()
        && $('#contractors option').val()
        && $('#contractors option').data('id1c')){

        var url = "/checkout/";
        var data = {};
        data.contractor = $('#contractors option').data('id1c');
        data.comment = $('#comment').val();

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "/";
             },
             error: function(){
                 console.log("error")
             }
         })



    }

}

function saveInvent(e){

    if ($('#warehouse').val()
        && $('#product').val()){

        var url = "/saveinvent/";
        var data = {};
        data.warehouse = $('#warehouse').attr('id1c');
        data.product = $('#product').attr('id1c');
        data.сharacteristic = $('#сharacteristic').attr('id1c');
        data.warehouseCell = $('#warehouseСell').attr('id1c');
        data.quantity = $('#quantity').val();
        data.comment = $('#comment').val();

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "/invents/?wid=" + $('#warehouse').attr('id1c');

             },
             error: function(jqXHR, textStatus, errorThrown){
                 console.log("error")
             }
         })



    }

}

function saveComment(e){

    if ($('#comment').val()){

        var url = "/savecomment/";
        var data = {};
        data.id = $('#taskid').val();
        data.comment = $('#comment').val();

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "";
             },
             error: function(){
                 console.log("error")
             }
         })



    }

}

function saveDmComment(e){

    if ($('#comment').val()){

        var url = "/savedmcomment/";
        var data = {};
        data.dmid = $('#dmid').val();
        data.id = $('#taskid').val();
        data.comment = $('#comment').val();

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "";
             },
             error: function(){
                 console.log("error")
             }
         })



    }

}

function saveCommentReport(e){

    if ($('#comment').val()){

        var url = "/savecommentreport/";
        var data = {};
        data.id = $('#taskid').val();
        data.comment = $('#comment').val();

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "/";
             },
             error: function(){
                 console.log("error")
             }
         })



    }

}

function executeTask(e){

        var url = "/executetask/";
        var data = {};
        data.id = $('#taskid').val();

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "/tasks";
             },
             error: function(){
                 console.log("error")
             }
         })


}

function executeDmTask(e){

        var url = "/executedmtask/";
        var dmid = $('#dmid').val();
        var data = {};
        data.id = $('#taskid').val();
        data.dmid = dmid;

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);

                 if(data.result){
                    location.href = "/dmtaskstouser/?id=" + dmid;
                 }
                 else{

                 }
             },
             error: function(){
                 console.log("error")
             }
         })


}

function getDmTasks(e){

        var url = "/dmtaskstouser/";
        var dmid = $('#dmid').val();
        var data = {};
        data.id = $('#taskid').val();
        data.dmid = dmid;

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);

                 if(data.result){
                    location.href = "/dmtaskstouser/?id=" + dmid;
                 }
                 else{

                 }
             },
             error: function(){
                 console.log("error")
             }
         })


}

function checkoutAccept(e){

    if ($('#contractor').val()
        && $('#currency').val()
        && $('#sum').val()){

        var url = "/add_accept/";
        var data = {};
        data.contractor = $('#contractor').attr('id1c');
        data.sum = $('#sum').val();
        data.currency = $('#currency').val();
        data.comment = $('#comment').val();
        data.orderNumber = $('#orderNumber').val();
        data.orderDate = $('#orderDate').val();

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);
                 location.href = "/";
             },
             error: function(){
                 console.log("error")
             }
         })



    }

}

function addDmTask(e){

    if ($('#name').val()
        && $('#executor').val()
        && $('#description').val()){

        var dmid = $('#dmid').val();
        var url = "/adddmtask/";
        var data = {};
        data.dmid = dmid;
        data.name = $('#name').val();
        data.description = $('#description').val();
        data.executor = $('#executor').val();

         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log(data);

                 if(data.result){
                    location.href = "/dmtaskstouser/?id=" + dmid;
                 }
                 else{

                 }

             },
             error: function(){
                 console.log("error")
             }
         })



    }

}

function send_to_1c(id1c){

    var url = "/sendto1c/";
    var data = {};
    data.id1c = id1c;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {
             console.log(data);
             if (data.success == true)
                 location.reload();
         },
         error: function(){
             console.log("error")
         }
     })


}

function sendto1c_acc(id1c){

    var url = "/sendto1c_acc/";
    var data = {};
    data.id1c = id1c;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {
             console.log(data);
             if (data.success == true)
                 location.reload();
         },
         error: function(){
             console.log("error")
         }
     })


}

function sendto1c_invent(id1c){

    var url = "/sendto1c_invent/";
    var data = {};
    data.id1c = id1c;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {
             console.log(data);
             if (data.success == true)
                 location.reload();
         },
         error: function(err1, err2, err3){
             console.log("error")
         }
     })


}

function sendto1c_recipe(id1c){

    var url = "/sendto1c_recipe/";
    var data = {};
    data.id1c = id1c;

     $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function (data) {
             console.log(data);
             if (data.success == true)
                 location.reload();
         },
         error: function(err1, err2, err3){
             console.log("error")
         }
     })


}

