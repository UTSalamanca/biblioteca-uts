window.onload = function () {
    $('#loaderID').fadeOut('slow', function () {
        $('#bodyMaster').removeClass('loaderHidden');
    });
}

$(document).ajaxStart(function () {
    $('#loaderID').fadeIn(); // Muestra el loader
    $('#bodyMaster').addClass('loaderHidden'); // Bloquea scroll si quieres
});

$(document).ajaxStop(function () {
    $('#loaderID').fadeOut(); // Oculta el loader
    $('#bodyMaster').removeClass('loaderHidden'); // Reactiva scroll
});

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