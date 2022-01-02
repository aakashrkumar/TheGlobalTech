function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
}

jQuery('body').bind('click', function (e) {
    if (jQuery(e.target).closest('.navbar').length == 0) {
        // click happened outside of .navbar, so hide
        var opened = jQuery('.navbar-collapse').hasClass('collapse in');
        if (opened === true) {
            jQuery('.navbar-collapse').collapse('hide');
        }
    }
});
