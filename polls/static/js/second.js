$(document).ready(function () {

    socket = new WebSocket("ws://" + window.location.host + "/user/");
    socket.onmessage = function (e) {
        $("#user").text(e.data)
    };
    socket.onopen = function () {
        socket.send($("#usr").val());
    };
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();


    function startTimer(duration, display) {
        var timer = duration, minutes, seconds;
        setInterval(function () {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            display.textContent = minutes + ":" + seconds;
            if (--timer < 0) {
                window.location.replace(location.href.replace('/first/', '/second/'));
            }
        }, 1000);
    }

    window.onload = function () {
        var minutes = $("#delta").val(),
            display = document.querySelector('#time');
        startTimer(minutes, display);
    };


});