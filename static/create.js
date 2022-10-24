
var files = '';
var idEl = '#procent';

var uuid = '';

var numFile = 0;
var numPart = 0;
var startingByte = 0;
var endindByte = 0;

var errorCount = 0;

var upload_chunk_size = 120000;

function onLoad() {

    numPart = numPart + 1;

    startingByte = endindByte;

    var curFile = files[numFile];

    $(idEl).html(curFile.name + " " + Math.floor(startingByte * 100 / curFile.size) + "%, ошибок " + errorCount);

    if (startingByte < curFile.size) {


    }
    else {

        numFile = numFile + 1;

        startingByte = 0;

    }

    sendNext();

}

function onError() {

    if (true || errorCount < 10) {

        errorCount = errorCount + 1;

        sendPartOfFile();

    }

}

function sendPartOfFile() {

    var curFile = files[numFile];

    var blob = curFile.slice(startingByte, endindByte);

    var req = new XMLHttpRequest();

    var url = "";
    req.open("POST", url, true);
    req.setRequestHeader('id', uuid);
    req.setRequestHeader('filename', encodeURIComponent(curFile.name));
    req.setRequestHeader('part', numPart);

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

    req.send(blob);

}

function sendNext() {

    if (numFile < files.length) {

        var curFile = files[numFile];

        if (startingByte == 0) {

            let u = Date.now().toString(16) + Math.random().toString(16) + '0'.repeat(16);
            uuid = [u.substr(0, 8), u.substr(8, 4), '4000-8' + u.substr(13, 3), u.substr(16, 12)].join('-');

        }

        endindByte = startingByte + upload_chunk_size;
        if (endindByte > curFile.size) {
            endindByte = curFile.size;
        }

        sendPartOfFile();


    } else {

        location.reload();

    }

}

function big_file_upload(f){
	
	upload_chunk_size = 120000;
	
	files = f[0].files;

    numFile = 0;

    startingByte = 0;

    sendNext();

}




class FilesSender {

    constructor(curFiles, curIdEl, cur_upload_chunk_size = 120000) {

        this.files = curFiles;
        this.idEl = curIdEl;

        this.numFile = 0;
        this.numPart = 0;
        this.startingByte = 0;
        this.endindByte = 0;

        this.errorCount = 0;

        this.upload_chunk_size = cur_upload_chunk_size;

        this.req = new XMLHttpRequest();

    }

    onLoad(me) {

        me.numPart = me.numPart + 1;

        me.startingByte = me.endindByte;

        var curFile = me.files[me.numFile];

        $(me.idEl).html(Math.floor(me.startingByte * 100 / curFile.size) + "%");

        if (me.startingByte < curFile.size) {


        }
        else {

            me.numFile = me.numFile + 1;

            me.startingByte = 0;

        }

        me.sendNext(me);

    }

    onError(me) {

        if (me.errorCount < 10) {

            me.errorCount = me.errorCount + 1;

            me.doSend(me);

        }

    }

    sendNext(me) {

        if (me.numFile < me.files.length) {

            var curFile = me.files[me.numFile];

            if (me.startingByte == 0) {

                let u = Date.now().toString(16) + Math.random().toString(16) + '0'.repeat(16);
                me.uuid = [u.substr(0, 8), u.substr(8, 4), '4000-8' + u.substr(13, 3), u.substr(16, 12)].join('-');

            }

            me.endindByte = me.startingByte + me.upload_chunk_size;
            if (me.endindByte > curFile.size) {
                me.endindByte = curFile.size;
            }

            me.blob = curFile.slice(me.startingByte, me.endindByte);


            // var me = me;

            me.doSend(me);


        } else {

            location.reload();

        }



    }


    doSend(me) {
        
		var curFile = me.files[me.numFile];

		var url = "";
		me.req.open("POST", url, true);
		me.req.setRequestHeader('id', me.uuid);
		me.req.setRequestHeader('filename', encodeURIComponent(curFile.name));
		me.req.setRequestHeader('part', me.numPart);
		
		me.req.onreadystatechange = function() { // (3)
		
		  if (this.readyState != 4) return;

		  // button.innerHTML = 'Готово!';

		  if (this.status != 200) {
			
			setTimeout(me.onError, 1000, me);
			// alert(this.status + ': ' + this.statusText);
			
		  } else {
			
			me.onLoad(me);
			
		  }

		}
		
		try {

			me.req.send(me.blob);

		} catch (err) {

			setTimeout(me.onError, 1000, me);

		}
		
		
    }

}



function big_file_upload3(f) {

    curFilesSender = new FilesSender(f[0].files, "#procent");

    curFilesSender.sendNext(curFilesSender);

}
	

function send_part(blob, curUid, curFile, numPart, endindByte, upload_chunk_size, reader){
	
	url = "";
	const req = new XMLHttpRequest();
	req.open("POST", url, true);
	req.setRequestHeader('id', curUid);
	req.setRequestHeader('filename', encodeURIComponent(curFile.name));
	req.setRequestHeader('part', numPart);
	req.onload = (event) => {

		numPart = numPart + 1;

		startingByte = endindByte;

		$("#procent").html(Math.floor(startingByte * 100 / curFile.size) + "%");

		if (startingByte < curFile.size) {

			endindByte = startingByte + upload_chunk_size;
			if (endindByte > curFile.size) {
				endindByte = curFile.size;
			}

			blob = curFile.slice(startingByte, endindByte);
			reader.readAsBinaryString(blob);
		}
		else {

			const req2 = new XMLHttpRequest();
			req2.open("POST", url, true);
			req2.setRequestHeader('id', curUid);
			req2.setRequestHeader('filename', encodeURIComponent(curFile.name));
			req2.setRequestHeader('part', -1);
			req2.setRequestHeader('size', curFile.size);
			req2.onload = (event) => {

				i = i + 1;

				if (i < curFiles.length) {

					curFile = curFiles[i];
					curUid = crypto.randomUUID();

					console.log(curFile.name)

				} else {

					location.reload();

				}

			};

			req2.send(this.result);

			req2.onprogress = function(event) {
			  if (event.lengthComputable) {
				// alert(`Received ${event.loaded} of ${event.total} bytes`);
			  } else {
				// alert(`Received ${event.loaded} bytes`); // no Content-Length
			  }

			};

			req2.onerror = function(event) {
			   alert("Request failed");
			};		

		}

	};

	req.send(blob);
	
	req.onprogress = function(event) {
	  if (event.lengthComputable) {
		// alert(`Received ${event.loaded} of ${event.total} bytes`);
	  } else {
		// alert(`Received ${event.loaded} bytes`); // no Content-Length
	  }

	};

	req.onerror = function(event) {
	   
	   
	   console.log("Request failed");
	   
	   setTimeout(send_part, 1000, blob, curUid, curFile, numPart, endindByte, upload_chunk_size, reader);
	   
	};		


}
	
function big_file_upload2(f){
	
	var upload_chunk_size = 120000;
	
	var i = 0; 
	var curFiles = f[0].files;
	
	let u = Date.now().toString(16) + Math.random().toString(16) + '0'.repeat(16);
	let guid = [u.substr(0,8), u.substr(8,4), '4000-8' + u.substr(13,3), u.substr(16,12)].join('-');	

	var curUid = guid; //crypto.randomUUID();
		
	var curFile = curFiles[i];
	
	var reader = new FileReader();

    var numPart = 0;
	var startingByte = 0;
 
	var endindByte = startingByte + upload_chunk_size;
	if(endindByte > curFile.size){
		endindByte = curFile.size;
	}
			
    var blob = curFile.slice(startingByte, endindByte);

	reader.onloadend = function(e) { 

		send_part(blob, curUid, curFile, numPart, endindByte, upload_chunk_size, reader);

    };

   //     const blob = new Blob(["abc123"], { type: "text/plain" });

/*
        $.post('', {
			id:curUid,
			filename:curFile.name,
            part: numPart,
			data:this.result,
        }, function (data) {

            numPart = numPart + 1;

			startingByte = endindByte + 1;
			
			if(startingByte < curFile.size){

				endindByte = startingByte + upload_chunk_size;
				if(endindByte > curFile.size){
					endindByte = curFile.size;
				}
				
				blob = curFile.slice(startingByte, endindByte);
				reader.readAsBinaryString(blob);
			}
			else {

                $.post('', {
                    id: curUid,
                    filename: curFile.name,
                    part: -1,
                }, function (data) {

                    i = i + 1;

                    if (i < curFiles.length) {

                        curFile = curFiles[i];
                        curUid = crypto.randomUUID();

                        console.log(curFile.name)

                    } else {



                    }

                }).fail(function (e) {
                    alert("error");
                });
				
			}

        }).fail(function(e) {
			alert( "error" );
		});
*/			
		
	reader.onprogress = function(evt) { 
		console.log(evt.loaded, evt.total) 
	}
		
	reader.onload = function(e) {
		console.log(startingByte);
	};
		  
    reader.readAsArrayBuffer(blob);
	
}

function big_file_uploadold(f){
	
	var upload_chunk_size = 120000;
	
	var i = 0; 
	var curFiles = f[0].files;
		
	var curUid = crypto.randomUUID();
		
	var curFile = curFiles[i];
	
	var reader = new FileReader();

    var numPart = 0;
	var startingByte = 0;
 
	var endindByte = startingByte + upload_chunk_size;
	if(endindByte > curFile.size){
		endindByte = curFile.size;
	}
			
    var blob = curFile.slice(startingByte, endindByte);

	reader.onloadend = function(e) { 

        url = "";
        const req = new XMLHttpRequest();
        req.open("POST", url, true);
        req.setRequestHeader('id', curUid);
        req.setRequestHeader('filename', encodeURIComponent(curFile.name));
        req.setRequestHeader('part', numPart);
        req.onload = (event) => {

            numPart = numPart + 1;

            startingByte = endindByte + 1;

            if (startingByte < curFile.size) {

                endindByte = startingByte + upload_chunk_size;
                if (endindByte > curFile.size) {
                    endindByte = curFile.size;
                }

                blob = curFile.slice(startingByte, endindByte);
                reader.readAsBinaryString(blob);
            }
            else {

                const req2 = new XMLHttpRequest();
                req2.open("POST", url, true);
                req2.setRequestHeader('id', curUid);
                req2.setRequestHeader('filename', encodeURIComponent(curFile.name));
                req2.setRequestHeader('part', -1);
                req2.onload = (event) => {

                    i = i + 1;

                    if (i < curFiles.length) {

                        curFile = curFiles[i];
                        curUid = crypto.randomUUID();

                        console.log(curFile.name)

                    } else {



                    }

                };

                req2.send(this.result);

            }

        };

        req.send(this.result);

    };

   //     const blob = new Blob(["abc123"], { type: "text/plain" });

/*
        $.post('', {
			id:curUid,
			filename:curFile.name,
            part: numPart,
			data:this.result,
        }, function (data) {

            numPart = numPart + 1;

			startingByte = endindByte + 1;
			
			if(startingByte < curFile.size){

				endindByte = startingByte + upload_chunk_size;
				if(endindByte > curFile.size){
					endindByte = curFile.size;
				}
				
				blob = curFile.slice(startingByte, endindByte);
				reader.readAsBinaryString(blob);
			}
			else {

                $.post('', {
                    id: curUid,
                    filename: curFile.name,
                    part: -1,
                }, function (data) {

                    i = i + 1;

                    if (i < curFiles.length) {

                        curFile = curFiles[i];
                        curUid = crypto.randomUUID();

                        console.log(curFile.name)

                    } else {



                    }

                }).fail(function (e) {
                    alert("error");
                });
				
			}

        }).fail(function(e) {
			alert( "error" );
		});
*/			
		
	reader.onprogress = function(evt) { 
		console.log(evt.loaded, evt.total) 
	}
		
	reader.onload = function(e) {
		console.log(startingByte);
	};
		  
    reader.readAsArrayBuffer(blob);
	
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

