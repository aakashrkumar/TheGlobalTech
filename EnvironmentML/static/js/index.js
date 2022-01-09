$(document).ready(function () {

    $('.main-content').css('display', 'none').fadeIn(2000);

    $('.link').click(function (event) {

        event.preventDefault();

        newLocation = this.href;

        $('.main-content').fadeOut(2000, newpage);

    });


    function newpage() {

        window.location = newLocation;

    }

});

