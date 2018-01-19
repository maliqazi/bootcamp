// Import express and path modules.
var express = require( "express");
var path = require( "path");
// Create the express app.
var app = express();
// Define the static folder.
app.use(express.static(path.join(__dirname, "./static")));
// Setup ejs templating and define the views folder.
app.set('views', path.join(__dirname, './views'));
app.set('view engine', 'ejs');
// Root route to render the index.ejs view.
app.get('/', function(req, res) {
 res.render("index");
})

var math = require('mathjs');

var server = app.listen(8000, function() {
 console.log("listening on port 8000");
});
var io = require('socket.io').listen(server);

var users=[]

io.sockets.on('connection', function (socket) {
  console.log("Client/socket is connected!");
  console.log("Client/socket id is: ", socket.id);
  socket.on( "got_a_new_user", function (data){
      var num = String(math.floor(1000 + math.random() * 9000));
      var user = {session_id: num, user_name: data};
      users.push(user);
      io.emit('new_user', {users});
  });
  socket.on("new_message", function (data){
     io.emit ('send_message', {response: data});
  });
  socket.on("window_closed", function (data){
    for ( var i=0; i<users.length; i++)
    {
      if (users[i].user_name === data.user_name)
      {
        users.splice(i,1);
        break;
      }
    }
    console.log(users);
    io.emit("new_user", {users});
  });
});
