var io = require('socket.io').listen(8001)
  , amqp = require('amqp')
  ;

io.set('log level', 1)

var connection = amqp.createConnection()

connection.on('ready', function(){

    connection.queue("", {"autoDelete": true}, function(queue){

        queue.bind_headers("amq.headers", {
            "x-match": "all",
            "ns": "auditor"
        });
        queue.subscribe(function(message, headers, deliveryInfo){
            console.log("Headers: ", headers);
            console.log(message.data.toString());
        });
    });

    io.sockets.on('connection', function(socket) {

        console.log("Client connected.");
        connection.queue("", {"autoDelete": true}, function(queue){

            queue.bind_headers("amq.headers", {
                "x-match": "all",
                "ns": "auditor",
                "type": "event"
            });

            queue.subscribe(function(message, headers, deliveryInfo){
                socket.emit(headers.ns + "." + headers.type + "." + headers.cmd, message.data.toString());
            });

            socket.on('disconnect', function(){
                console.log("Client disconnected.");
                queue.destroy();
            });
        });
    });
});

