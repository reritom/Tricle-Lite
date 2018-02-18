$(document).ready(function() {
    /*
      TODO
      - Add check before download to see if this valid
    */
    urlId = false; // Global variable. Gets reset on 'Done'
    started = false;
    sessionToken = false;

    $("#submit").click(function(e) {
        /*
          On click of the form, the data is posted.
          If successful, the loader is automatically called.
        */
        e.preventDefault();
        sessionToken = generateToken();
        $("#RT").val(sessionToken);
        var formData = new FormData($('form')[0]);
        /*
        // For seeing the form data
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);

        }
        */
        $.ajax({
            type: "POST",
            url: "/post",
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(result) {
                console.log(result);
                if (result.post === true) {
                    urlId = result.url;
                    startLoad(urlId);
                }
            },
            error: function() {
                console.log("aww shit, something went wrong")
            }
        }); // End of AJAX
    }); //End of submit click

}); //End of ready


function startLoad(urlId) {
    /*
      This method starts processing the files, and then
      calls the downloader if successful.
    */
    if (!urlIsValid()) {
        return
    };
    $.ajax({
        type: "GET",
        url: "/" + "load" + "/" + urlId + "/",
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function(result) {
            console.log(result);
            //Unhide download button
            // Start auto-download
            if (result.load === true) {
                urlId = result.url;
                isDownloadable();
            }
        },
        error: function() {
            console.log("aww shit, something went wrong")
        }
    }); // End of AJAX
}

function startDown() {
    /*
      This method attempts to download the zip file
    */
    if (!urlIsValid()) {
        return
    };
    console.log("Downloading file");
    window.location = "/" + "down" + "/" + urlId + "/" + "?" + "token=" + sessionToken;
}

function amDone() {
    /*
      This method calls the cleanup view.
    */
    if (!urlIsValid()) {
        return
    };
    console.log("Ending process");
    $.ajax({
        type: "GET",
        url: "/" + "done" + "/" + urlId + "/",
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function(result) {
            console.log(result);
            urlId = false;
        },
        error: function() {
            console.log("aww shit, something went wrong")
        }
    }); // End of AJAX
}

function isDownloadable(){
  /*
    Return true if the urlId is still valid for downloads
  */
  if (!urlIsValid()) {
      return false
  };

  $.ajax({
      type: "GET",
      url: "/" + "status" + "/" + urlId + "/",
      processData: false,
      contentType: false,
      dataType: 'json',
      success: function(result) {
          console.log(result);
          if (result.valid && result.downloadable){
            console.log("am here");
            startDown();
          }
          else {
            errorHandler("Download limit reached");
          };
      },
      error: function() {
          console.log("aww shit, something went wrong")
      }
  }); // End of AJAX

}

function urlIsValid() {
    /*
      Return true if the urlId global variable is set
    */
    if (urlId === false) {
        console.log("url is invalid");
        errorHandler("url is invalid");
        return false;
    } else {
        successHandler();
        return true;
    }
}

function errorHandler(message) {
    /*
      Format a message and display it.
    */
    $("#errorDiv").show();
    $("#errorMessage").html(message);
}

function successHandler() {
    /*
      Format a message and display it.
    */
    $("#errorDiv").hide();
    $("#errorMessage").html("");
}

function startOrRestart() {
    console.log("In SOR");
    console.log(started);
    if (started === false) {
      console.log("Started is false");
      if (true === true) {
        console.log("Validated is true");
        // Click the form submit
        $('#submit')[0].click();

        if (urlId != false) {
          // If successful, started = true
          started = !started;

          // Rename the start button to restart
            $('#submit').html("Restart");
        }
      }

    }
    else if (started == true){
      // Remove the urlId
      urlId = false;

      // Rename the button to start
      $('#submit').html("Start");

      started = !started;
    };
}

function generateToken() {
  console.log("Generation token");
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  )
}

function retrieveForm() {
  console.log("Creating retrieve form");
  var formData = new FormData();
  formData.append("retrieve_token", sessionToken);
  return formData
}
