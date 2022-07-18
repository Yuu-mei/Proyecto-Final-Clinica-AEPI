import os;
import time
from auxiliary.colors import colors as c;
from controller import factura_controller as fc;

def renderizar_gui():
    os.system('cls');
    print(f"{c.BRIGHTGREEN}");
    PATH = f"{os.path.dirname(__file__)}\menu_facturas.txt";
    try:
        fichero = open(PATH, "r", encoding="utf8");
    except FileNotFoundError:
        print(f"{c.BRIGHTRED}MAKE SURE THE PATH IS PROPERLY SET './menu_facturas.txt'{c.ENDC}");
    except Exception as err:
        print(f"{c.BRIGHTRED}UNHANDLED EXCEPTION: {err}{c.ENDC}");
    else:
        for linea in fichero:
            for char in linea:
                print(char, end="", flush=True);
            time.sleep(0.05);
    finally:
        fichero.close();

def menu_facturas_gui():
    renderizar_gui();
    bandera:bool = True;
    while bandera:
        try:
            eleccion = int(input(f"\n{c.GREEN}"));
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: COMANDO NO VÁLIDO{c.ENDC}");
        else:
            match eleccion:
                case 1: # Mostrar facturas
                    __mostrar_facturas();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 2: # Actualizar facturas
                    __actualizar_facturas();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 3: # Generar facturas
                    __generar_facturas();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 4: # Eliminar facturas
                    __eliminar_facturas();
                    input(f"{c.BRIGHTGREEN}PRESIONE 'ENTER' PARA VOLVER AL MENU ANTERIOR{c.ENDC}");
                    renderizar_gui();
                case 5: # Volver al menu
                    bandera = False;
                    return;
                case _:
                    print(f"{c.BRIGHTRED}ERROR: COMANDO NO VÁLIDO{c.ENDC}");

def __mostrar_facturas():
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
        # Llamamos al controller para recoger la data e irla representando
        facturas_list:list = fc.mostrar_facturas();

        for factura in facturas_list:
            for val in factura:
                print(f"\t{val}", end="\t", flush=True);
                time.sleep(0.05);
            print(flush=True);
            time.sleep(0.05);
        print("""│                                                           │
└───────────────────────────────────────────────────────────┘""");

def __actualizar_facturas():
    # Mostramos primero la lista de facturas para que el usuario sepa cual modificar
    __mostrar_facturas();

    # Llamamos al metodo del controller para realizar las comprobaciones y cambios pertinentes
    fc.actualizar_facturas();

def __generar_facturas():
    # Limpiamos la pantalla y empezamos a dibujar la GUI
    os.system('cls');
    print(f"""{c.BRIGHTGREEN}┌───────────────────────────────────────────────────────────┐
│                                                           │""");
    # Llamamos al metodo del controller para recoger datos y asegurarnos de que los campos sean validos
    añadido_satisfactoriamente = fc.generar_facturas();
    if(añadido_satisfactoriamente):
        print(f"\n\n\t{c.BRIGHTGREEN}FACTURA AÑADIDA A LA DB");
    else:
        print(f"\n\n\t{c.BRIGHTRED}ERROR AL AÑADIR LA FACTURA. CONTACTE CON SU ADMINISTRADOR{c.BRIGHTGREEN}");
    print("""│                                                           │
└───────────────────────────────────────────────────────────┘""");

def __eliminar_facturas():
    # Mostramos primero la lista de facturas para que el usuario sepa cual modificar
    __mostrar_facturas();
    # Llamamos al metodo para realizar las operaciones pertinentes
    fc.eliminar_facturas();