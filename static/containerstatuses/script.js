var ctj = '';

document.addEventListener("DOMContentLoaded", function(){

    ctj = JSON.parse(container_statuses_h.replaceAll('&quot;', '"'));

    ctj.forEach(element => {
        
        var responseText = requestGet("?ftc=" + element.ТранспортныйКонтейнер);
    
        JSON.parse(responseText)['files'].forEach(felement => {

            comments = '';
            if(felement.comments){
                comments = felement.comments;
            }

            element.Файлы.push({'ИдентификаторКонтейнера': element.ТранспортныйКонтейнер, 'ИдентификаторФайла': felement.id, 'Автор': felement.user,
            'ДатаСоздания': felement.created, 'Имя': felement.name, 'Описание': comments, 'Расширение':felement.ext, 'in_t':true,
            'Картинка': picByExt(felement.ext)});

            document.querySelector('#pic_' + element.ТранспортныйКонтейнер).innerHTML = '<img src="/static/attach.svg" alt="" style="width: 1em;">';
        });

        element.Контейнеры.forEach(celement => {
            
            var responseText = requestGet("?fc=" + celement.ИдентификаторКонтейнера);
        
            JSON.parse(responseText)['files'].forEach(felement => {

                celement.ЕстьФайлы = true;

                comments = '';
                if(felement.comments){
                    comments = felement.comments;
                }

                element.Файлы.push({'ИдентификаторКонтейнера': celement.ИдентификаторКонтейнера, 'ИдентификаторФайла': felement.id, 'Автор': felement.user,
                'ДатаСоздания': felement.created, 'Имя': felement.name, 'Описание': comments, 'Расширение':felement.ext, 'in_t':true,
                'Картинка': picByExt(felement.ext)});

                //document.querySelector('#pic_' + celement.ИдентификаторКонтейнера).innerHTML = '<img src="/static/attach.svg" alt="" style="width: 1em;">';
            });

        });

    });

});

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

function onTransportContainerClick(transportcontainer){

    selected = document.querySelector('#container_statuses .selected');
    if(selected)
        selected.classList.remove('selected');

    document.querySelector('#container_statuses [transportcontainer="' + transportcontainer + '"]').classList.add('selected')

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

            document.querySelector('#add_file').style = 'display: block';

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
                    + '<div id="container_row" class="themed-grid-row  curpoint" onclick="onFileClick(\'' + сelement.ИдентификаторФайла +'\', \'' + сelement.Расширение + '\', ' + сelement.in_t + ')" container="' + сelement.ИдентификаторКонтейнера + '">'
                    +'    <div class="themed-grid-col-row w50" >' + (сelement.Картинка ? '<img src="' + сelement.Картинка + '" alt="" style="width: 1em;">' : '' ) + сelement.Имя + '.' + сelement.Расширение + '</div>'
                    +'    <div class="themed-grid-col-row w10 tacntr" >' + сelement.Автор + '</div>'
                    +'    <div class="themed-grid-col-row w10 tacntr" >' + сelement.ДатаСоздания + '</div>'
                        +'<div class="themed-grid-col-row w30 tacntr" >' + сelement.Описание + '</div>'
                    +'</div>';

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
        

                }
            });

            element.Файлы.forEach(сelement => {
                
                if(сelement.ИдентификаторКонтейнера == container){

                    document.querySelector('#zip_file').style = 'display: block';

                    files_table.innerHTML = files_table.innerHTML 
                    + '<div id="container_row" class="themed-grid-row  curpoint" onclick="onFileClick(\'' + сelement.ИдентификаторФайла +'\', \'' + сelement.Расширение + '\', ' + сelement.in_t + ')" container="' + сelement.ИдентификаторКонтейнера + '">'
                    +'    <div class="themed-grid-col-row w50" >' + '<img src="' + сelement.Картинка + '" alt="" style="width: 1em;">' + сelement.Имя + '.' + сelement.Расширение + '</div>'
                    +'    <div class="themed-grid-col-row w10 tacntr" >' + сelement.Автор + '</div>'
                    +'    <div class="themed-grid-col-row w10 tacntr" >' + сelement.ДатаСоздания + '</div>'
                        +'<div class="themed-grid-col-row w30 tacntr" >' + сelement.Описание + '</div>'
                    +'</div>';

                }

            });

        };

    });


}

function onFileClick(fileid, ext, in_t) {

    if(in_t){

        locationhref = '?fatt=' + fileid + "&ext=" + ext;

    } else {

        locationhref = '../attachedfile?type=ref&name=КонтейнерПрисоединенныеФайлы&id=' + fileid + "&ext=" + ext;
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