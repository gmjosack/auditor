var io = require('socket.io').listen(8001)
  , amqp = require('amqp')
  , extend = require('extend')
  ;

io.set('log level', 1)

var connection = amqp.createConnection()


function subscribe(extra_headers, callback, socket){
    extra_headers = typeof extra_headers !== 'undefined' ? extra_headers : {};
    callback = typeof callback !== 'undefined' ? callback : function(message, headers, deliveryInfo){
            console.log("Headers: ", headers);
            console.log("Message: ", message.data.toString());
    };
    socket = typeof socket !== 'undefined' ? socket : null;

    var headers = {
        "x-match": "all",
        "ns": "auditor"
    };

    extend(headers, extra_headers);

    connection.queue("", {"autoDelete": true}, function(queue){
        queue.bind_headers("amq.headers", headers);
        queue.subscribe(callback);
    });

    if (socket){
        socket.on('disconnect', function(){
            console.log("Client disconnected.");
            queue.destroy();
        });
    }
}


connection.on('ready', function(){

    console.log("Subscribing to all events.")
    subscribe()

    io.sockets.on('connection', function(socket) {

        console.log("Client connected.");

        socket.on('subscribe', function(data){
            console.log("Client subscription: ", data)
            subscribe(data, function(message, headers, deliveryInfo){
                socket.emit(headers.ns + "." + headers.type + "." + headers.cmd, message.data.toString());
            });
        });
    });
});

