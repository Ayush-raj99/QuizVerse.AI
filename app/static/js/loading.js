const messages = [

"🤖 Connecting to Gemini AI...",

"📖 Reading NCERT concepts...",

"🧠 Understanding important topics...",

"📝 Generating Board-level MCQs...",

"🎯 Checking answer quality...",

"✅ Finalizing your quiz..."

];

let progress = 0;

let message = 0;

const status = document.getElementById("status");

const bar = document.getElementById("progressBar");

const percent = document.getElementById("percent");

const timer = setInterval(()=>{

progress += 2;

bar.style.width = progress + "%";

percent.innerHTML = progress + "%";

if(progress%18===0 && message<messages.length){

status.innerHTML=messages[message];

message++;

}

if(progress>=100){

clearInterval(timer);

}

},100);