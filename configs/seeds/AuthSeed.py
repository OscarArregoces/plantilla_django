from django.contrib.auth.hashers import make_password

DocumentTypeSeed = [
    {"name": "Cédula de Ciudadanía"},
    {"name": "Tarjeta de Identidad"},
    {"name": "Registro Civil"},
    {"name": "Cédula de Extranjería"},
    {"name": "Carné de Identidad"},
    {"name": "Documento Nacional de Identidad"},
    {"name": "Pasaporte"},
    {"name": "Licencia de Conducción"},
    {"name": "Libreta Militar"},
    {"name": "Tarjeta Profesional"},
]

PersonsSeed = [
    {
        "fullname": "Usuario Desarrollador",
        "identification": "1111111111",
        "address": "CARRERA 23 # 14 K 22",
        "nationality_id": 49,
        "departamento_id": 764,
        "municipio_id": 685,
        "email": "desarrollador@gmail.com",
        "email2": "",
        "document_type_id": 1,
        "gender_type_id": 1,
        "date_of_birth": "1999-08-28",
    },
    {
        "fullname": "Usuario Administrador",
        "identification": "2222222222",
        "address": "Cll 15# 21-89",
        "nationality_id": 49,
        "departamento_id": 764,
        "municipio_id": 685,
        "document_type_id": 1,
        "gender_type_id": 1,
        "email": "administrador@gmail.com",
        "email2": "",
        "date_of_birth": "1999-08-28",
    },
    {
        "fullname": "Diomedes Diaz de Jeus",
        "identification": "3333333333",
        "address": "Cll 15# 21-89",
        "nationality_id": 49,
        "departamento_id": 764,
        "municipio_id": 685,
        "document_type_id": 1,
        "gender_type_id": 1,
        "email": "diomedes@gmail.com",
        "email2": "",
        "date_of_birth": "1999-08-28",
    },
    {
        "fullname": "Leonel Andres Messi",
        "identification": "4444444444",
        "address": "Cll 15# 21-89",
        "nationality_id": 49,
        "departamento_id": 764,
        "municipio_id": 685,
        "document_type_id": 1,
        "gender_type_id": 1,
        "email": "messi@gmail.com",
        "email2": "",
        "date_of_birth": "1999-08-28",
    },
]

UsersSeed = [
    {
        "username": "desarrollador",
        "password": make_password("12345"),
        "is_staff": True,
        "person_id": 1,
    },
    {
        "username": "admin",
        "password": make_password("12345"),
        "person_id": 2,
    },
    {
        "username": "3333333333",
        "password": make_password("3333333333"),
        "person_id": 3,
    },
    {
        "username": "4444444444",
        "password": make_password("4444444444"),
        "person_id": 4,
    },
]

GroupsSeed = [
    {"name": "Admin"},
    {"name": "Funcionario"},
]

GendersSeed = [
    {"name": "Hombre"},
    {"name": "Mujer"},
    {"name": "Otro"},
]
