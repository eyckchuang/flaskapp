function myfunction(id)
{
  var nm=document.getElementById("nmId").value;
  var btn= document.getElementById(id).name;
  if(btn == "button1")
  {
    alert(nm+", Of Course u can vote! cheers");
  }
  else
  {
    alert(nm+", no ");
  }
}