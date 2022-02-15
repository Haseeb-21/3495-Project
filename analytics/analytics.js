var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "Haseeb-2001",
  database: "grades"
});

function getAnalytics(data) {
    var grades = [];
    for (let i = 0; i < 7; i++) {
        grades.push(data[i]['grade'])
      }

    var total = 0;
    for(var i = 0; i < grades.length; i++) {
        total += grades[i];
    }

    var avg = (total / grades.length).toFixed(2);
    var min = Math.min.apply(Math, grades)
    var max = Math.max.apply(Math, grades)
    console.log(min, max, avg)

 } 
con.connect(function(err) {
    if (err) throw err;
    var sql = "SELECT * FROM grades";
    con.query(sql, function (err, result) {
      if (err) throw err;
    getAnalytics(result)
    con.end()
    });
  });
