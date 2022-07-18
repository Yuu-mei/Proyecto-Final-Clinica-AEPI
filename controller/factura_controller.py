# No deberíamos improtar el modelo de Paciente aqui pero no me parecería correcto meter un retorno de IDs de Paciente en Factura
from models.factura import Factura;
from models.paciente import Paciente;
from auxiliary.colors import colors as c;
from auxiliary.custom_exceptions import InvalidBillID, InvalidPacientID;

def mostrar_facturas():
    return Factura.mostrar_facturas();

def actualizar_facturas():
    # Recuperamos los IDs que existen para saber si son modificables
    ids = Factura.devolver_ids_factura();

    bandera:bool = True;
    while bandera:
        try:
            factura_id = int(input(f"{c.BRIGHTGREEN}INTRODUZCA EL ID DE LA FACTURA A MODIFICAR [-1 SALIR]: "));
            if (factura_id == -1):
                return;
            if (factura_id not in ids):
                raise InvalidBillID;
        except InvalidBillID:
            print(f"{c.BRIGHTRED}ERROR: ID NO VÁLIDO{c.ENDC}");
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: SOLO VALORES NUMÉRICOS{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            bandera = False;
            bandera2:bool = True;
            while bandera2:
                try:
                    importe = float(input(f"\t{c.BRIGHTGREEN}NUEVO IMPORTE: "));
                    if (importe < 0):
                        raise ValueError;
                except ValueError:
                    print(f"{c.BRIGHTRED}ERROR: CAMPO NUMÉRICO NO VÁLIDO{c.ENDC}");
                except Exception as err:
                    print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
                else:
                    bandera2 = False;
                    # Si todo va bien, llamamos al metodo de modificación de la DB
                    Factura.modificar_factura_por_id(importe, factura_id);

def generar_facturas():
    # Recogemos los IDs disponibles de Pacientes para comprobar que el input es válido
    ids = Paciente.devolver_ids_paciente();
    bandera:bool = True;
    while bandera:
        try:
            id_paciente = int(input(f"\t{c.BRIGHTGREEN}ID PACIENTE [-1 SALIR]: "));
            importe = float(input(f"\tIMPORTE: "));

            if (id_paciente == -1):
                return;

            if (id_paciente not in ids):
                raise InvalidPacientID;
            if (importe < 0):
                raise ValueError;
        except InvalidPacientID:
            print(f"{c.BRIGHTRED}ERROR: ID DE PACIENTE NO ENCONTRADO EN LA DB{c.ENDC}");
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: CAMPO NUMÉRICO NO VÁLIDO{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            # También tengo un método para hacerlo por instancia, pero quiero hacerlo algo diferente a Paciente
            Factura.añadir_factura_por_campos(id_paciente, importe);
            return True;

def eliminar_facturas():
    # Recogemos las IDs primero para asegurarnos de que está
    ids = Factura.devolver_ids_factura();
    bandera:bool = True;
    while bandera:
        try:
            factura_id = int(input(f"{c.BRIGHTGREEN}INTRODUZCA EL ID DE LA FACTURA A ELIMINAR [-1 = SALIR]: "));
            if (factura_id == -1):
                bandera = False;
                return;
            if (factura_id not in ids):
                raise InvalidBillID;
        except InvalidBillID:
            print(f"{c.BRIGHTRED}ERROR: ID NO VÁLIDO{c.ENDC}");
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: SOLO VALORES NUMÉRICOS{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            confirmar_borrado = input(f"{c.BRIGHTRED}¿ESTÁ SEGURO QUE QUIERE BORRARLA? [S/N=ANY]: {c.BRIGHTGREEN}");
            if (confirmar_borrado == "S"):
                Factura.eliminar_factura_por_ID(factura_id);
            else:
                return;