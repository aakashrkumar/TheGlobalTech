$(document).ready(function () {
    $('.main-content').css('display', 'none');
    $('.main-content').fadeIn(2000);
    $('.link').click(function (event) {
        event.preventDefault();
        newLocation = $('.link a').attr("href");
        $('.main-content').fadeOut(2000);
    });

    function newpage() {
        window.location = newLocation;
    }
});
