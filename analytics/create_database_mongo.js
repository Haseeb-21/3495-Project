var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/analytics";

//create database
MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  console.log("Database created!");
  db.close();
});

//create collection
MongoClient.connect(url, function(err, db) {
   if (err) throw err;
    var dbo = db.db("analytics");
    dbo.createCollection("analytics", function(err, res) {
      if (err) throw err;
      console.log("Collection created!");
     db.close();
    });
  });

//insert data 
MongoClient.connect(url, function(err, db) {
   if (err) throw err;
    var dbo = db.db("analytics");
   var myobj = { id: 1, min: 0, max: 0, mean: 0 };
    dbo.collection("analytics").insertOne(myobj, function(err, res) {
      if (err) throw err;
      console.log("1 document inserted");
      db.close();
   });
  });