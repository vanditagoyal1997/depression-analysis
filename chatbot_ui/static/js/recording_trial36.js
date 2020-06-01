URL = window.URL || window.webkitURL;

var gumStream;                      //stream from getUserMedia()
var rec;                            //Recorder.js object
var input;                          //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("audio_start");
var stopButton = document.getElementById("audio_stop");
var resultsPrediction=document.getElementById("results_prediction")
//var pauseButton = document.getElementById("pauseButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
//pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    console.log("recordButton clicked");

    /*
        Simple constraints object, for more advanced audio features see
        https://addpipe.com/blog/audio-constraints-getusermedia/
    */

    var constraints = { audio: true, video:false }

    /*
        Disable the record button until we get a success or fail from getUserMedia() 
    */

    recordButton.disabled = true;
    stopButton.disabled = false;
    //pauseButton.disabled = false

    /*
        We're using the standard promise based getUserMedia() 
        https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
    */

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        /*
            create an audio context after getUserMedia is called
            sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
            the sampleRate defaults to the one set in your OS for your playback device

        */
        audioContext = new AudioContext();

        //update the format 
       // document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

        /*  assign to gumStream for later use  */
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        /* 
            Create the Recorder object and configure to record mono sound (1 channel)
            Recording 2 channels  will double the file size
        */
        rec = new Recorder(input,{numChannels:1})

        //start the recording process
        rec.record()

        console.log("Recording started");

    }).catch(function(err) {
		console.log(err);
        //enable the record button if getUserMedia() fails
        //recordButton.disabled = false;
        //stopButton.disabled = true;

    });
}

/*function pauseRecording(){
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording){
        //pause
        rec.stop();
        pauseButton.innerHTML="Resume";
    }else{
        //resume
        rec.record()
        pauseButton.innerHTML="Pause";

    }
}*/

function stopRecording() {
    console.log("stopButton clicked");

    //disable the stop button, enable the record too allow for new recordings
    stopButton.disabled = true;
   // recordButton.disabled = false;
    //pauseButton.disabled = true;

    //reset button just in case the recording is stopped while paused
    //pauseButton.innerHTML="Pause";

    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(sendDataAudio);
}
function sendDataAudio(blob){
	//var d=new Date();
	//d.setSeconds(0,0);
	//console.log(d)
    //var filename = d.toISOString();
	//console.log(filename)
	//filename=filename.replace(/:/g,"_")
    //var fd=new FormData();
    //fd.append("file",blob);
	//fd.append('file_name',filename);
    console.log("pray that this works despite the security risk rn");
	fetch("/create_audio", {
	method: "post",
	body: blob
	});


	/*$.ajax({
	  type: 'POST',
      url: '/create_audio',
      data: fd,
      processData: false,
      contentType: false,
      success: function(result) {
				console.log(result);
		},
			error: function(result) {
				console.log('error from create_audio');
			}
	  
    });*/

}
function sendData(blob){
	//trying xmlhttpreq
	var d=new Date();
	d.setSeconds(0,0);
	console.log(d)
    var filename = d.toISOString();
	console.log(filename)
	filename=filename.replace(/:/g,"_")
	var reader = new window.FileReader();
  reader.readAsDataURL(blob);
  reader.onloadend = function() {
	console.log("creating formdata")
    var fd = new FormData();
    base64data = reader.result;
    fd.append('file', base64data);
	fd.append('file_name',filename);
	console.log("sendingform_data")
    $.ajax({
      type: 'POST',
      url: '/convert',
      data: fd,
      cache: false,
      processData: false,
      contentType: false,
      enctype: 'multipart/form-data'
    }).done(function(data) {
      console.log(data);
    });
  }
	console.log("praying that it works")

}


function createDownloadLink(blob) {

   // var url = URL.createObjectURL(blob);
	console.log("in downloadlink_audio");
	var fileReader = new FileReader();
	var file=blob;
	console.log("file=url of blob");
	fileReader.readAsDataURL(file);
	console.log("readAsDataURL");
    fileReader.onloadend = function(){
		var arrayBuffer = fileReader.result; 
		console.log("arraybuffer has the string");
    //var au = document.createElement('audio');
    //var li = document.createElement('li');
    //var link = document.createElement('a');

    //name of .wav file to use during upload and download (without extendion)
	var d=new Date();
	d.setSeconds(0,0);
	console.log(d)
    var filename = d.toISOString();
	console.log(filename)
	
	//filename="audio_inter"

    //add controls to the <audio> element
    //au.controls = true;
    //au.src = url;

    //save to disk link
    /* link.href = url;
    link.download = filename+".wav"; //download forces the browser to donwload the file using the  filename
    //link.innerHTML = "Save to disk";
	link.click()
	link.remove() */
	filename=filename.replace(/:/g,"_")
    //add the new audio element to li
    //li.appendChild(au);

    //add the filename to the li
    //li.appendChild(document.createTextNode(filename+".wav "))

    //add the save to disk link to li
    //li.appendChild(link);
	//recordingsList.appendChild(li);

	
	var postData = {
						  "sender" : "123",
						  "file":arrayBuffer,
						  "filename" : filename
					};
	console.log("finished creating postData");
	$.ajax({
			type: 'POST',
			url: '/convert',
			data: JSON.stringify (postData),
			contentType: "application/json",
			dataType: 'json',
			success: function(result) {
				console.log(result);
				var row = document.createElement('tr');
				var cell1 = document.createElement('td');
				var cell2 = document.createElement('td');
				cell1.append(result.type);
				cell2.append(result.pred);
				//row.append($('<td>').html(result.type,result.pred));
				row.append(cell1)
				row.append(cell2)
				resultsPrediction.append(row)
			},
			error: function(result) {
				console.log('error from convert');
			}
	});
	}
 
}