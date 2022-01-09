function isImage(filename) {
    return ["png", "jpg", "jpeg", "svg"].includes(filename.split('.').pop());
}

function fadeInPage() {
    if (!window.AnimationEvent) {
        return;
    }
    var fader = document.getElementById('fader');
    fader.classList.add('fade-out');
}