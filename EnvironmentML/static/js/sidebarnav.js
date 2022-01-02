function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
}

jQuery('body').bind('click', function (e) {
    if (jQuery(e.target).closest('.sidebarnav').length == 0) {
        console.log("click")
        // click happened outside of .navbar, so hide
        var opened = jQuery('.sidebarnav').style.width == "0";
        if (opened === true) {
            closeNav();
        }
    }
});
