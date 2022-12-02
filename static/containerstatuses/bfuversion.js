
var ownername = ''
var ownerid = ''
var fileid = ''

//*********************/
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
    req.setRequestHeader('ownerid', ownerid);
    req.setRequestHeader('ownername', encodeURIComponent(ownername));
    req.setRequestHeader('fileid', fileid);

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

function sendNext() {

    if (numFile < files.length) {

        var curFile = files[numFile];

        if (startingByte == 0) {

            if(numFile > 0){
                
                sendMessageToContainerFilesInfoBot(files[numFile-1].name);

            }

            uuid = newUid();

        }

        endindByte = startingByte + upload_chunk_size;
        if (endindByte > curFile.size) {
            endindByte = curFile.size;
        }

        sendPartOfFile();


    } else {

        sendMessageToContainerFilesInfoBot(files[numFile-1].name);

        location.reload();

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

    ownername = e.srcElement.getAttribute('ownername');
    ownerid = e.srcElement.getAttribute('ownerid');
    fileid = e.srcElement.getAttribute('fileid');
    
    big_file_upload_files(e.srcElement.files);

}




function onFileClick(fileid, in_t, ext) {

    full_name = document.querySelector('#name_ext').getAttribute('name_ext');

    if(in_t == 'True'){

        locationhref = '?fatt=' + fileid + '&ext=' + ext + '&full_name=' + full_name;

    } else {

        locationhref = '../attachedfile?type=ref&name=' + document.querySelector('#inputFile').getAttribute('ownername') + 'ПрисоединенныеФайлы&id=' + fileid + '&ext=' + ext + '&full_name=' + full_name;
    }

    window.open(locationhref);



}

function sendMessageToContainerFilesInfoBot(container_file_name) {
    
    container_text = document.querySelector('#inputFile').getAttribute('container_text')
        + ", файл " + document.querySelector('#name_ext').getAttribute('name_ext')
        + ": присоединена версия " + container_file_name;

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
