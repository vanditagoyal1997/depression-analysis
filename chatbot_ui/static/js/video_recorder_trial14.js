// This example uses MediaRecorder to record from an audio and video stream, and uses the
// resulting blob as a source for a video element.
//
// The relevant functions in use are:
//
// navigator.mediaDevices.getUserMedia -> to get the video & audio stream from user
// MediaRecorder (constructor) -> create MediaRecorder instance for a stream
// MediaRecorder.ondataavailable -> event to listen to when the recording is ready
// MediaRecorder.start -> start recording
// MediaRecorder.stop -> stop recording (this will generate a blob of data)
// URL.createObjectURL -> to create a URL from a blob, which we use as video src
URL = window.URL || window.webkitURL;

let recordbutton,stopbutton,recorder, stream, chunks;

recordbutton = document.getElementById('audio_start');
stopbutton = document.getElementById('audio_stop');
recordbutton.addEventListener('click', startrecording);
stopbutton.addEventListener('click', stoprecording);
  // get video & audio stream from user

navigator.mediaDevices.getUserMedia({
		audio: true,
		video: true
	})
  .then(stm => {
      stream = stm;
	  recorder = new MediaRecorder(stream,{mimeType: 'video/webm'});
	  recorder.ondataavailable = e => {
      chunks.push(e.data);
      if(recorder.state == 'inactive')  sendDataVideo();
    };

	}).catch(e => console.error(e));

function startrecording() {
	console.log("recording start");
	chunks=[]
	recorder.start();
}

function stoprecording() {

  // Stopping the recorder will eventually trigger the 'dataavailable' event and we can complete the recording process
  recorder.stop();
}
function sendDataVideo(){
	let blob = new Blob(chunks, {type: 'video/webm'})
	var d=new Date();
	d.setSeconds(0,0);
	console.log(d)
    var filename = d.toISOString();
	console.log(filename)
	filename=filename.replace(/:/g,"_")
    var fd=new FormData();
    fd.append("file",blob);
	fd.append('file_name',filename);
    console.log("pray that this works despite the security risk rn");
	fetch("/create_video", {
	method: "post",
	body: blob
	}).then(response => {
    if (response.ok) {
      document.location.href="/"
    } else {
      console.log("error--after data is stored")
    }
  });
;
}
function makeLink()
{
	let blob = new Blob(chunks, {type: 'video/webm'})
	var url = URL.createObjectURL(blob);
    var au = document.createElement('video');
    var li = document.createElement('li');
    var link = document.createElement('a');

    //name of .wav file to use during upload and download (without extendion)
	var d=new Date();
	d.setSeconds(0,0);
    var filename = d.toISOString();
    //var filename = new Date().toISOString();

    //add controls to the <audio> element
    au.controls = true;
    au.src = url;

    //save to disk link
    link.href = url;
    link.download = filename+".webm"; //download forces the browser to donwload the file using the  filename
    //link.innerHTML = "Save to disk";
	link.click()
	link.remove()
}

function onRecordingReady(e) {
  var video = document.getElementById('recording');
  // e.data contains a blob representing the recording
  video.src = URL.createObjectURL(e.data);
  video.play();
}

