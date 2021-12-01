var express  = require('express');
var app = express();
var mongoose = require('mongoose');
var bodyParser = require("body-parser");
var User = require("./models/user");
var auth = require("./middleware/auth");
var passport = require('passport');
var LocalStrategy  = require('passport-local');
var passportLocalMongoose  = require('passport-local-mongoose');
var bcrypt= require('bcrypt-nodejs');
const { use } = require('passport');
const jwt = require("jsonwebtoken");
var cors = require('cors');
const schedule = require('node-schedule');

const multer = require('multer');
const path = require('path');
const fs = require('fs');
/*********************************************************************************************************************************************************** */
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*"); // update to match the domain you will make the request from
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

//database connection
mongoose.connect("mongodb+srv://amankumar:mongopass@cluster0.hhmjr.mongodb.net/database?retryWrites=true&w=majority",{ useNewUrlParser: true, useUnifiedTopology: true});
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());
app.use(cors());


//Sign-up
app.post("/user/signup",cors(), async(req, res) => {
  const user = new User(req.body)
  try{
    await user.save()
    const token = await user.generateauthtoken()
    res.status(201).json({user, token})
  } catch(e){
    res.status(400).send("Username already exists");
  }
});

// Login
app.post("/user/login",cors(), async(req, res)=> {
  try{
    const user = await User.findbycredentials(req.body.username, req.body.password);
    const token = await user.generateauthtoken()
    res.status(200).send({user, token}); 

  } catch(e){
    res.status(400).send("Wrong Credentials");
}
});


//main link read
app.get('/mainlink/:username',(req,res)=>{
	User.find({"username":req.params.username},function(err,result){
		        if(err){
            res.send(err)
        }
        else{
            res.json(result);
        }
	})
})

app.get('/administrator',(req,res)=>{
	User.find({},function(err,result){
		        if(err){
            res.send(err)
        }
        else{
            res.json(result);
        }
	})
})

// //sublink count update
// app.get('/sublink/countinc/:id',(req,res)=>{
// 	User.findOneAndUpdate({"sublinks._id":req.params.id}, {$inc:{"sublinks.$.count":1}},
//     (err, result) => {
//     if (err) {
//       res.json({
//         status:400,
//         success:false, 
//         message:err
//       })
//     }
//     else{	
//     res.json(result);
//     }
//   }) 
// })


// //sublink update
// app.post('/sublinks/update/:id',(req,res)=>{
// 	User.findOneAndUpdate({"sublinks._id":req.params.id},{"$set": {"sublinks.$.name" :req.body.name , "sublinks.$.link" : req.body.link}},{"new": true, "upsert": true},
// 						   function(err,result){
// 		        if(err){
//             res.send(err)
//         }
//         else{
//             res.json(result);
//         }
// 	})
// })

//mainlink count update 
app.get('/mainlink/countinc/:username',(req,res)=>{
	User.findOneAndUpdate({"username":req.params.username},{$inc:{creditScore:10}},{"multi": true},(err, result) => {
    if (err) {
      res.json({
        status:400,
        success:false,
        message:err
      })
    }
    else{	
    res.json(result);
    }
  }) 
}) 

app.get('/mainlink/countdec/:username',(req,res)=>{
	User.findOneAndUpdate({"username":req.params.username},{$inc:{creditScore:-10}},{"multi": true},(err, result) => {
    if (err) {
      res.json({
        status:400,
        success:false,
        message:err
      })
    }
    else{	
    res.json(result);
    }
  }) 
}) 

// Profile Pic
  var myStorage = multer.diskStorage({
    destination:function(req,file,cb){
        cb(null,'uploads')
    },
    filename:function(req,file,cb){
        cb(null,file.fieldname + '-' + Date.now() + path.extname(file.originalname))
    }
  })

  var upload = multer({
    storage:myStorage
  });

  app.post('/upload/:username', async(req, res) => {
    var img = req.body.image;
      User.findOneAndUpdate({"username":req.params.username}, {"$set": {"img" : img}},(err, result) => {
        if (err) {
          res.json({
            status:400,
            success:false, 
            message:err
          })
        }
        else{	
            res.json(result);
        }
      })  
  })

var port = process.env.PORT || 3000;
app.listen(port, function(){
	console.log("server started");
});