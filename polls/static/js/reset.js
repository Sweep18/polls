$(document).ready(function () {

    var socket = new WebSocket("ws://" + window.location.host + "/vote/");

    socket.onopen = function () {

        socket.send('reset');
    };
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();

});