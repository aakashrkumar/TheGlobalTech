function openNav() {
    document.getElementById("sideNavBar").style.width = "250px";
    document.getElementById("sideNavBar").classList.add("collapse");
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("sideNavBar").style.width = "0";
    document.getElementById("sideNavBar").classList.remove("collapse");
}

jQuery('body').bind('click', function (e) {
    if (jQuery(e.target).closest('sideNavBar').length == 0) {
        console.log('clicked outside of sideNavBar');
        console.log(document.getElementById("sideNavBar").style.width);
        if (document.getElementById("sideNavBar").classList.contains('collapse')) {
            closeNav();
        }
    }
});
