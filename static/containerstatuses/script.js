var ctj = '';

arFiles = [];
arTcs = [];
arCs = [];

document.addEventListener("DOMContentLoaded", function(){

    ctj = JSON.parse(container_statuses_h.replaceAll('&quot;', '"'));

    ctj.forEach(element => {
        
        element.Файлы.forEach(felement => {
            
            arFiles.push(felement.ИдентификаторФайла);

        });

        arTcs.push(element.ТранспортныйКонтейнер);

        element.Контейнеры.forEach(celement => {
            
            arCs.push(element.ИдентификаторКонтейнера);

        });

    });


    requestPost("?lfv=1", arFiles, Lfv);

});

function Lfv(responseText) {

    JSON.parse(responseText)['version'].forEach(velement => {

        ctj.forEach(element => {
        
            element.Файлы.forEach(felement => {

                if(felement.ИдентификаторФайла == velement.file_id){

                    felement.Версия = velement.version;
                    felement.ИдентификаторВерсии = velement.id;

                }

            });

        });

    });

    requestPost("?ftc=1", arTcs, Ftc);

}

function Ftc(responseText){

    JSON.parse(responseText)['files'].forEach(felement => {

        ctj.forEach(element => {
        
            if(element.ТранспортныйКонтейнер == felement.tc_id){

                comments = '';
                if(felement.comments){
                    comments = felement.comments;
                }

                element.Файлы.push({'ИдентификаторКонтейнера': element.ТранспортныйКонтейнер, 'ИдентификаторФайла': felement.id, 'Автор': felement.user,
                'ДатаСоздания': felement.created, 'Имя': felement.name, 'Описание': comments, 'Расширение':felement.ext, 'in_t':true,
                'Картинка': picByExt(felement.ext), 'ИдентификаторВерсии': felement.version_id, 'Версия': felement.version});

                document.querySelector('#pic_' + element.ТранспортныйКонтейнер).innerHTML = '<img src="/static/attach.svg" alt="" style="width: 1em; ">';

            }
        });

    });

    requestPost("?fc=1", arCs, Fc);

}


function Fc(responseText){

    JSON.parse(responseText)['files'].forEach(felement => {

        ctj.forEach(element => {

            element.Контейнеры.forEach(celement => {
                
                if(celement.ИдентификаторКонтейнера == felement.c_id){

                    celement.ЕстьФайлы = true;

                    comments = '';
                    if(felement.comments){
                        comments = felement.comments;
                    }

                    element.Файлы.push({'ИдентификаторКонтейнера': celement.ИдентификаторКонтейнера, 'ИдентификаторФайла': felement.id, 'Автор': felement.user,
                    'ДатаСоздания': felement.created, 'Имя': felement.name, 'Описание': comments, 'Расширение':felement.ext, 'in_t':true,
                    'Картинка': picByExt(felement.ext), 'Версия': felement.version});

                    //document.querySelector('#pic_' + celement.ИдентификаторКонтейнера).innerHTML = '<img src="/static/attach.svg" alt="" style="width: 1em;">';

                }
            });
        });
    });

}


function picByExt(ext){

    if(ext == 'pdf'){
        return '/static/pdf.png'
    }
    if(ext == 'jpg'){
        return '/static/jpg.png'
    }
    if(ext == 'xls' || ext == 'xlsx'){
        return '/static/xls.png'
    }
    if(ext == 'doc' || ext == 'docx'){
        return '/static/doc.png'
    }

    return '';

}

function requestGet(url) {
    var req = new XMLHttpRequest();

    req.open("GET", url, false);

    req.onreadystatechange = function () {

        if (this.readyState != 4)
            return;

        // button.innerHTML = 'Готово!';
        if (this.status != 200) {
            //setTimeout(onError, 1000);
            // alert(this.status + ': ' + this.statusText);
        } else {
            //onLoad();
        }

    };

    req.send();

    return req.responseText;
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

function onTransportContainerClick(transportcontainer){

    selected = document.querySelector('#container_statuses .selected');
    if(selected)
        selected.classList.remove('selected');

    document.querySelector('#container_statuses [transportcontainer="' + transportcontainer + '"]').classList.add('selected')

    document.querySelector('#history_tc').classList.remove('hidden');
    document.querySelector('#edit_tc').classList.remove('hidden');

    containers_table = document.querySelector('#containers_table');
    containers_table.innerHTML = '';

    files_table = document.querySelector('#files_table');
    files_table.innerHTML = '';

    ctj.forEach(element => {
        
        if(element.ТранспортныйКонтейнер == transportcontainer){

            file_header = document.querySelector('#file_header');
            file_header.innerHTML = 'Файлы (транспортный контейнер ' + element.ВнутреннийНомер + ')';
            
            inputFile = document.querySelector('#inputFile');
            inputFile.setAttribute('type1c', 'doc');
            inputFile.setAttribute('name1c', 'ТранспортныйКонтейнер');
            inputFile.setAttribute('id1c', transportcontainer);
            inputFile.setAttribute('is_transcontainer', true);
            inputFile.setAttribute('transcontainer', transportcontainer);
            inputFile.setAttribute('container', '');
            inputFile.setAttribute('container_text', 'Транспортный контейнер ' + element.ВнутреннийНомер);

            document.querySelector('#add_file').style = 'display: block';

            document.querySelector('#zip_file').style = 'display: none';

            element.Контейнеры.forEach(сelement => {
                
                containers_table.innerHTML = containers_table.innerHTML + '<div id="container_row" class="themed-grid-row curpoint" onclick="onContainerClick(\'' + transportcontainer + '\', \'' + сelement.ИдентификаторКонтейнера +'\')" container="' + сelement.ИдентификаторКонтейнера + '">'
                +'    <div id="pic_' + сelement.ИдентификаторКонтейнера + '" class="themed-grid-col-row w5 tacntr" >' + (сelement.ЕстьФайлы ? '<img src="/static/attach.svg" alt="" style="width: 1em;">' : '') + '</div>'
                +'    <div class="themed-grid-col-row w45 tacntr" >' + сelement.КраткоеНаименованиеГруза + '</div>'
                    +'<div class="themed-grid-col-row w50 tacntr" >' + сelement.Комментарий + '</div>'
                +'</div>';

            });

            element.Файлы.forEach(сelement => {
                
                if(сelement.ИдентификаторКонтейнера == transportcontainer){

                    document.querySelector('#zip_file').style = 'display: block';

                    files_table.innerHTML = files_table.innerHTML 
                    + fileRow(сelement.ИдентификаторКонтейнера, сelement.ИдентификаторФайла, сelement.Имя, сelement.Расширение,
                        сelement.Картинка, сelement.Автор, сelement.ДатаСоздания, сelement.Описание, сelement.in_t, 'ТранспортныйКонтейнер', сelement.Версия); 
                }

            });



        };

    });

}

function onContainerClick(transportcontainer, container) {

    selected = document.querySelector('#containers_table .selected');
    if(selected)
        selected.classList.remove('selected');

    document.querySelector('#containers_table [container="' + container + '"]').classList.add('selected')

    files_table = document.querySelector('#files_table');
    files_table.innerHTML = '';

    document.querySelector('#zip_file').style = 'display: none';

    ctj.forEach(element => {
        
        if(element.ТранспортныйКонтейнер == transportcontainer){

            element.Контейнеры.forEach(сelement => {
                
                if(сelement.ИдентификаторКонтейнера == container){

                    file_header = document.querySelector('#file_header');
                    file_header.innerHTML = 'Файлы (контейнер ' + сelement.КраткоеНаименованиеГруза + ', ' + сelement.Комментарий + ')';
                    
                    inputFile = document.querySelector('#inputFile');
                    inputFile.setAttribute('type1c', 'doc');
                    inputFile.setAttribute('name1c', 'Контейнер');
                    inputFile.setAttribute('id1c', container);
                    inputFile.setAttribute('is_transcontainer', false);
                    inputFile.setAttribute('transcontainer', transportcontainer);
                    inputFile.setAttribute('container', container);
                    inputFile.setAttribute('container_text', 'контейнер ' + сelement.КраткоеНаименованиеГруза + ', ' + сelement.Комментарий);
        

                }
            });

            element.Файлы.forEach(сelement => {
                
                if(сelement.ИдентификаторКонтейнера == container){

                    document.querySelector('#zip_file').style = 'display: block';

                    files_table.innerHTML = files_table.innerHTML
                        + fileRow(сelement.ИдентификаторКонтейнера, сelement.ИдентификаторФайла, сelement.Имя, сelement.Расширение,
                            сelement.Картинка, сelement.Автор, сelement.ДатаСоздания, сelement.Описание, сelement.in_t, 'Контейнер', 
                            сelement.Версия, сelement.ИдентификаторВерсии); 
                }

            });

        };

    });


}

function fileRow(ИдентификаторКонтейнера, ИдентификаторФайла, Имя, Расширение, Картинка, Автор, ДатаСоздания, Описание, in_t, objname, version, ИдентификаторВерсии) {
    
    return      '<div id="container_row" class="themed-grid-row " >'
            +'      <div class="themed-grid-col-row w50" >' 
            +'         <a href="../fileversions?name=' + objname + '&id=' + ИдентификаторКонтейнера + '&cid=' + ИдентификаторФайла + '&in_t=' + (in_t ? '1' : '0') + '&cname=' + document.querySelector('#inputFile').getAttribute('container_text') + '" class="flex curpoint" style="display: contents;">'
            +'             <img src="/static/exchange.png" alt="" style="width: 2em; margin-top: .3em; margin-left: 2%; margin-right: 2%;" >'
            +'         </a>'
            +'        <div class="curpoint" style="display: contents;" onclick="onFileClick(\'' + (ИдентификаторВерсии ? ИдентификаторВерсии : ИдентификаторФайла) +'\', \'' + Расширение + '\', ' + (ИдентификаторВерсии ? true : in_t) + ',\'' + Имя + '.' + Расширение + '\')" container="' + ИдентификаторКонтейнера + '">'
            +'         <img src="' + Картинка + '" alt="" style="width: 1em; margin-right: 2%;">' + Имя + '.' + Расширение + (version ? ' ' + version : '')
            +'        </div>'
            +'      </div>'
            +'      <div class="themed-grid-col-row w10 tacntr" >' + Автор + '</div>'
            +'      <div class="themed-grid-col-row w10 tacntr" >' + ДатаСоздания + '</div>'
            +'      <div class="themed-grid-col-row w30 tacntr" >' + Описание + '</div>'
            +'   </div>';

}

function onFileClick(fileid, ext, in_t, full_name) {

    if(in_t){

        locationhref = '?fatt=' + fileid + "&ext=" + ext + "&full_name=" + full_name;

    } else {

        locationhref = '../attachedfile?type=ref&name=КонтейнерПрисоединенныеФайлы&id=' + fileid + "&ext=" + ext + "&full_name=" + full_name;
    }

    window.open(locationhref);

}

function zipFile() {

    inputFile = document.querySelector("#inputFile");

    container = inputFile.getAttribute('container');
    transcontainer = inputFile.getAttribute('transcontainer');

    if(container == ''){

        locationhref = '?ziptc=' + transcontainer;

    } else {

        locationhref = '?zipc=' + container;

    }

    window.open(locationhref);

}

function addFile() {
    
    document.querySelector('#exchange_id').value = '';

    document.querySelector('#inputFile').click();

}

function exchangeFile(id1c){

    document.querySelector('#exchange_id').value = id1c;

    document.querySelector('#inputFile').click();

}

function sendMessageToContainerFilesInfoBot(container_file_name) {
    
    container_text = document.querySelector('#inputFile').getAttribute('container_text')
        + ": присоединен файл " + container_file_name;

    var req = new XMLHttpRequest();

    var url = "?smtcfib=" + container_text;
    req.open("GET", url, true);
    req.onreadystatechange = function () { // (3)

        if (this.readyState != 4) return;

        // button.innerHTML = 'Готово!';

        if (this.status != 200) {

            // alert(this.status + ': ' + this.statusText);

        } else {


        }

    }

    req.send();


}

function onClickHistoryTc(){

    location = "../tchystory?id=" + document.querySelector('#container_statuses .selected').getAttribute('transportcontainer');

}

function onClickEditTc(){

    popupet = document.querySelector('#popupet');

    curTc = document.querySelector('#container_statuses .selected');

    popupet.querySelector('#tc_edit_header').innerHTML = 'Статус транспортного контейнера';
    popupet.querySelector('#transportcontainer').value = curTc.getAttribute('transportcontainer');
    popupet.querySelector('#tc_edit_internal_number').value = curTc.querySelector('#tc_internal_number').innerHTML;
    popupet.querySelector('#tc_edit_deliverer_number').value = curTc.querySelector('#tc_deliverer_number').innerHTML;
    popupet.querySelector('#tc_edit_product_supplier').value = curTc.querySelector('#tc_product_supplier').innerHTML;
    popupet.querySelector('#tc_edit_container_number').value = curTc.querySelector('#tc_container_number').innerHTML;
    popupet.querySelector('#tc_edit_destination').value = curTc.querySelector('#tc_destination').innerHTML;
    popupet.querySelector('#tc_edit_status').value = curTc.querySelector('#tc_status').innerHTML;
    popupet.querySelector('#tc_edit_planned_arrival_week').value = curTc.querySelector('#tc_planned_arrival_week').innerHTML;
    popupet.querySelector('#tc_edit_recipient').value = curTc.querySelector('#tc_recipient').innerHTML;

    strFreight = curTc.querySelector('#tc_freight_cost').innerHTML.replaceAll('&nbsp;', '').replaceAll(',', '.').split(' ');

    popupet.querySelector('#tc_edit_freight_cost').value = strFreight[0];
    popupet.querySelector('#tc_edit_freight_currency').value = strFreight[1];

    popupet.classList.remove('hidden');

    setPeriod();

}

function setPeriod(){

    popupet = document.querySelector('#popupet');

    if(!popupet.classList.contains('hidden')){

        dateIn = new Date();

        var year = dateIn.getFullYear();
        var month = dateIn.getMonth() + 1; // getMonth() is zero-based
        var day = dateIn.getDate();
        var hour = dateIn.getHours();
        var minute = dateIn.getMinutes();
        var second = dateIn.getSeconds();

        strMonth = (month < 10 ? '0' : '') + String(month)
        strDay = (day < 10 ? '0' : '') + String(day)
        strHour = (hour < 10 ? '0' : '') + String(hour)
        strMinute = (minute < 10 ? '0' : '') + String(minute)
        strSecond = (second < 10 ? '0' : '') + String(second)
        
        popupet.querySelector('#tc_edit_period').value =  strDay + '.' + strMonth + '.' + String(year) + ' ' + strHour + ':' + strMinute + ':' + strSecond;
    
        setTimeout(setPeriod, 1000);

    }

}

function saveStatus(){

    popupet = document.querySelector('#popupet');

    data = {'id': popupet.querySelector('#transportcontainer').value,
        'period': popupet.querySelector('#tc_edit_period').value,
        'internal_number': popupet.querySelector('#tc_edit_internal_number').value,
        'deliverer_number': popupet.querySelector('#tc_edit_deliverer_number').value,
        'product_supplier': popupet.querySelector('#tc_edit_product_supplier').value,
        'container_number': popupet.querySelector('#tc_edit_container_number').value,
        'destination': popupet.querySelector('#tc_edit_destination').value,
        'status': popupet.querySelector('#tc_edit_status').value,
        'planned_arrival_week': popupet.querySelector('#tc_edit_planned_arrival_week').value,
        'recipient': popupet.querySelector('#tc_edit_recipient').value,
        'freight_cost': popupet.querySelector('#tc_edit_freight_cost').value,
        'freight_currency': popupet.querySelector('#tc_edit_freight_currency').value,
    }

    requestPost('?saveStatus=1', data, function(response_text){

        if(JSON.parse(response_text).result){
            location.reload();
        }
    });


}


function onClickAddTc() {
    
    popupet = document.querySelector('#popupet');

    popupet.querySelector('#tc_edit_header').innerHTML = 'Статус транспортного контейнера ';
    popupet.querySelector('#transportcontainer').value = '';
    popupet.querySelector('#tc_edit_internal_number').value = '';
    popupet.querySelector('#tc_edit_deliverer_number').value = '';
    popupet.querySelector('#tc_edit_product_supplier').value = '';
    popupet.querySelector('#tc_edit_container_number').value = '';
    popupet.querySelector('#tc_edit_destination').value = '';
    popupet.querySelector('#tc_edit_status').value = '';
    popupet.querySelector('#tc_edit_planned_arrival_week').value = '';
    popupet.querySelector('#tc_edit_recipient').value = '';

    popupet.querySelector('#tc_edit_freight_cost').value = '';
    popupet.querySelector('#tc_edit_freight_currency').value = '';

    popupet.classList.remove('hidden');

    setPeriod();



}