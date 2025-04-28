$.LoadingOverlay("show");

window.onload = function () {
    $.LoadingOverlay("hide")
}

$(document).ajaxStart(function () {
    $.LoadingOverlay("show");
});
// 
$(document).ajaxStop(function () {
    $.LoadingOverlay("hide");
});