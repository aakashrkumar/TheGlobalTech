

function isImage(filename) {
    return ["png", "jpg", "jpeg", "svg"].includes(filename.split('.').pop());
}