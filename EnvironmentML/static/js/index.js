$(document).ready(function () {

    $('.main-content').css('display', 'none');

    $('.main-content').fadeIn(1000);


    $('.link').click(function (event) {

        event.preventDefault();

        newLocation = this.href;

        $('.main-content').fadeOut(1000, newpage);

    });


    function newpage() {

        window.location = newLocation;

    }

});

