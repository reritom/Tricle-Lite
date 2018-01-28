$(document).ready(function() {
    /*
      TODO
      - Add check before download to see if this valid
    */
    urlId = false // Global variable. Gets reset on 'Done'

    $("#submit").click(function(e) {
        /*
          On click of the form, the data is posted.
          If successful, the loader is automatically called.
        */
        e.preventDefault();
        var formData = new FormData($('form')[0])
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
        }
        $.ajax({
            type: "POST",
            url: "/",
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
        url: "/" + "load" + "/" + urlId,
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function(result) {
            console.log(result);
            //Unhide download button
            // Start auto-download
            if (result.load === true) {
                urlId = result.url;
                startDown(urlId);
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
    window.location = "/" + "down" + "/" + urlId;
    //AJAX call a tester, if the download is still valid, download
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
        url: "/" + "done" + "/" + urlId,
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
