var io = require('socket.io').listen(8001)
  , amqp = require('amqp')
  ;

io.set('log level', 1)

var connection = amqp.createConnection()

connection.on('ready', function(){

    connection.queue("", {"autoDelete": true}, function(queue){

        queue.bind("amq.headers", "");
        queue.subscribe(function(message, headers, deliveryInfo){
            console.log(message.data.toString());
        });
    });

    io.sockets.on('connection', function(socket) {


        console.log("Connected");
        console.log(socket);
        connection.queue("", {"autoDelete": true}, function(queue){

            queue.bind("amq.headers", "");
            queue.subscribe(function(message, headers, deliveryInfo){
                socket.emit("event", message.data.toString());
            });
        });
    });
});

