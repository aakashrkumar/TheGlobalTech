var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("slidesContainer");
    if (n > slides.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex - 1].style.display = "block";
    slides[slideIndex - 1].children[0].style.height = $(".project-card:visible").outerWidth() + "px";
    // if height was updated to 0, wait for it to update and try again
    if (slides[slideIndex - 1].children[0].style.height == "0px") {
        setTimeout(function () {
            slides[slideIndex - 1].children[0].style.height = $(".project-card:visible").outerWidth() + "px";
        }, 100);
    }
    console.log(slides[slideIndex - 1].children[0].style.height);
    if ($(window).width() < 600) {
        $("#home-aligner").removeClass("valign-wrapper");
    }
    // add the class align-center valign-wrapper if screen size is more than 600px
    else {
        $("#home-aligner").addClass("valign-wrapper");
    }

}

// on resize
$(window).resize(function () {
    $(".slidesContainer").children().css("height", $(".project-card:visible").outerWidth() + "px");
    // get div by the id home-aligner and remove the class align-center valign-wrapper if screen size is less than 600px
    if ($(window).width() < 600) {
        $("#home-aligner").removeClass("valign-wrapper");
    }
    // add the class align-center valign-wrapper if screen size is more than 600px
    else {
        $("#home-aligner").addClass("valign-wrapper");
    }
});
