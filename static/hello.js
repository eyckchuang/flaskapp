function myFunction() {
  var today= new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  var msg = "";
  if (h<12)
  {
    msg = "good morning,";
  }
  else
  {
    msg= "good";
  }

  document.getElementById('time').innerHTML = msg + "-" + h + ":" + m + ":" +s;
}