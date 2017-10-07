$(document).ready(function () {

    $(function () {
        $("#id_event").autocomplete({
            source: "/get_event/",
            select: function (event, ui) {
                AutoCompleteSelectHandler(event, ui)
            },
            minLength: 2
        });
    });

    function AutoCompleteSelectHandler(event, ui) {
        var selectedObj = ui.item;
    }

    socket = new WebSocket("ws://" + window.location.host + "/vote/");
    socket.onmessage = function (e) {
        $("#votes").text(e.data)
    };
    socket.onopen = function () {
        socket.send($("#vot").val());
    };
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();

});