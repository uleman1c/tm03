function addCatalog(){

    var filename = prompt("Добавить папку", "Новая папка");

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

