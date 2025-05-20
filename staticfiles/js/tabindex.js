// Función genera un delay
var sleepES5 = function(ms){
    var esperarHasta = new Date().getTime() + ms;
    while(new Date().getTime() < esperarHasta) continue;
};

const tabIndex_form = (modal, btn_search = false) => {
    if (modal == '') {
        document.addEventListener('keypress', function(evt) {
            // Si el evento NO es una tecla Enter
            if (evt.key !== 'Enter') {
              return;
            }
            if (evt.key == 'Enter') {
                evt.preventDefault();
            }

            let element = evt.target;
            // Si el evento NO fue lanzado por un elemento con class "focusNext"
            if (!element.classList.contains('focusNext')) {
              return;
            }
        });
    }
    else {
        $('#'+ modal).on('shown.bs.modal', function () {
            document.addEventListener('keypress', function(evt) {
            
                // Si el evento NO es una tecla Enter
                if (evt.key !== 'Enter') {
                  return;
                }
                let element = evt.target;
                // Si el evento NO fue lanzado por un elemento con class "focusNext"
                if (!element.classList.contains('focusNext')) {
                  return;
                }
                // AQUI logica para encontrar el siguiente
                let tabIndex = element.tabIndex + 1;
                var next = document.querySelector('[tabindex="'+tabIndex+'"]');
              
                // Si encontramos un elemento 
                if (next) {
                    next.focus();
                    evt.preventDefault();
                }
            });
        });
    }

}

function document_actions_tabindex() {
    document.addEventListener('keypress', function(evt) {
        
        // Si el evento NO es una tecla Enter
        if (evt.key !== 'Enter') {
          return;
        }
        let element = evt.target;
        // Si el evento NO fue lanzado por un elemento con class "focusNext"
        if (!element.classList.contains('focusNext')) {
          return;
        }
        // AQUI logica para encontrar el siguiente
        let tabIndex = element.tabIndex + 1;
        var next = document.querySelector('[tabindex="'+tabIndex+'"]');
      
        // Si encontramos un elemento 
        if (next) {
            if (btn_search) {
                if (tabIndex == 3) {
                    $('#btn_search_matricula').click();
                    let dato_alumno;
                    // Realiza un ciclo de busqueda
                    do {
                        dato_alumno = $('input[name=alumno]').val();
                        sleepES5(3000);
                    } while (dato_alumno != '');
                }
            }
            next.focus();
            event.preventDefault();
        }
    });
}