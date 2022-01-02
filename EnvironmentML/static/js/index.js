var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("sidebarnav").style.top = "0";
    } else {
        document.getElementById("sidebarnav").style.top = "-50px";
    }
    prevScrollpos = currentScrollPos;
}

function isImage(filename) {
    return ["png", "jpg", "jpeg", "svg"].includes(filename.split('.').pop());
}