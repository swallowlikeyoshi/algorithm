var sc
$(document).ready(function(){

    sc = io.connect('http://' + document.domain + ':' + location.port + '/chatting');
    
    sc.on('connect', function(){
        sc.emit('joined', {});
    });

    sc.on('status', function(data){
        $('#chatBox').val($('#chatBox').val() + data.sent_message + '\n');
        $('#chatBox').scrollTop($('#chatBox')[0].scrollHeight);
    });

    sc.on('message', function(data){
        $('#chatBox').val($('#chatBox').val() + '<' + data.session_name + '>: ' + data.sent_message + '\n');
        $('#chatBox').scrollTop($('#chatBox')[0].scrollHeight);
    });

    $('#userInput').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#userInput').val();
            $('#userInput').val('');
            sc.emit('text', { 'message': text });
        }
    });
});

function leave_room() {
    sc.emit('left', {}, function(){
        sc.disconnect();
        window.location.href = "/";
    });
}