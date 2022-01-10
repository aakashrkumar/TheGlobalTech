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
        slides[i].classList.remove("active-project-card");
    }
    slides[slideIndex - 1].style.display = "block";
    slides[slideIndex - 1].children[0].classList.add("active-project-card");
    slides[slideIndex - 1].children[0].style.height = $(".active-project-card").outerWidth() + "px";
    console.log();
}

// on resize
$(window).resize(function () {
    $(".slidesContainer").children().css("height", $(".project-card").outerWidth() + "px");
});
