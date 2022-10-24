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
