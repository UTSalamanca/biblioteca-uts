def get_paginas_avanzadas(pagina_actual, total_paginas, max_paginas=5):
    """
    Retorna una lista con números de página y '...' si es necesario.
    Ejemplo: [1, '...', 4, 5, 6, '...', 10]
    """
    if total_paginas <= max_paginas + 2:
        return list(range(1, total_paginas + 1))

    paginas = []
    mitad = max_paginas // 2
    inicio = max(pagina_actual - mitad, 1)
    fin = min(pagina_actual + mitad, total_paginas)

    if inicio > 2:
        paginas.extend([1, '...'])
    else:
        paginas.extend(range(1, inicio))

    paginas.extend(range(inicio, fin + 1))

    if fin < total_paginas - 1:
        paginas.extend(['...', total_paginas])
    elif fin < total_paginas:
        paginas.append(total_paginas)

    return paginas