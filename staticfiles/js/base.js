window.onload = function () {
    $('#loaderID').fadeOut()
    $('#bodyMaster').removeClass('loaderHidden')
}

// Custom
// var customElement = $("<div>", {
//     "css": {
//         "font-size": "35px",
//         "text-align": "center",
//         "padding": "10px",
//         "color": "white"
//     },
//     "class": "your-custom-class",
//     "text": "Cargando..."
// });
// $.LoadingOverlay("show", {
//     image: "img/mapache.svg",
//     background: "rgba(0, 0, 0, 0.556)",
//     custom: customElement
// });
//
// window.onload = function () {
//     $.LoadingOverlay("hide")
// }