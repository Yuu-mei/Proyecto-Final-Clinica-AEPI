import os;
import time
from auxiliary.colors import colors as c;
from controller import paciente_controller as pc;

def renderizar_gui():
    os.system('cls');
    print(f"{c.BRIGHTGREEN}");
    PATH = f"{os.path.dirname(__file__)}\estado_tripulacion.txt";
    try:
        fichero = open(PATH, "r", encoding="utf8");
    except FileNotFoundError:
        print(f"{c.BRIGHTRED}MAKE SURE THE PATH IS PROPERLY SET './estado_tripulacion.txt'{c.ENDC}");
    except Exception as err:
        print(f"{c.BRIGHTRED}UNHANDLED EXCEPTION: {err}{c.ENDC}");
    else:
        for linea in fichero:
            for char in linea:
                print(char, end="", flush=True);
            time.sleep(0.05);
    finally:
        fichero.close();

def estado_tripulacion_gui():
    renderizar_gui();
    bandera:bool = True;
    while bandera:
        try:
            eleccion = int(input(f"\n{c.GREEN}"));
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: COMANDO NO VÁLIDO{c.ENDC}");
        else:
            match eleccion:
                case 1: # Mostrar pacientes
                    __mostrar_pacientes();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 2: # Buscar pacientes
                    __buscar_pacientes();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 3: # Mostrar las facturas de un paciente
                    __mostrar_facturas();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 4: # Dar de alta a un paciente (eliminar)
                    __eliminar_paciente();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 5: # Actualizar datos de un paciente
                    __actualizar_datos_paciente();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 6: # Ingresar paciente (Crear paciente)
                    __añadir_paciente();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 7: # Volver al menu
                    bandera = False;
                    return;
                case _:
                    print(f"{c.BRIGHTRED}ERROR: COMANDO NO VÁLIDO{c.ENDC}");

# Metodo privado porque solo quiero que accedas desde este menu (.py)
def __mostrar_pacientes():
    # Se que estoy repitiendo codigo pero no me atrevo a hacer una funcion fuera debido a los problemas que tengo ya con las importaciones y los paths relativos
    os.system('cls');
    print(f"{c.BRIGHTGREEN}");
    PATH = f"{os.path.dirname(__file__)}\mostrar_pacientes.txt";
    try:
        fichero = open(PATH, "r", encoding="utf8");
    except FileNotFoundError:
        print(f"{c.BRIGHTRED}MAKE SURE THE PATH IS PROPERLY SET './mostrar_pacientes.txt'{c.ENDC}");
    except Exception as err:
        print(f"{c.BRIGHTRED}UNHANDLED EXCEPTION: {err}{c.ENDC}");
    else:
        for linea in fichero:
            for char in linea:
                print(char, end="", flush=True);
            time.sleep(0.05);
        # Llamamos al controller para recoger la data e irla representando
        pacientes_dict:dict = pc.mostrar_pacientes();
        # Esta tabulacion esta hecha para rellenar huecos en caso necesario (igual deberia haber usado una libreria para tablas pero no se si esta permitido)
        tab = "\t\t"
        # Este diccionario funciona como si fuera un json de ahí a que tenga una key dentro de una key
        for key, val in pacientes_dict.items():
            print(f"\t{key}", end="\t\t", flush=True);
            for inside_key, inside_val in val.items():
                print(f"{inside_val if len(str(inside_val)) > 0 else tab}", end="\t\t  ", flush=True);
                time.sleep(0.05);
            print(flush=True);
            time.sleep(0.05);
        # Aunque se descoloque la tabla un poco, creo que es entendible y asi la voy a dejar cerrada
        print("""│                                                                                                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘""");
        # Retorno las keys para que pueda usarlas en el metodo de mostrar facturas
        return pacientes_dict.keys();

def __buscar_pacientes():
    # Limpiamos la pantalla y printeamos la GUI
    os.system('cls');

    print(f"""{c.BRIGHTGREEN}┌───────────────────────────────────────────────────────────┐
│                                                           │""");

    # Llamamos al metodo del controller para retornar el paciente y recogemos los datos para representarlos
    pacientes_dict:dict = pc.buscar_pacientes();
    
    # Mostramos que no hay resultados y volvemos al menu
    if (len(pacientes_dict)==0):
        os.system('cls');
        print(f"{c.BRIGHTRED}NO SE HAN ENCONTRADO PACIENTES BAJO ESAS CARACTERÍSTICAS.\nVOLVIENDO AL MENÚ...{c.BRIGHTGREEN}");
        return;
    print("""│                                                           │
└───────────────────────────────────────────────────────────┘""");

    # Printeamos la GUI para los pacientes si hay data
    os.system('cls');
    print(f"{c.BRIGHTGREEN}");
    PATH = f"{os.path.dirname(__file__)}\mostrar_pacientes.txt";
    try:
        fichero = open(PATH, "r", encoding="utf8");
    except FileNotFoundError:
        print(f"{c.BRIGHTRED}MAKE SURE THE PATH IS PROPERLY SET './mostrar_pacientes.txt'{c.ENDC}");
    except Exception as err:
        print(f"{c.BRIGHTRED}UNHANDLED EXCEPTION: {err}{c.ENDC}");
    else:
        for linea in fichero:
            for char in linea:
                print(char, end="", flush=True);
            time.sleep(0.05);
        # Finalmente manipulamos el dict para mostrar la data
        for key, val in pacientes_dict.items():
            print(f"\t{key}", end="\t\t", flush=True);
            for inside_key, inside_val in val.items():
                print(f"{inside_val}", end="\t\t  ", flush=True);
                time.sleep(0.05);
            print(flush=True);
            time.sleep(0.05);
        # Aunque se descoloque la tabla un poco, creo que es entendible y asi la voy a dejar cerrada
        print("""│                                                                                                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘""");

def __mostrar_facturas():
    # Primero vamos a mostrar todos los pacientes para que le sea mas fácil elegir al usuario y recogemos que IDs hay
    ids = __mostrar_pacientes();
    # Llamamos al controller para que haga sus operaciones pasandole las IDs existentes y recogemos la data
    facturas = pc.mostrar_facturas(ids);

    # Comprobamos que el paciente tenga facturas
    if (len(facturas) == 0):
        os.system('cls');
        print(f"{c.BRIGHTRED}ESE PACIENTE NO TIENE FACTURAS.\nVOLVIENDO AL MENÚ...{c.BRIGHTGREEN}");
        time.sleep(1);
        return;

    # Printeamos la data
    os.system('cls');
    print(f"{c.BRIGHTGREEN}");
    PATH = f"{os.path.dirname(__file__)}\mostrar_facturas.txt";
    try:
        fichero = open(PATH, "r", encoding="utf8");
    except FileNotFoundError:
        print(f"{c.BRIGHTRED}MAKE SURE THE PATH IS PROPERLY SET './mostrar_facturas.txt'{c.ENDC}");
    except Exception as err:
        print(f"{c.BRIGHTRED}UNHANDLED EXCEPTION: {err}{c.ENDC}");
    else:
        for linea in fichero:
            for char in linea:
                print(char, end="", flush=True);
            time.sleep(0.05);
        # Finalmente manipulamos el dict para mostrar la data
        for lista in facturas:
            for val in lista:
                print(f"\t{val}", end="\t", flush=True);
                time.sleep(0.05);
            print();
            time.sleep(0.05);
        # Aunque se descoloque la tabla un poco, creo que es entendible y asi la voy a dejar cerrada
        print("""│                                                           │
└───────────────────────────────────────────────────────────┘""");

def __añadir_paciente():
    # Limpiamos la pantalla y empezamos a dibujar la GUI
    os.system('cls');
    print(f"""{c.BRIGHTGREEN}┌───────────────────────────────────────────────────────────┐
│                                                           │""");
    # Llamamos al metodo del controller para recoger datos y asegurarnos de que los campos sean validos
    añadido_satisfactoriamente = pc.añadir_paciente();
    if(añadido_satisfactoriamente):
        print(f"\n\n{c.BRIGHTGREEN}PACIENTE AÑADIDO A LA DB");
    else:
        print(f"\n\n{c.BRIGHTRED}ERROR AL AÑADIR EL PACIENTE. CONTACTE CON SU ADMINISTRADOR{c.BRIGHTGREEN}");
    print("""│                                                           │
└───────────────────────────────────────────────────────────┘""");

def __eliminar_paciente():
    # Primero mostramos los pacientes para que puedan elegir uno y almacenamos las posibles opciones
    ids = __mostrar_pacientes();
    # Llamamos al metodo del controlador para realizar las operaciones
    pc.eliminar_paciente(ids);

def __actualizar_datos_paciente():
    # Primero mostramos los pacientes para que puedan elegir uno y almacenamos las posibles opciones
    ids = __mostrar_pacientes();
    # Llamamos al metodo del controlador para realizar las operaciones
    pc.modificar_paciente(ids);