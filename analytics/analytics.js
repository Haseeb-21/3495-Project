var mysql = require('mysql');
var mongo = require('mongodb');


var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "Haseeb-2001",
  database: "grades"
});


var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/analytics";

//create database
//MongoClient.connect(url, function(err, db) {
//  if (err) throw err;
//  console.log("Database created!");
//  db.close();
//});

// create collection
//MongoClient.connect(url, function(err, db) {
//   if (err) throw err;
//    var dbo = db.db("mydb");
//    dbo.createCollection("analytics", function(err, res) {
//      if (err) throw err;
//      console.log("Collection created!");
//     db.close();
//    });
//  });

// insert data 
//MongoClient.connect(url, function(err, db) {
//   if (err) throw err;
//    var dbo = db.db("analytics");
//   var myobj = { id: 1, min: 0, max: 100, mean: 0 };
//    dbo.collection("analytics").insertOne(myobj, function(err, res) {
//      if (err) throw err;
//      console.log("1 document inserted");
//      db.close();
//   });
//  });


function updateMongo(min, max, mean) {
// update entry
MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    var dbo = db.db("analytics");
    var myquery = { "id": 1 };
    var newvalues = { $set: { min: min, max: max, mean: mean } };
    dbo.collection("analytics").updateOne(myquery, newvalues, function(err, res) {
      if (err) throw err;
      console.log("1 document updated");
      //db.close();
    });
  });
};

function getAnalytics(data) {
    var grades = [];
    for (let i = 0; i < 7; i++) {
        grades.push(data[i]['grade'])
      }

    var total = 0;
    for(var i = 0; i < grades.length; i++) {
        total += grades[i];
    }

    var min = Math.min.apply(Math, grades)
    var max = Math.max.apply(Math, grades)
    var mean = (total / grades.length).toFixed(2);
    
    updateMongo(min, max, mean)

 } 

function x() {
  var sql = "SELECT * FROM grades";
  con.query(sql, function (err, result) {
    if (err) throw err;
  getAnalytics(result)
  })
}


setInterval(x, 1500)
