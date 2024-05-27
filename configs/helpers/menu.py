resources = [
    {
        "id_padre": 0,
        "path": "/inicio/",
        "icono": "pi pi-home",
        "method": "GET",
        "link": "/inicio/",
        "titulo": "Inicio",
        "items": [
            {
                "path": "/inicio/datos-personales/",
                "icono": "icon",
                "link": "/inicio/datos-personales/",
                "method": "GET",
                "titulo": "Datos Personales",
                "items": [
                    {
                        "path": "/inicio/datos-personales/actualizar-datos/",
                        "icono": "icon",
                        "method": "POST",
                        "link": "/inicio/datos-personales/actualizar-datos/",
                        "titulo": "Actualizar Datos",
                    },
                ],
            },
        ],
    },
]


resources_admin = [
    {"id":1},
    {"id":2},
    {"id":3},
]