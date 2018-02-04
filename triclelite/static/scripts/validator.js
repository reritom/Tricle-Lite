$(document).ready(function() {

minLength = 3;
keyStats = [false, false, false];
validated = false;

$("#K1").keyup(function(event){
  console.log($("#K1").val());
  keyStats[0] = ($("#K1").val().length < minLength)? false : true;
  validateKeysBorder();
}); // End of K1 keyup

$("#K2").keyup(function(event){
  console.log($("#K2").val());
  keyStats[1] = ($("#K2").val().length < minLength)? false : true;
  validateKeysBorder();
}); // End of K1 keyup

$("#K3").keyup(function(event){
  console.log($("#K3").val());
  keyStats[2] = ($("#K3").val().length < minLength)? false : true;
  validateKeysBorder();
}); // End of K1 keyup

function validateKeysBorder() {
  var numOfTrue = 0;
  // See how many keys are valid
  console.log("Hello");
  for (var i = 0; i < keyStats.length; i++) {
      if (keyStats[i] === true) { //increment if true
        numOfTrue++;
      }
  }
  console.log("Number of true");
  console.log(numOfTrue);
  console.log("Length");
  console.log(keyStats.length);
  console.log(validated);
  validated = (keyStats.length === numOfTrue)? true : false;
}



}); //End of document ready
