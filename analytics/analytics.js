var mysql = require('mysql2');

var con = mysql.createConnection({
  host: "mysql_db",
  user: "root",
  password: "123",
  database: "grades"
});


var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://mongo_db:27017/analytics";

function updateMongo(min, max, mean) {
// update entry
MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    var dbo = db.db('analytics');
    dbo.listCollections().toArray((err, collections) => {
        if (collections.length == 0) {
          dbo.createCollection("statistics", function(err, res) {
            if (err) throw err;
            console.log("Collection created!");
          });
          myobj =  { id: 1, min: 0, max: 0, mean: 0 } ;
          dbo.collection("statistics").insertOne(myobj)
        }
          
        })
    
    var dbo = db.db("analytics");
    var myquery = { "id": 1 };
    var newvalues = { $set: { min: min, max: max, mean: mean } };
    dbo.collection("statistics").updateOne(myquery, newvalues, function(err, res) {
      if (err) throw err;
      //console.log("1 document updated");
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

function readMySQL() {
  var sql = "SELECT * FROM grades";
  con.query(sql, function (err, result) {
    if (err) throw err;
  getAnalytics(result)
  })
}


setInterval(readMySQL, 1500)
