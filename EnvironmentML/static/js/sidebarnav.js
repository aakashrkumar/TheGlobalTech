function openNav() {
    document.getElementById("sideNavBar").style.width = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("sideNavBar").style.width = "0";
}

jQuery('body').bind('click', function (e) {
    if (jQuery(e.target).closest('sideNavBar').length == 0) {
        if (document.getElementById("sideNavBar").style.width == "250px") {
            closeNav();
        }
    }
});
