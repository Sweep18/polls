$(document).ready(function () {

    var socket = new WebSocket("ws://" + window.location.host + "/vote/");
    socket.onmessage = function (e) {

        if (e.data.substring(0, 5) == 'reset') {
            window.location.replace(location.href.replace('/polls/second/', '/polls/reset/' + e.data.substring(5)));
        }

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
                window.location.reload();
            }
        }, 1000);
    }

    window.onload = function () {
        var minutes = $("#delta").val(),
            display = document.querySelector('#time');
        startTimer(minutes, display);
    };


});