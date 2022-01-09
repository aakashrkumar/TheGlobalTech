$(document).ready(function () {
    $('.main-content').css('display', 'none');
    $('.main-content').fadeIn(2000);
    $('.link').click(function (event) {
        event.preventDefault();
        $('.main-content').fadeOut(2000);
        newLocation = $('.link a').attr("href");
    });

    function newpage() {
        window.location = newLocation;
    }
});
