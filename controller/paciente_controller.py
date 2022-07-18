# Como puedes comprobar esto es más bien como si usaras un service en Angular, por lo que tal y como estoy implementado el MVC es más bien una copia a como lo hace Angular
# La view representa los datos y recoge el input (gestionandolo) para llamar al servicio (controller)
# El controller llama al model determinado y devuelve los datos a la vista
# El model realiza la operación pertinente en la DB y le devuelve los datos al controller
# PD: Movi el manejo y manipulacion del INPUT al controller porque me parecia que la View hacia demasiado si no
from models.paciente import Paciente;
from auxiliary.colors import colors as c;
from auxiliary.custom_exceptions import InvalidCharField, InvalidNameField, InvalidDescField, InvalidPacientID;

def mostrar_pacientes():
    return Paciente.mostrar_pacientes();

def buscar_pacientes():
    bandera:bool = True;
    while bandera:
        try:
            # No pasa nada si son vacios, al usar un LIKE % retorna todos
            nombre = input(f"{c.BRIGHTGREEN}\tNOMBRE [-1 SALIR]: ");
            apellidos = input(f"\tAPELLIDOS: ");
            clientePreferencial = input(f"\t¿TRATO PREFERENCIAL? [S/N]: ")
            desc_dolencia = input(f"\tDESCRIPCIÓN DE LA DOLENCIA: ");
            desc_tratamiento = input(f"\tDESCRIPCIÓN DEL TRATAMIENTO: ");

            if (nombre == "-1"):
                return;

            if ((not nombre.isalpha() or not apellidos.isalpha()) and (nombre != "" and apellidos != "")):
                raise InvalidNameField;
            if (clientePreferencial != "S" and clientePreferencial !="N" and clientePreferencial != ""):
                raise ValueError;
            if (desc_dolencia.isdigit() or desc_tratamiento.isdigit()):
                raise InvalidDescField;
            if (len(nombre) == 0 and len(apellidos) == 0 and len(clientePreferencial) == 0 and len(desc_dolencia) == 0 and len(desc_tratamiento) == 0):
                raise InvalidCharField;
        except InvalidNameField:
            print(f"{c.BRIGHTRED}ERROR: CAMPOS NOMBRE Y APELLIDOS DEBEN DE SER ALFABÉTICOS{c.ENDC}");
        except InvalidDescField:
            print(f"{c.BRIGHTRED}ERROR: CAMPO(S) DESCRIPTIVOS NO VÁLIDOS{c.ENDC}");
        except InvalidCharField:
            print(f"{c.BRIGHTRED}ERROR: AL MENOS HA DE HABER UN CAMPO RELLENADO{c.ENDC}");
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: CAMPO NO VÁLIDO [S/N] SOLO{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            if (clientePreferencial == "S"):
                clientePreferencial = 1;
            elif (clientePreferencial == "N"):
                clientePreferencial = 0;
            else:
                clientePreferencial = "";
            # Otra forma sería creando un objeto Paciente y pasandoselo a un metodo que acepte el objeto per se
            return Paciente.mostrar_pacientes_por_campo(nombre=nombre, apellidos=apellidos, clientePreferencial=clientePreferencial, desc_dolencia=desc_dolencia, desc_tratamiento=desc_tratamiento);

def mostrar_facturas(ids):
    # Este metodo, a diferencia del otro, muestra las facturas desglosadas
    bandera:bool = True;
    while bandera:
        try:
            paciente_id = int(input(f"{c.BRIGHTGREEN}INTRODUZCA EL ID DEL PACIENTE PARA BUSCAR SUS FACTURAS [-1 = SALIR]: "));
            if (paciente_id == -1):
                return;
            if (paciente_id not in ids):
                raise InvalidPacientID;
        except InvalidPacientID:
            print(f"{c.BRIGHTRED}ERROR: ID NO VÁLIDO{c.ENDC}");
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: SOLO VALORES NUMÉRICOS{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            bandera = False;
            return Paciente.mostrar_facturas_de_cliente(paciente_id);

def añadir_paciente():
    bandera:bool = True;
    while bandera:
        try:
            nombre = input(f"\t{c.BRIGHTGREEN}NOMBRE [-1 SALIR]: ");
            apellidos = input(f"\tAPELLIDOS: ");
            clientePreferencial = input(f"\t¿TRATO PREFERENCIAL? [S/N]: ")
            desc_dolencia = input(f"\tDESCRIPCIÓN DE LA DOLENCIA: ");
            desc_tratamiento = input(f"\tDESCRIPCIÓN DEL TRATAMIENTO: ");

            if (nombre == "-1"):
                return;

            if (not nombre.isalpha() and not apellidos.isalpha()):
                raise InvalidNameField;
            if (clientePreferencial != "S" and clientePreferencial !="N" and clientePreferencial != ""):
                raise ValueError;
            if (desc_dolencia.isdigit() or desc_tratamiento.isdigit()):
                raise InvalidDescField;
            if (len(nombre) == 0):
                raise InvalidCharField;
        except InvalidNameField:
            print(f"{c.BRIGHTRED}ERROR: CAMPOS NOMBRE Y APELLIDOS DEBEN DE SER ALFABÉTICOS{c.ENDC}");
        except InvalidDescField:
            print(f"{c.BRIGHTRED}ERROR: CAMPO(S) DESCRIPTIVOS NO VÁLIDOS{c.ENDC}");
        except InvalidCharField:
            print(f"{c.BRIGHTRED}ERROR: DEBES INTRODUCIR AL MENOS EL CAMPO 'NOMBRE'{c.ENDC}");
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: CAMPO NO VÁLIDO [S/N] SOLO{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            # Convertimos el valor de clientePreferencial a algo que pueda entender el metodo
            clientePreferencial = 1 if (clientePreferencial == "S") else 0;
            # Creamos el objeto de paciente para llamar al metodo de insertar (al ser un cliente nuevo, ni le pasamos el ID que será autoasignado ni la lista de facturas ya que no tiene)
            nuevo_paciente = Paciente(nombre=nombre, apellidos=apellidos, cliente_preferencial=clientePreferencial, desc_dolencia=desc_dolencia, desc_tratamiento=desc_tratamiento);
            # Ejecutamos el metodo para guardarlo en la DB (ya asignara a esta instancia el ID pertinente) | Devolvemos para mostrar un mensaje de si todo ha ido bien o no
            return nuevo_paciente.añadir_paciente();

def eliminar_paciente(ids):
    # La clase paciente tiene otro metodo para borrar por instancia pero creo que es más rápido así y se puede evitar la modificación de datos
    bandera:bool = True;
    while bandera:
        try:
            paciente_id = int(input(f"{c.BRIGHTGREEN}INTRODUZCA EL ID DEL PACIENTE QUE SERÁ DADO DE ALTA [-1 = SALIR]: "));
            if (paciente_id == -1):
                bandera = False;
                return;
            if (paciente_id not in ids):
                raise InvalidPacientID;
        except InvalidPacientID:
            print(f"{c.BRIGHTRED}ERROR: ID NO VÁLIDO{c.ENDC}");
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: SOLO VALORES NUMÉRICOS{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            confirmar_borrado = input(f"{c.BRIGHTRED}¿ESTÁ SEGURO QUE QUIERE BORRARLO? [S/N=ANY]: {c.BRIGHTGREEN}");
            if (confirmar_borrado == "S"):
                Paciente.eliminar_paciente_por_ID(paciente_id);
            else:
                return;

def modificar_paciente(ids):
    bandera:bool = True;
    while bandera:
        try:
            paciente_id = int(input(f"{c.BRIGHTGREEN}INTRODUZCA EL ID DEL PACIENTE A MODIFICAR [-1 = SALIR]: "));
            if (paciente_id == -1):
                return;
            if (paciente_id not in ids):
                raise InvalidPacientID;
        except InvalidPacientID:
            print(f"{c.BRIGHTRED}ERROR: ID NO VÁLIDO{c.ENDC}");
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: SOLO VALORES NUMÉRICOS{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            bandera = False;
            bandera2:bool = True;
            # Recogemos el paciente de la DB
            paciente = Paciente.recoger_paciente(paciente_id);
            # Obtenemos la modificación de los datos (vacio = dejarlo como está)
            print(f"{c.BRIGHTGREEN}MODIFIQUE LOS CAMPOS O DEJELOS VACÍOS PARA MANTENERLOS IGUAL")
            while bandera2:
                try:
                    nombre = input(f"\t{c.BRIGHTGREEN}NOMBRE ({paciente.nombre}) [-1 SALIR]: ");
                    apellidos = input(f"\tAPELLIDOS ({paciente.apellidos}): ");
                    clientePreferencial = input(f"\t¿TRATO PREFERENCIAL? [S/N] ({paciente.cliente_preferencial}): ")
                    desc_dolencia = input(f"\tDESCRIPCIÓN DE LA DOLENCIA ({paciente.desc_dolencia}): ");
                    desc_tratamiento = input(f"\tDESCRIPCIÓN DEL TRATAMIENTO ({paciente.desc_tratamiento}): ");

                    if (nombre == "-1"):
                        return;

                    if ((not nombre.isalpha() or not apellidos.isalpha()) and (nombre != "" and apellidos != "")):
                        raise InvalidNameField;
                    if (clientePreferencial != "S" and clientePreferencial !="N" and clientePreferencial != ""):
                        raise ValueError;
                    if (desc_dolencia.isdigit() or desc_tratamiento.isdigit()):
                        raise InvalidDescField;
                except InvalidNameField:
                    print(f"{c.BRIGHTRED}ERROR: CAMPOS NOMBRE Y APELLIDOS DEBEN DE SER ALFABÉTICOS{c.ENDC}");
                except InvalidDescField:
                    print(f"{c.BRIGHTRED}ERROR: CAMPO(S) DESCRIPTIVOS NO VÁLIDOS{c.ENDC}");
                except ValueError:
                    print(f"{c.BRIGHTRED}ERROR: CAMPO NO VÁLIDO [S/N] SOLO{c.ENDC}");
                except Exception as err:
                    print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
                else:
                    bandera2 = False;
                    # Si todo va bien, cambiamos los datos del paciente
                    if (len(nombre) != 0):
                        paciente.nombre = nombre;
                    if (len(apellidos) != 0):
                        paciente.apellidos = apellidos;
                    if (len(clientePreferencial) != 0):
                        paciente.cliente_preferencial = 1 if (clientePreferencial == "S") else 0;
                    if (len(desc_dolencia) != 0):
                        paciente.desc_dolencia = desc_dolencia;
                    if (len(desc_tratamiento) != 0):
                        paciente.desc_tratamiento = desc_tratamiento;
                    # Modificamos la DB con los datos cambiados
                    paciente.modificar_paciente();
