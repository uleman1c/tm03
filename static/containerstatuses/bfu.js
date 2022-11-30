
var type1c = ''
var name1c = ''
var id1c = ''
var transcontainer = ''
var container = ''

var is_transcontainer = false

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

    document.querySelector(idEl).innerHTML = curFile.name + " " + Math.floor(startingByte * 100 / curFile.size) + "%, ошибок " + errorCount;

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
    req.setRequestHeader('type1c', type1c);
    req.setRequestHeader('name1c', encodeURIComponent(name1c));
    req.setRequestHeader('id1c', id1c);
    req.setRequestHeader('id', uuid);
    req.setRequestHeader('filename', encodeURIComponent(curFile.name));
    req.setRequestHeader('part', numPart);
    req.setRequestHeader('size', endindByte - startingByte);

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

function addFileToTable(curUuid){

    var req = new XMLHttpRequest();

    var url = "?f=" + curUuid;
    req.open("GET", url, false);

    req.onreadystatechange = function () { // (3)

        if (this.readyState != 4) return;

        // button.innerHTML = 'Готово!';

        if (this.status != 200) {

            //setTimeout(onError, 1000);
            // alert(this.status + ': ' + this.statusText);

        } else {

            //onLoad();

        }

    }

    req.send();

    if(is_transcontainer){

        ctj.forEach(element => {
        
            if(element.ТранспортныйКонтейнер == id1c){

                JSON.parse(req.responseText)['files'].forEach(felement => {

                    comments = '';
                    if(felement.comments){
                        comments = felement.comments;
                    }

                    element.Файлы.push({'ИдентификаторКонтейнера': element.ТранспортныйКонтейнер, 'ИдентификаторФайла': felement.id, 'Автор': felement.user,
                    'ДатаСоздания': felement.created, 'Имя': felement.name, 'Описание': comments, 'Расширение':felement.ext, 'in_t':true,
                    'Картинка': picByExt(felement.ext)});
                });
            }
        });

        onTransportContainerClick(id1c)

    } else {

        ctj.forEach(element => {
        
            if(element.ТранспортныйКонтейнер == transcontainer){

                JSON.parse(req.responseText)['files'].forEach(felement => {

                    comments = '';
                    if(felement.comments){
                        comments = felement.comments;
                    }

                    element.Файлы.push({'ИдентификаторКонтейнера': container, 'ИдентификаторФайла': felement.id, 'Автор': felement.user,
                    'ДатаСоздания': felement.created, 'Имя': felement.name, 'Описание': comments, 'Расширение':felement.ext, 'in_t':true,
                    'Картинка': picByExt(felement.ext)});
                });
            }
        });

        onContainerClick(transcontainer, container);

    }



}

function sendNext() {

    if (numFile < files.length) {

        var curFile = files[numFile];

        if (startingByte == 0) {

            if(numFile > 0){
                addFileToTable(uuid);
            }

            uuid = newUid();

        }

        endindByte = startingByte + upload_chunk_size;
        if (endindByte > curFile.size) {
            endindByte = curFile.size;
        }

        sendPartOfFile();


    } else {

        addFileToTable(uuid);

        document.querySelector(idEl).innerHTML = '';

        //location.reload();

    }

}

function newUid() {
    let u = Date.now().toString(16) + Math.random().toString(16) + '0'.repeat(16);
    return [u.substr(0, 8), u.substr(8, 4), '4000-8' + u.substr(13, 3), u.substr(16, 12)].join('-');
}

function big_file_upload(f){
	
	upload_chunk_size = 120000;
	
	files = f[0].files;

    numFile = 0;

    startingByte = 0;

    sendNext();

}

function big_file_upload_files(f){
	
	upload_chunk_size = 120000;
	
	files = f;

    numFile = 0;

    startingByte = 0;

    sendNext();

}

function onSelectFile(e){

    type1c = e.srcElement.getAttribute('type1c')
    name1c = e.srcElement.getAttribute('name1c')
    id1c = e.srcElement.getAttribute('id1c')
    is_transcontainer = e.srcElement.getAttribute('is_transcontainer') == 'true'
    container = e.srcElement.getAttribute('container')
    transcontainer = e.srcElement.getAttribute('transcontainer')
    
    big_file_upload_files(e.srcElement.files);

}
