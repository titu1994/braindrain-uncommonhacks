// Imports
var express = require("express");
var bodyParser = require("body-parser");
var app = express();
User = require("./models/models.js");
Charity = require("./models/charity.js")

var mongoose = require('mongoose')
mongoose.Promise = global.Promise;

var uristring =
    process.env.MONGOLAB_URI ||
    process.env.MONGOHQ_URL ||
    'mongodb://dkaush4:qwerty123@ds231758.mlab.com:31758/charitydb';

    // The http server will listen to an appropriate port, or default to
// port 5000.
var theport = process.env.PORT || 5000;

mongoose.connect(uristring, function(err){
    if(err){
        throw err;
    }
    else{
        console.log("Successfully connected to DB..")
    }
});
var db = mongoose.connection;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", function (req, res){
    res.status(200).send("First endpoint here. Hit another endpoint to get data.")
    console.log("Here");
});

//USER Endpoints.
//GET
app.get('/getuser/:id', function(req, res){
    User.getuserbyid(req.params.id, function (err, user){
        if(err){
            throw err;
        }
        res.status(200).json(user)
    });
});
//CREATE USER
app.post('/createuser', function(req, res){
    var user = req.body
    User.createuser(user, (err, user)=> {
        if(err){
            throw err;
        }
        res.status(200).json(user);
    });
});
// app.post('/login', function(req, res){
    
// });

//Charity 
app.get('/getcharity/:id', function(req,res){
    Charity.getcharitybyid(req.params.id, function(err, charity){
        if(err){
            throw err;
        }
        res.status(200).json(charity)
    });
});
app.post('/createcharity', function(req, res){
    var charity = req.body;
    Charity.createcharity(charity, (err, charity)=>{
        if (err){
            throw err;
        }
        res.status(200).json(charity);
    });
});

//Load HTTP module
var http = require("http");

//Create HTTP server and listen on port 8000 for requests
http.createServer(function (request, response) {

   // Set the response HTTP header with HTTP status and Content type
   response.writeHead(200, {'Content-Type': 'text/plain'});
   
}).listen(theport);