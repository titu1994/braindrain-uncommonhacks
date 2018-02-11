var mongoose = require("mongoose");
var Schema = mongoose.Schema;
var crypto = require('crypto');
var jwt = require('jsonwebtoken');

//Create Schema.
var userSchema = new Schema({
    name: String,
    donations: [
        {
            charityType: String,
            amount: {
                default: 0,
                type: Number
            }
        }
    ],
    charities:[
        {
            id: Number,
            name: String
        }
    ],
    email:{
        type: String,
        required: true
    },
    password: String
})

var User = module.exports = mongoose.model('User', userSchema);


//Model Methods.
userSchema.methods.validateLogin = function (password){
    if (this.password == password){
        return true
    }
    else{
        return false
    }
}
module.exports.createuser = function(user, callback){
    try{
        User.create(user, callback);
    } catch (ex){
        console.log(ex);
    }
};

module.exports.getuserbyid = function(id, callback){
    User.findById(id, callback);
}
// module.exports.createUser = function(user, callback){
//     User.create(user, callback);
// }

// user.methods.setPassword = function (password) {
//     this.salt = crypto.randomBytes(16).toString('hex');
//     this.hash = crypto.pbkdf2Sync(password, this.salt, 1000, 64,'sha512').toString('hex');
// }

// user.methods.validPassword = function(password){
//     var hash = crypto.pbkdf2Sync(password, this.salt, 1000, 64, 'sha512').toString('hex');
//     return this.hash == hash
// }

// user.methods.generateJWT = function(){
//     var expiry = new Date();
//     expiry.setDate(expiry.getDate()+7);
//     return jwt.sign({
//         _id: this._id,
//         email: this.email,
//         exp: parseInt(expiry.getTime() / 1000),
//     },"My_SECRET");
// }