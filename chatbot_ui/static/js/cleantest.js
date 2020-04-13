/**
 * 
 */
var bot_msgs=["Hi! I am voicebot. Tap the microphone and start talking to me.",   //   0
	"How Can I help You?",                                              //   1
	"Can you provide me your Loan ID?",                                 //   2
	" What's your Mobile number ",                                          //   3
	"Can you provide me your Date Of Birth ?",              //   4
	"Sorry, I couldn't understand you. Could you please repeat?",       //   5
	"Sorry, No matching record found.",                                 //   6
	"Sorry, please try again.",                                         //   7
	"We are already in the process!",               //   8
	"what's your name? ",                                 //   9
	" Please Check the details provided by you and confirm with Yes or No?",      //   10
	" Can you tell me what do you want to inquire about? " ,                  //11
	" I cannot answer this. However, I can help you with ",                   //12
	" Loan termination, your next due date, next due installment amount, number of installments unpaid, amount over due"   //13              
	];              

var msg_latest=bot_msgs[0];


var LID;
var name;
var url_sent="";
var marker=true;  /////////////   Marker for Validation
var opcode="NA";       /////////////   Variable indicating which operation is going on
var oper_stat="failure";
var flag_suggest=0;
var suggest_spoken="";
var flag_nospeech=0;


var recognition = new webkitSpeechRecognition();
recognition.lang="en-IN";
recognition.continuous = false;



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


function speakNlisten(msg_disp,msg_speak)
{
	//addBotItem(msg_disp);
	var msg=new SpeechSynthesisUtterance(msg_speak);
	window.speechSynthesis.speak(msg);
	msg.onend= function(event) {
	//    console.log('Utterance has finished being spoken after ' + event.elapsedTime + ' milliseconds.');
		startListen();
	  }
//	handleMic(msg,timer);

}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function startListen() {
	gotoListeningState();
	recognition.start();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function setVal()
{
	speakNlisten(bot_msgs[2],bot_msgs[2]);
	msg_latest=bot_msgs[2];

}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function AxiaCall()
{
//	var jsonstring = {"text": recognizedText ,"opcode": opcode};
	var jsonstring = {"text": recognizedText };

	$.ajax({

		url: 'SpeechInput_text',
		type: "POST",
		contentType: "application/json; charset=utf-8",
		data:JSON.stringify(jsonstring),
		dataType : "json",

		async: false,    //Cross-domain requests and dataType: "jsonp" requests do not support synchronous operation
		cache: false,    //This will force requested pages not to be cached by the browser          
		processData:false,

		success: function (cdata) {
			
			console.log(cdata);
			if(cdata.opcode!=="NA" && cdata.opcode!=="NA-RC")
				{
				speakNlisten(cdata.text,cdata.speech);
				}
			else
				{
				addBotItem(cdata.text);
				var msg=new SpeechSynthesisUtterance(cdata.speech);
				window.speechSynthesis.speak(msg);
				}
			
			opcode=cdata.opcode;
			
		},
		error: function (erdat) {

			alert("Error!");
			alert(JSON.stringify(erdat));            
		}
	});
}




/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function validation(data,input_type,operation)
{
	var jsonstring = {"operation": operation ,"input_type": input_type ,"data": data};


	$.ajax({

		url: 'request_validation',
		type: "POST",
		contentType: "application/json; charset=utf-8",
		data:JSON.stringify(jsonstring),
		dataType : "json",

		async: false,    //Cross-domain requests and dataType: "jsonp" requests do not support synchronous operation
		cache: false,    //This will force requested pages not to be cached by the browser          
		processData:false,

		success: function (cdata) {
			if(!(cdata.validation))
			{
				console.log("inside validation")
//				var timer = window.setTimeout(function() { startListen(); }, 5000);
				var msg_incorrect="";
				if(input_type==="name")
					{
					msg_incorrect="This name is Invalid. ";
					msg_incorrect+=msg_latest;
					}
				else if(input_type==="loanId")
					{
					msg_incorrect="The loan ID does not exist . How can I help you?";
					msg_latest=bot_msgs[1];
					oper_stat="failure";
					oper=10;
					}
				
				speakNlisten(msg_incorrect,msg_incorrect);
				marker=false;
			}
			else
			{
				marker=true;
			}
		},
		error: function (erdat) {

			alert("Error!");
			alert(JSON.stringify(erdat));            
		}
	});
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function isChrome() {
	var isChromium = window.chrome,
	winNav = window.navigator,
	vendorName = winNav.vendor,
	isOpera = winNav.userAgent.indexOf("OPR") > -1,
	isIEedge = winNav.userAgent.indexOf("Edge") > -1,
	isIOSChrome = winNav.userAgent.match("CriOS");

	if(isIOSChrome){
		return true;
	} else if(isChromium !== null && isChromium !== undefined && vendorName === "Google Inc." && isOpera == false && isIEedge == false) {
		return true;
	} else {
		return false;
	}
}

function gotoListeningState() {
	const micListening = document.querySelector(".mic .listening");
	const micReady = document.querySelector(".mic .ready");

	micListening.style.display = "block";
	micReady.style.display = "none";
}

function gotoReadyState() {
	const micListening = document.querySelector(".mic .listening");
	const micReady = document.querySelector(".mic .ready");

	micListening.style.display = "none";
	micReady.style.display = "block";
}

function addBotItem(text) {
	/* const appContent = document.querySelector(".app-content");
	appContent.innerHTML += '<div class="item-container item-container-bot"><img src="resources/i/bot1.jpg" height="40" width="40"><div class="item"><p>' +  text + '</p></div></div>';
	appContent.scrollTop = appContent.scrollHeight; */ // scroll to bottom
}

function addUserItem(text) {
	/* const appContent = document.querySelector(".app-content");
	appContent.innerHTML += '<div class="item-container item-container-user"><img src="resources/i/user.png" height="40" width="40"><div class="item"><p>' + text + '</p></div></div>';
	appContent.scrollTop = appContent.scrollHeight;  */// scroll to bottom
}

function displayCurrentTime() {
	const timeContent = document.querySelector(".time-indicator-content");
	const d = new Date();
	const s = d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
	/* timeContent.innerHTML = s; */
}

function addError(text) {
	//alert(text);
	const footer = document.querySelector(".app-footer");
	footer.style.display = "none";
}



document.addEventListener("DOMContentLoaded", function(event) {

	// test for relevant API-s
	// for (let api of ['speechSynthesis', 'webkitSpeechSynthesis', 'speechRecognition', 'webkitSpeechRecognition']) {
	//   console.log('api ' + api + " and if browser has it: " + (api in window));
	// }

	displayCurrentTime();

	// check for Chrome
	/*if (!isChrome()) {
		addError("This demo only works in Google Chrome.");
		return;
	}
*/
	if (!('speechSynthesis' in window)) {
		addError("Your browser doesn’t support speech synthesis. This demo won’t work.");
		return;
	}

	if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
		addError("Your browser cannot record voice. This demo won’t work.");
		return;
	}

	// Now we’ve established that the browser is Chrome with proper speech API-s.




	// Initial feedback message.


	//addBotItem("Hi! I am voicebot. Tap the microphone and start talking to me.");
	//alert(msg_latest);

	//speakNlisten(bot_msgs[1], bot_msgs[1], timer, recognition)
	//alert(bot_msgs[1]);
		  msg_latest=bot_msgs[1];
		  var msg = new SpeechSynthesisUtterance(bot_msgs[1]);
		    window.speechSynthesis.speak(msg);
	 
	
	
	recognition.onstart = function() {
		recognizedText = null;
	};
	recognition.onresult = function(ev) {
		console.log(msg_latest);
		recognizedText = ev["results"][0][0]["transcript"];
		console.log(" onresult ",recognizedText);

		addUserItem(recognizedText);
		//AxiaCall();
		$('#msg-insert').append('<div class="row msg_container base_sent">'+
                        '<div class="col-md-10 col-xs-10 ">'+
                            '<div class="messages msg_sent">'+
                               ' <p style="display: inline-block;">'+recognizedText+'</p>'+
                           '     <time datetime="2009-11-13T20:00">Timothy • 51 min</time>'+
                           ' </div>'+
                       ' </div>'+
                      '  <div class="col-md-2 col-xs-2 avatar">'+
                        '    <img src="http://www.bitrebels.com/wp-content/uploads/2011/02/Original-Facebook-Geek-Profile-Avatar-1.jpg" class=" img-responsive ">'+
                     '   </div>'+
                  '  </div>');
		ajaxcall(recognizedText)
		/******************************    TEST CASES   *******************************************/    


		
		
		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		////////////////////////////////////////////////////////////////////////////////////////////////////////////    

	};

	recognition.onerror = function(ev) {
		console.log("Speech recognition error", ev);
		//var timer = window.setTimeout(function() { startListen(); }, 5000);
		if(ev.error==="no-speech")
			{
			if(flag_nospeech==0)
				{
				flag_nospeech=1;
				speakNlisten("Hello? are you there ?","Hello? are you there ? ");
				}
			else
				{
				//speakNlisten(,);
				//alert("Guess you're busy. See ya later!");
				var msg=new SpeechSynthesisUtterance("Guess you're busy. See ya later!");
				window.speechSynthesis.speak(msg);
				
				}
			
			}
	
		
	};
	recognition.onend = function() {
		gotoReadyState();
	};

	function startListening() {
	    gotoListeningState();
	    recognition.start();
	  }
	// Mic Click Action Function
	const startButton = document.querySelector("#audio");
	startButton.addEventListener("click", function(ev) {
		startListening();
		ev.preventDefault();
	});

	// Esc key handler - cancel listening if pressed
	// http://stackoverflow.com/questions/3369593/how-to-detect-escape-key-press-with-javascript-or-jquery
	document.addEventListener("keydown", function(evt) {
		evt = evt || window.event;
		var isEscape = false;
		if ("key" in evt) {
			isEscape = (evt.key == "Escape" || evt.key == "Esc");
		} else {
			isEscape = (evt.keyCode == 27);
		}
		if (isEscape) {
			recognition.abort();
		}
	});


});
