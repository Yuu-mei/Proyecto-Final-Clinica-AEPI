import os;
import time;
from auxiliary.colors import colors as c;
from views import estado_instalacion, estado_tripulacion, menu_facturas;

def renderizar_gui():
    os.system('cls');
    print(f"{c.BRIGHTGREEN}");
    PATH = f"{os.path.dirname(__file__)}\main_menu.txt";
    try:
        fichero = open(PATH, "r", encoding="utf8");
    except FileNotFoundError:
        print(f"{c.BRIGHTRED}MAKE SURE THE PATH IS PROPERLY SET './main_menu.txt'{c.ENDC}");
    except Exception as err:
        print(f"{c.BRIGHTRED}UNHANDLED EXCEPTION: {err}{c.ENDC}");
    else:
        for linea in fichero:
            for char in linea:
                print(char, end="", flush=True);
            time.sleep(0.05);
    finally:
        fichero.close();


# En caso de que alguien diga algo del copyright voy a protegerme bajo el Fair Use
def main_menu_gui():
    renderizar_gui();
    bandera:bool = True;
    while bandera:
        try:
            eleccion = int(input(f"\n{c.GREEN}"));
        except ValueError:
            print(f"{c.BRIGHTRED}ERROR: COMANDO NO VÁLIDO{c.ENDC}");
        else:
            match eleccion:
                case 1:
                    estado_instalacion.estado_instalacion_gui();
                    renderizar_gui();
                case 2:
                    estado_tripulacion.estado_tripulacion_gui();
                    renderizar_gui();
                case 3:
                    menu_facturas.menu_facturas_gui();
                    renderizar_gui();
                case 4:
                    print(f"{c.ENDC}");
                    quit();
                case _:
                    print(f"{c.BRIGHTRED}ERROR: COMANDO NO VÁLIDO{c.ENDC}");
        print(f"{c.ENDC}");