var io = require('socket.io').listen(8001)
  , amqp = require('amqp')
  ;

io.set('log level', 1)

var connection = amqp.createConnection()

connection.on('ready', function(){

    connection.queue("", {"autoDelete": true}, function(queue){

        queue.bind("amq.topic", "");
        queue.subscribe(function(message, headers, deliveryInfo){
            console.log(message.data.toString());
        });
    });

    io.sockets.on('connection', function(socket) {

        console.log("Client connected.");
        connection.queue("", {"autoDelete": true}, function(queue){

            queue.bind("amq.topic", "event.*");
            queue.subscribe(function(message, headers, deliveryInfo){
                console.log(deliveryInfo.routingKey);
                socket.emit(deliveryInfo.routingKey, message.data.toString());
            });

            socket.on('disconnect', function(){
                console.log("Client disconnected.");
                queue.destroy();
            });
        });
    });
});

