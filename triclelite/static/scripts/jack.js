$( document ).ready(function() {

urlId = "Empty"
//on post, run the ajax
$("#submit").click(function(e){
        e.preventDefault();
        var formData = new FormData($('form')[0])
        for (var pair of formData.entries()) {
    console.log(pair[0]+ ', ' + pair[1]);
}
        /*
        formData.append("csrfmiddlewaretoken", $('token').val());

        formData.append("key_one", $('[name="key_one"]').val());
        formData.append("key_two", $('[name="key_two"]').val());
        formData.append("key_three", $('[name="key_three"]').val());
        formData.append("mode", $('[name="mode"]').val());
        */

        $.ajax({type: "POST",
                url: "/",
                data: formData,
                processData: false,
                contentType: false,
                dataType: 'json',
                success:function(result)
                {
                    console.log(result)
                }
                }
              );
      });
    });
//store the url if success, or show Error
//if success, call ajax to load
//if load success, click the download button
//if error, show  error

/*
    $.ajax({
      url: urlId,
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
  */

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
