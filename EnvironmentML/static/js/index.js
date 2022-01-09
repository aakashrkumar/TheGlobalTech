$(document).ready(function() {
  $('body').css('display', 'none');
  $('body').fadeIn(1000);
  $('.link').click(function(event) {
    event.preventDefault();
    newLocation = $('.link a').attr("href");
    $('body').fadeOut(1000, newpage);
  });
  function newpage() {
    window.location = newLocation;
  }
});
