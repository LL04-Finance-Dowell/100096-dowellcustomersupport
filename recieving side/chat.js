
let msg_list=document.getElementById('chat-message-list')
document.addEventListener('keypress', logKey);

function createYouDiv() {

    let text=document.createElement('div')
    text.innerHTML=document.getElementById('chat-box').value
    text.setAttribute('class','message-text')

    let time=document.createElement('div')
    time.innerHTML='Aug 30'
    time.setAttribute('class','message-time')

    let container=document.createElement('div')
    container.setAttribute('class','message-content')
    container.appendChild(text);
    container.appendChild(time);

    let containerx=document.createElement('div')
    containerx.setAttribute('class','message-row you-message')
    containerx.appendChild(container);
    document.getElementById("chat-message-list").appendChild(containerx);

}  

function createOtherDiv() {

    let text=document.createElement('div')
    text.innerHTML=document.getElementById('chat-box').value
    text.setAttribute('class','message-text')

    let time=document.createElement('div')
    time.innerHTML='Aug 30'
    time.setAttribute('class','message-time')

    let container=document.createElement('div')
    container.setAttribute('class','message-content')
    container.appendChild(text);
    container.appendChild(time);

    let containerx=document.createElement('div')
    containerx.setAttribute('class','message-row other-message')
    containerx.appendChild(container);
    document.getElementById("chat-message-list").appendChild(containerx);

}  

let cnt=1
function logKey(e) {
    if (e.which==13) {
        if (cnt%2==0) {
            createOtherDiv()
        } else {
            createYouDiv()
        }
        cnt++
     }
   else{
       let randomName = faker.name.findName()
       console.log(randomName);
   }
  }

