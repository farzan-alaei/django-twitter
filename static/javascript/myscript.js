document.addEventListener("DOMContentLoaded", function() {
    
    
    buttonclicked = document.getElementById('chat-open');

    user_chat = document.getElementById('user-chat');
    console.log(buttonclicked)
    console.log(user_chat)

    buttonclicked.addEventListener("click", function() {
        // Remove the class from the div
        user_chat.classList.remove("hidden");
    });

});