function onTransportContainerClick(transportcontainer){

    selected = document.querySelector('#container_statuses .selected');
    if(selected)
        selected.classList.remove('selected');

    document.querySelector('#container_statuses [transportcontainer="' + transportcontainer + '"]').classList.add('selected')

    containers_table = document.querySelector('#containers_table');
    containers_table.innerHTML = '';

    files_table = document.querySelector('#files_table');
    files_table.innerHTML = '';

    ctj = JSON.parse(container_statuses_h.replaceAll('&quot;', '"'));

    ctj.forEach(element => {
        
        if(element.ТранспортныйКонтейнер == transportcontainer){

            element.Контейнеры.forEach(сelement => {
                
                containers_table.innerHTML = containers_table.innerHTML + '<div id="container_row" class="themed-grid-row curpoint" onclick="onContainerClick(\'' + transportcontainer + '\', \'' + сelement.ИдентификаторКонтейнера +'\')" container="' + сelement.ИдентификаторКонтейнера + '">'
                +'    <div class="themed-grid-col-row w5 tacntr" >' + (сelement.ЕстьФайлы ? '<img src="/static/attach.svg" alt="" style="width: 50%;">' : '') + '</div>'
                +'    <div class="themed-grid-col-row w45 tacntr" >' + сelement.КраткоеНаименованиеГруза + '</div>'
                    +'<div class="themed-grid-col-row w50 tacntr" >' + сelement.Комментарий + '</div>'
                +'</div>';

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

    ctj = JSON.parse(container_statuses_h.replaceAll('&quot;', '"'));

    ctj.forEach(element => {
        
        if(element.ТранспортныйКонтейнер == transportcontainer){

            element.Файлы.forEach(сelement => {
                
                if(сelement.ИдентификаторКонтейнера == container){

                    files_table.innerHTML = files_table.innerHTML 
                    + '<div id="container_row" class="themed-grid-row  curpoint" onclick="onFileClick(\'' + сelement.ИдентификаторФайла +'\', \'' + сelement.Расширение + '\')" container="' + сelement.ИдентификаторКонтейнера + '">'
                    +'    <div class="themed-grid-col-row w50" >' + сelement.Имя + '.' + сelement.Расширение + '</div>'
                    +'    <div class="themed-grid-col-row w10 tacntr" >' + сelement.Автор + '</div>'
                    +'    <div class="themed-grid-col-row w10 tacntr" >' + сelement.ДатаСоздания + '</div>'
                        +'<div class="themed-grid-col-row w30 tacntr" >' + сelement.Описание + '</div>'
                    +'</div>';

                }

            });

        };

    });


}

function onFileClick(fileid, ext) {

    location.href = '../attachedfile?type=ref&name=КонтейнерПрисоединенныеФайлы&id=' + fileid + "&ext=" + ext;

}

