
// show loading robot on form submit
$('#upload_form button[type="submit"]').on('click', function() {
  $('.welcome-robot-div').addClass('hide-stuff');
  $('.waiting-robot-div').addClass('show-stuff');
  $('.status-message').removeClass('hide-stuff');
  $('.flash-messages').hide();
  animatePoints();
});

$('#try-button').on('click', function() {
  $('.custom-file-input').click();
});

var animatePoints = function() {
  if ($('.status-points').text() == "") {
    $('.status-points').text('.');
    setTimeout(function() {
      animatePoints();
    }, 700);
  } else if ($('.status-points').text() == ".") {
    $('.status-points').text('..');
    setTimeout(function() {
      animatePoints();
    }, 700);
  } else if ($('.status-points').text() == "..") {
    $('.status-points').text('...');
    setTimeout(function() {
      animatePoints();
    }, 700);
  } else if ($('.status-points').text() == "...") {
    $('.status-points').text('');
    setTimeout(function() {
      animatePoints();
    }, 700);
  }
}

// show file name after selecting file
$('#inputGroupFile01').on('change',function(){
    var fileName = $(this).val();
    $(this).next('.custom-file-label').html(fileName);
});

// show modal with enlarged image on click
$("#imageresource").on("click", function() {
  $('#image_modal').modal();
  $('#imagepreview').attr('src', $('#imageresource').attr('src'));
  $('#image_modal').modal('show');
});

// close modal again on click
$(".modal-footer button").on("click", function() {
  $("#image_modal").modal("toggle");
})
