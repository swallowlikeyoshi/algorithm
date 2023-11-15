var sc
$(document).ready(function(){

    sc = io.connect('http://' + document.domain + ':' + location.port + '/chatting');
    
    sc.on('connect', function(){
        sc.emit('joined', {});
    });

    sc.on('status', function(data){
        if (data.contents == true) {
            newMessage = '<' + data.name + '> 입장'
            $('#chatBox').val($('#chatBox').val() + newMessage + '\n');
        }
        else {
            newMessage = '<' + data.name + '> 퇴장'
            $('#chatBox').val($('#chatBox').val() + newMessage + '\n');
        }
        $('#chatBox').scrollTop($('#chatBox')[0].scrollHeight);
    });

    sc.on('message', function(data){
        $('#chatBox').val($('#chatBox').val() + '<' + data.name + '>: ' + data.contents + '\n');
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