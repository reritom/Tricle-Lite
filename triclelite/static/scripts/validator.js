$(document).ready(function() {

minLength = 3;
k1Stat = false;
k2Stat = false;
k3Stat = false;

keysStat = false;

$("#K1").keyup(function(event){
  console.log($("#K1").val());
  if ($("#K1").val().length < minLength) {
    k1Stat = false;
  }
  else {
    k1Stat = true;
  }
}); // End of K1 keyup

$("#K2").keyup(function(event){
  console.log($("#K2").val());
  if ($("#K2").val().length < minLength) {
    k2Stat = false;
  }
  else {
    k2Stat = true;
  }
}); // End of K1 keyup

$("#K3").keyup(function(event){
  console.log($("#K3").val());
  if ($("#K3").val().length < minLength) {
    k3Stat = false;
  }
  else {
    k3Stat = true;
  }
}); // End of K1 keyup

}); //End of document ready

function validateKeys() {

}

function getValidationStatus(){

}
