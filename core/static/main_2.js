// Emoji selection
window.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('chat-submit');
    const chatArea = document.getElementById('chat-area');
    const inputElm = document.getElementById('chat-input');
    const emojiBtn = document.getElementById('emoji-btn');
    const picker = new EmojiButton();
    const room_id = JSON.parse(document.getElementById('room_id').textContent);
    const session_id = JSON.parse(document.getElementById('session_id').textContent);

    picker.on('emoji', emoji => {
      document.getElementById('chat-input').value += emoji;
    });

    emojiBtn.addEventListener('click', () => {
      picker.togglePicker(emojiBtn);
    });

    // send msg
    submitBtn.addEventListener('click', ()=>{
        //  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrftoken = document.getElementById('chat_django_csrf_token').children[0].value;
        let userInput = inputElm.value;
        let temp = `<div class="out-msg">
        <span class="my-msg">${userInput}</span>
        <!--img src="{% static 'img/pic.png' %}" class="avatar"-->
        </div>`;

        chatArea.insertAdjacentHTML("beforeend", temp);

        console.log("submit button clicked", csrftoken)

        $.ajax({
                type: 'POST',
                url : `https://100096.pythonanywhere.com/send/`+ room_id + `/`,
                headers: {'X-CSRFToken': csrftoken},
                POST: {
                    'message': userInput,
                    'session_id': session_id
                },
                data: {
                    'message': userInput,
                    'session_id': session_id
                },

                success: function(response){
                    console.log(response);
                    /*$("#chat-area").empty();
                    for (var key in response.messages)
                    {
                        var temp2="<div class='container darker'><b>"+response.messages[key].user+"</b><p>"+response.messages[key].value+"</p><span class='time-left'>"+response.messages[key].date+"</span></div>";
                        $("#chat-area").append(temp);
                    }*/
                },
                error: function(response){
                    // alert('An error occurred')
                },
                headers: {'X-CSRFToken': csrftoken}
            });
        inputElm.value = '';

    })

  });





document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var instances = M.Dropdown.init(elems, {});
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems, {opacity: 0.6});

});

document.addEventListener('DOMContentLoaded', function() {
var elems = document.querySelectorAll('.tooltipped');
var instances = M.Tooltip.init(elems, {});
});