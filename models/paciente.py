from mysql.connector import connection, errorcode;
import mysql.connector;
from auxiliary.colors import colors as c;
from .factura import Factura;

class Paciente():
    """
    Modelo para Paciente
    Parámetros: nombre (str - required) | idPaciente (int) | apellidos (str) |
    cliente_preferencial (bool) | desc_dolencia (str) | desc_tratamiento (str) | facturas (list[Factura] - unused)
    Métodos mágicos: __str__ (devuelve nombre+apellidos)
    Métodos: 
    """
    def __init__(self, nombre:str, idPaciente:int="", apellidos:str="", 
    cliente_preferencial:bool|int=False, desc_dolencia:str="", desc_tratamiento:str="", facturas:list[Factura]=[]) -> None:
        self.nombre = nombre;
        self.idPaciente = idPaciente;
        self.apellidos = apellidos;
        self.cliente_preferencial = cliente_preferencial;
        self.desc_dolencia = desc_dolencia;
        self.desc_tratamiento = desc_tratamiento;
        self.facturas = facturas;

    #region Métodos mágicos
    def __str__(self) -> str:
        return f"{c.BRIGHTGREEN}NOMBRE COMPLETO DEL PACIENTE: {self.nombre} {self.apellidos}{c.ENDC}";
    #endregion

    #region Metodos
    # Metodo de instancia ya que lo usaremos para guardar la info de un nuevo paciente en un objeto
    def añadir_paciente(self):
        """
        Método que añade un paciente a la base de datos segun la instancia creada
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y commitearla
            cursor = db.cursor();
            # Usamos scaped values para evitar SQL Injection
            insert_sql = "INSERT INTO paciente (nombre, apellidos, clientePreferencial, desc_dolencia, desc_tratamiento) VALUES (%s, %s, %s, %s, %s);"
            vals = (self.nombre, self.apellidos, self.cliente_preferencial, self.desc_dolencia, self.desc_tratamiento);
            cursor.execute(insert_sql, vals);
            db.commit();

            # Recogemos el ID para asignarselo a la instancia en caso de que queramos luego borrar por instancia y no por ID
            select_sql = "SELECT idPaciente FROM paciente WHERE nombre=%s AND apellidos=%s AND clientePreferencial = %s AND desc_dolencia = %s AND desc_tratamiento = %s"
            cursor.execute(select_sql, vals);
            id_result = cursor.fetchone();
            self.idPaciente = id_result[0];

            # Creamos una factura en la otra tabla vacia, que posteriormente podremos modificar (lo hago debido a que para mostrar los pacientes lo hago según tengan un join a la factura)
            insert_sql = "INSERT INTO factura (idPaciente, importe) VALUES (%s,%s)";
            vals = (self.idPaciente, 0);
            cursor.execute(insert_sql, vals);
            db.commit();

            # Añadimos la factura inicial a la lista de facturas de la instancia
            select_factura_sql = "SELECT idFactura, importe FROM factura as f INNER JOIN paciente as p ON %s = p.idPaciente";
            vals = (self.idPaciente,);
            cursor.execute(select_factura_sql, vals);
            factura = cursor.fetchone();
            self.facturas.append(factura);

            db.close();
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            elif (err.errno == errorcode.ER_WARN_DATA_OUT_OF_RANGE):
                print(f"{c.BRIGHTRED}ERROR: ALGÚN PARÁMETRO SE SALE DEL RANGO ACEPTABLE{c.ENDC}");
            elif (err.errno == errorcode.ER_DATA_TOO_LONG):
                print(f"{c.BRIGHTRED}ERROR: LA LONGITUD DE ALGÚN PARÁMETRO ES DEMASIADO LARGO{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        else:
            return True;

    
    # Recoger paciente segun ID pasada para los metodos de instancia
    @classmethod
    def recoger_paciente(cls, paciente_id:int):
        """
        Método que dada una ID pasada devuelve una instancia de la clase para poder operar sobre los métodos de instancia
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL de busqueda y retornar la info necesaria
            cursor = db.cursor();
            select_sql = "SELECT * FROM paciente WHERE idPaciente=%s"
            vals = (paciente_id,)
            cursor.execute(select_sql, vals);
            # Recogemos los datos del paciente
            datos_paciente = cursor.fetchall();

            # Traemos de vuelta todas las facturas del paciente para añadirlas a la instancia
            select_factura_sql = "SELECT idFactura, importe FROM factura as f INNER JOIN paciente as p ON f.idPaciente = p.idPaciente WHERE f.idPaciente = %s";
            vals = (paciente_id,);
            cursor.execute(select_factura_sql, vals);
            facturas = cursor.fetchall();

            # Creamos un objeto de factura por cada factura que venga y se lo añadimos a la lista
            lista_facturas:list[Factura] = [];

            for factura_vals in facturas:
                factura = Factura(paciente_id, factura_vals[0], factura_vals[1]);
                lista_facturas.append(factura);

            # Finalmente cerramos la DB
            db.close();
            # Creamos la instancia con estos datos y la retornamos
            paciente = Paciente(nombre=datos_paciente[0][1], idPaciente=datos_paciente[0][0], apellidos=datos_paciente[0][2], cliente_preferencial=datos_paciente[0][3], desc_dolencia=datos_paciente[0][4], desc_tratamiento=datos_paciente[0][5], facturas=lista_facturas);

            return paciente;
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            elif (err.errno == errorcode.ER_WARN_DATA_OUT_OF_RANGE):
                print(f"{c.BRIGHTRED}ERROR: ALGÚN PARÁMETRO SE SALE DEL RANGO ACEPTABLE{c.ENDC}");
            elif (err.errno == errorcode.ER_DATA_TOO_LONG):
                print(f"{c.BRIGHTRED}ERROR: LA LONGITUD DE ALGÚN PARÁMETRO ES DEMASIADO LARGO{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    # Modificamos el paciente con los datos de una instancia en la DB (creo que sería mejor si fuera un método de clase al que se le pasa una ID a modificar)
    def modificar_paciente(self):
        """
        Método que modifica un paciente segun la instancia creada
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y updatear
            cursor = db.cursor();
            update_sql = "UPDATE paciente SET nombre=%s, apellidos=%s, clientePreferencial=%s, desc_dolencia=%s, desc_tratamiento=%s WHERE idPaciente = %s";
            vals = (self.nombre, self.apellidos, self.cliente_preferencial, self.desc_dolencia, self.desc_tratamiento, self.idPaciente);
            cursor.execute(update_sql, vals);
            db.commit();

            db.close();
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            elif (err.errno == errorcode.ER_WARN_DATA_OUT_OF_RANGE):
                print(f"{c.BRIGHTRED}ERROR: ALGÚN PARÁMETRO SE SALE DEL RANGO ACEPTABLE{c.ENDC}");
            elif (err.errno == errorcode.ER_DATA_TOO_LONG):
                print(f"{c.BRIGHTRED}ERROR: LA LONGITUD DE ALGÚN PARÁMETRO ES DEMASIADO LARGO{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    # Metodo de clase ya que es independiente de cada objeto
    @classmethod
    def mostrar_pacientes(cls):
        """
        Método de clase que muestra los pacientes
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y obtener la data
            cursor = db.cursor();
            select_sql = "SELECT p.*, sum(DISTINCT(importe)) FROM paciente as p INNER JOIN factura as f ON f.idPaciente = p.idPaciente GROUP BY p.idPaciente;";
            cursor.execute(select_sql);
            pacientes = cursor.fetchall();

            # Creamos un diccionario para cada paciente
            pacientes_dict:dict = {};

            # Vamos de fila en fila y añadimos la data al diccionario
            for paciente in pacientes:
                pacientes_dict[paciente[0]] = {
                    "nombre": paciente[1],
                    "apellidos": paciente[2],
                    "clientePreferencial": "S" if (paciente[3] == 1) else "N",
                    "desc_dolencia": paciente[4],
                    "desc_tratamiento": paciente[5],
                    "facturas": paciente[6],
                }

            db.close();

            return pacientes_dict;
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    # Metodo de clase ya que es independiente de cada objeto
    @classmethod
    def mostrar_pacientes_por_campo(cls, **kwargs):
        """
        Método que muestra un paciente según el parámetro dado (se puede sustituir el kwargs por los parametros per se pero esta pensado para multiples usos)
        """
        parametros_validos:tuple = ("nombre", "apellidos", "clientePreferencial", "desc_dolencia", "desc_tratamiento");
        for key in kwargs.keys():
            if (key not in parametros_validos):
                print(f"{c.BRIGHTRED} ERROR: PARÁMETRO '{key}' NO VÁLIDO{c.ENDC}");
                return;
        else:
            try:
                db = connection.MySQLConnection(user='root', password='root',
                host='127.0.0.1', database='clinica');

                # Creamos el cursor para ejecutar la secuencia SQL y obtener la data
                cursor = db.cursor();

                # Sentencia que iremos construyendo poco a poco en el bucle por si nos pasan mas de un parámetro de búsqueda
                select_sql = "SELECT p.*,  sum(DISTINCT(importe)) FROM paciente as p INNER JOIN factura as f ON f.idPaciente = p.idPaciente WHERE ";

                for i, (key, val) in enumerate(kwargs.items()):
                    # Uso un LIKE porque vale incluso para los bools y así la persona que use el programa no tiene que acordarse de todo a pies juntillas
                    select_sql += f"p.{key} LIKE '{val}%'";
                    if (len(kwargs.items()) > 1 and i < len(kwargs.items())-1):
                        select_sql += " AND ";

                select_sql += "GROUP BY p.idPaciente;";
                # En este caso al no pasarle los vals de una manera especifica es posible que ocurran SQL Injections pero no estoy completamente seguro de como evitarlo con una sentencia que construyes poco a poco
                cursor.execute(select_sql);
                pacientes = cursor.fetchall();

                # Creamos un diccionario para cada paciente
                pacientes_dict:dict = {};

                # Vamos de fila en fila y añadimos la data al diccionario
                for paciente in pacientes:
                    pacientes_dict[paciente[0]] = {
                        "nombre": paciente[1],
                        "apellidos": paciente[2],
                        "clientePreferencial": "S" if (paciente[3] == 1) else "N",
                        "desc_dolencia": paciente[4],
                        "desc_tratamiento": paciente[5],
                        "facturas": paciente[6],
                    }

                db.close();

                return pacientes_dict;
            except mysql.connector.Error as err:
                if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                    print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
                elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                    print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
                else:
                    print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
            except Exception as err:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    @classmethod
    def mostrar_facturas_de_cliente(cls, idPaciente:int):
        """
        Metodo para mostrar las facturas de un cliente especifico
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y obtener la data
            cursor = db.cursor();

            # Intentamos recuperar datos de facturas si existen
            select_sql_facturas = "SELECT idPaciente, idFactura, importe FROM factura WHERE idPaciente = %s;";
            vals = (idPaciente,);
            cursor.execute(select_sql_facturas, vals);
            facturas = cursor.fetchall();

            return facturas;
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    # Eliminar paciente por instancia (NO USADO)
    def eliminar_paciente(self):
        """
        Método que elimina un paciente segun la ID de la instancia del Paciente
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y borramos en ambas tablas
            cursor = db.cursor();

            # Primero borramos de la tabla factura para evitar problemas
            delete_factura_sql = "DELETE FROM factura WHERE idPaciente = %s";
            vals = (self.idPaciente,);
            cursor.execute(delete_factura_sql, vals);
            db.commit();
            # Luego borramos el paciente
            # PD: Juraria que tambien se podria hacer con JOIN pero prefiero tenerlo separado por si acaso sale mal en alguna de las dos
            delete_paciente_sql = "DELETE FROM paciente WHERE idPaciente = %s";
            vals = (self.idPaciente,);
            cursor.execute(delete_paciente_sql, vals);
            db.commit();

            db.close();
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            elif (err.errno == errorcode.ER_WARN_DATA_OUT_OF_RANGE):
                print(f"{c.BRIGHTRED}ERROR: ALGÚN PARÁMETRO SE SALE DEL RANGO ACEPTABLE{c.ENDC}");
            elif (err.errno == errorcode.ER_DATA_TOO_LONG):
                print(f"{c.BRIGHTRED}ERROR: LA LONGITUD DE ALGÚN PARÁMETRO ES DEMASIADO LARGO{c.ENDC}");
            elif (err.errno == errorcode.ER_ROW_IS_REFERENCED_2):
                print(f"{c.BRIGHTRED}ERROR: EL ID DEL PACIENTE ESTA REFERENCIADO EN OTRA TABLA{c.ENDC}");
            elif (err.errno == errorcode.ER_PARSE_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA SENTENCIA SQL NO ES CORRECTA{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    @classmethod
    def eliminar_paciente_por_ID(cls, paciente_id:int):
        """
        Método que elimina un paciente dada una ID
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y borramos en ambas tablas
            cursor = db.cursor();
            # Primero borramos de la tabla factura para evitar problemas
            delete_factura_sql = "DELETE FROM factura WHERE idPaciente = %s";
            vals = (paciente_id,);
            cursor.execute(delete_factura_sql, vals);
            db.commit();
            # Luego borramos el paciente
            # PD: Juraria que tambien se podria hacer con JOIN pero prefiero tenerlo separado por si acaso sale mal en alguna de las dos
            delete_paciente_sql = "DELETE FROM paciente WHERE idPaciente = %s";
            vals = (paciente_id,);
            cursor.execute(delete_paciente_sql, vals);
            db.commit();

            db.close();
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            elif (err.errno == errorcode.ER_WARN_DATA_OUT_OF_RANGE):
                print(f"{c.BRIGHTRED}ERROR: ALGÚN PARÁMETRO SE SALE DEL RANGO ACEPTABLE{c.ENDC}");
            elif (err.errno == errorcode.ER_DATA_TOO_LONG):
                print(f"{c.BRIGHTRED}ERROR: LA LONGITUD DE ALGÚN PARÁMETRO ES DEMASIADO LARGO{c.ENDC}");
            elif (err.errno == errorcode.ER_ROW_IS_REFERENCED_2):
                print(f"{c.BRIGHTRED}ERROR: EL ID DEL PACIENTE ESTA REFERENCIADO EN OTRA TABLA{c.ENDC}");
            elif (err.errno == errorcode.ER_PARSE_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA SENTENCIA SQL NO ES CORRECTA{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    @classmethod
    def devolver_ids_paciente(cls):
        """
        Método de clase que devuelve las ids con tal de poder comprobar si el ID introducido es parte de la base de datos o no
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y obtener la data
            cursor = db.cursor();

            # Intentamos recuperar datos de pacientes si existen
            select_sql_paciente = "SELECT idPaciente FROM paciente";
            cursor.execute(select_sql_paciente);
            id_pacientes = cursor.fetchall();

            # Crear lista para que sea mas facil de manipular
            lista_id_pacientes:list = [];

            for id_paciente in id_pacientes:
                lista_id_pacientes.append(id_paciente[0]);

            db.close();

            return tuple(lista_id_pacientes);
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
    #endregion