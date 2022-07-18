class ID_Already_Exists(Exception):
    """
    Excepcion lanzada cuando se intenta cambiar el ID y ese ID ya esta siendo usado
    """
    pass;

class InvalidCharField(Exception):
    """
    Excepcion lanzada cuando se intenta cambiar un campo varchar/text por un digito, vacio o sobrepasa la longitud
    """
    pass;

class InvalidNameField(Exception):
    """
    Excepcion lanzada cuando el nombre o apellido de la búsqueda es numerico
    """
    pass;

class InvalidDescField(Exception):
    """
    Excepcion lanzada cuando las descripciones pertinentes al tratamiento o dolencia son digitos
    """
    pass;

class InvalidPacientID(Exception):
    """
    Excepcion lanzada cuando el ID no existe en la base de datos, en la tabla de pacientes
    """
    pass;

class InvalidBillID(Exception):
    """
    Excepcion lanzada cuando el ID no existe en la base de datos, en la tabla de factura
    """
    pass;