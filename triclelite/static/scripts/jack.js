$( document ).ready(function() {

urlId = false
//on post, run the ajax
$("#submit").click(function(e){
        e.preventDefault();
        var formData = new FormData($('form')[0])
        for (var pair of formData.entries()) {
    console.log(pair[0]+ ', ' + pair[1]);
}
        $.ajax({type: "POST",
                url: "/",
                data: formData,
                processData: false,
                contentType: false,
                dataType: 'json',
                success:function(result)
                {
                    console.log(result);
                    if (result.post === true) {
                      urlId = result.url;
                      startLoad(urlId);
                    }
                }
                }
              ); // End of AJAX
      }); //End of submit click

    }); //End of ready


  function startLoad(urlId) {
    // Code to be executed
    if (urlIsValid()) {
    $.ajax({type: "GET",
            url: "/" + "load" + "/" + urlId,
            processData: false,
            contentType: false,
            dataType: 'json',
            success:function(result)
            {
                console.log(result);
                //Unhide download button
                // Start auto-download
                if (result.load === true) {
                  urlId = result.url;
                  startDown(urlId);
                }
            }
            }
          ); // End of AJAX
        }; //End of URL is Valid
}

  function startDown() {
    // Code to be executed
    if (urlIsValid()){
    console.log("Downloading file");
    window.location="/" + "down" + "/" + urlId;
  }; // End of URL is Valid
    //AJAX call a tester, if the download is still valid, download
}

  //AJAX Done
  //    If success:
  //        Finished animation
  //        Reset page
  function amDone() {
    // Code to be executed
    console.log("Ending process");
    if (urlIsValid()){
    $.ajax({type: "GET",
            url: "/" + "done" + "/" + urlId,
            processData: false,
            contentType: false,
            dataType: 'json',
            success:function(result)
            {
                console.log(result);
                urlId = false;
            }
            }
          ); // End of AJAX
        };// End of URL is valid
}

function urlIsValid() {
  if (urlId === false){
    console.log("url is invalid")
    return false;
  }
  else {
    return true;
  }
}
