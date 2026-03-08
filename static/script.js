function sendMessage() {
    let input = 
    document.getElementById("user-input").value;

    fetch("/chat", {
        method:"POST",
        headers:{
         "Content-Type":"application/json" 

        },
        body:JSON.stringify({message:input})
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("chat-box").innerHTML += "<p><b>You:</b> "+input+"</p>";
        document.getElementById("chat-box").innerHTML += "<p><b>Bot:</b> "+data.reply+"</p>";
        document.getElementById("user-input").value="";
    })
}