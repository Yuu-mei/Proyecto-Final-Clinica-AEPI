import os;
import time;
from auxiliary.colors import colors as c;

def estado_instalacion_gui():
    os.system('cls');
    print(f"{c.BRIGHTGREEN}");
    PATH = f"{os.path.dirname(__file__)}\estado_instalacion.txt";
    try:
        fichero = open(PATH, "r", encoding="utf8");
    except FileNotFoundError:
        print(f"{c.BRIGHTRED}MAKE SURE THE PATH IS PROPERLY SET './estado_instalacion.txt'{c.ENDC}");
    except Exception as err:
        print(f"{c.BRIGHTRED}UNHANDLED EXCEPTION: {err}{c.ENDC}");
    else:
        for linea in fichero:
            for char in linea:
                print(char, end="", flush=True);
            time.sleep(0.05);
    finally:
        fichero.close();
        bandera:bool = True;
        while bandera:
            try:
                eleccion = int(input(f"\n{c.GREEN}"));
            except ValueError:
                print(f"{c.BRIGHTRED}ERROR: COMANDO NO VÁLIDO{c.ENDC}");
            else:
                match eleccion:
                    case 1:
                        bandera = False;
                        return;
                    case _:
                        print(f"{c.BRIGHTRED}ERROR: COMANDO NO VÁLIDO{c.ENDC}");