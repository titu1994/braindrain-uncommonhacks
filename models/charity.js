var mongoose = require('mongoose');
var Schema = mongoose.Schema;


// {
//     "description": "The Greatest Story Ever Told",
//     "financial_rating": 64.68,
//     "related_organizations": "0",
//     "administrative_expenses": "420161",
//     "overall_rating": 73.84,
//     "federated_campaigns": "0",
//     "government_funds": "443286",
//     "fundraising_events": "0",
//     "other_revenue": "981080",
//     "mission_statement": "The Abraham Lincoln Presidential Library Foundation supports the educational and cultural programming of the Abraham Lincoln Presidential Library and Museum; fosters Lincoln scholarship through the acquisition and publication of documentary materials relating to Lincoln and his era; and promotes a greater appreciation of history through exhibits, conferences, publications, online services, and other activities designed to promote historical literacy.",
//     "profit": "375241",
//     "transparency_rating": 89,
//     "charity_name": "Abraham Lincoln Presidential Library Foundation",
//     "program_service_revenue": "7446",
//     "address_line2": "Springfield, IL 62701",
//     "fundraising_expenses": "518831",
//     "address_line1": "500 East Madison Street Suite 200",
//     "contributions": "1855258",
//     "membership_dues": "0",
//     "program_expenses": "1972837",
//     "category": "Arts, Culture, Humanities",
//     "phone": "(217) 557-6250"
// }
   

var charitySchema = Schema({
    "description": String,
    "financial_rating": Number,
    "related_organizations": Number,
    "administrative_expenses": Number,
    "overall_rating": Number,
    "federated_campaigns": Number,
    "government_funds": Number,
    "fundraising_events": Number,
    "other_revenue": Number,
    "mission_statement": String,
    "profit": Number,
    "transparency_rating": String,
    "charity_name": String,
    "program_service_revenue": Number,
    "address_line2": String,
    "fundraising_expenses": Number,
    "address_line1": String,
    "contributions": Number,
    "membership_dues": Number,
    "program_expenses": Number,
    "category": String,
    "phone": String
});

var Charity = module.exports = mongoose.model('Charity', charitySchema);

module.exports.createcharity = function(charity, callback){
    Charity.create(charity, callback);
}

module.exports.getcharitybyid = function(id, callback){
    Charity.findById(id, callback);
}
