function openNav() {
    document.getElementById("sideNavBar").style.width = "400px";
    document.getElementById("sideNavBar").style.right = "0";
    document.getElementById("sideNavBar").classList.add("collapse");
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("sideNavBar").style.width = "0";
    document.getElementById("sideNavBar").classList.remove("collapse");
}

var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    var currentScrollPos = window.pageYOffset;
    if (currentScrollPos > prevScrollpos) {
        document.getElementById("navBar").style.height = "1%";
    } else {
        document.getElementById("navBar").style.height = "5%;";
    }
}


jQuery('body').bind('click', function (e) {
    if (jQuery(e.target).closest('.sidebarnavid').length == 0) {
        if (document.getElementById("sideNavBar").classList.contains('collapse')) {
            closeNav();
        }
    }
});
