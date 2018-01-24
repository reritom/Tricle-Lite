$( document ).ready(function() {

url = None
//on post, run the ajax
//store the url if success, or show Error
//if success, call ajax to load
//if load success, click the download button
//if error, show  error


      $.ajax({
        url: $('#runProc').attr("href"),
        dataType: 'json',
        success: function (data) {
          if (data.proc) {
            $('#note').text("Your download is ready");;
            $('#done_link').css("display", "block");

            $('#downen_link')[0].click();

            }
        else {
          }
        }
    });
  });

  //AJAX Post
  //    Show loading animation
  //    If success:
  //        Call load automatically

  //AJAX Load
  //    If success:
  //        Unhide download button
  //        Call download automatically

  //AJAX Download
  //    If success:
  //        Unhide done button

  //AJAX Done
  //    If success:
  //        Finished animation
  //        Reset page
