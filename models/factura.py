from mysql.connector import connection, errorcode;
import mysql.connector;
from auxiliary import colors as c;

class Factura():
    """
    Modelo para Factura
    Parámetros: idPaciente (int - required - FK de Paciente) | idFactura (int) |
    importe (float)
    Métodos: 
    """
    def __init__(self, idPaciente:int, idFactura:int=0, importe:float=0.0) -> None:
        self.idFactura = idFactura;
        self.idPaciente = idPaciente;
        self.importe = importe;

    #region Metodos
    # NO USADO (A diferencia de Paciente prefiero hacer casi todo con classmethod aqui para cambiar un poco)
    def añadir_factura(self):
        """
        Método que añade una factura a la base de datos segun la instancia creada
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y commitearla
            cursor = db.cursor();
            # Usamos scaped values para evitar SQL Injection
            insert_sql = "INSERT INTO factura (idPaciente, importe) VALUES (%s, %s);"
            vals = (self.idPaciente, self.importe);
            cursor.execute(insert_sql, vals);
            db.commit();

            # Recogemos el ID para asignarselo a la instancia en caso de que queramos luego borrar por instancia y no por ID
            select_sql = "SELECT idFactura FROM factura WHERE idPaciente=%s AND importe=%s"
            cursor.execute(select_sql, vals);
            id_result = cursor.fetchone();
            self.idFactura = id_result[0];

            db.close();
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
    def añadir_factura_por_campos(cls, id_paciente:int, importe:float):
        """
        Método que añade una factura a la base de datos segun los parámetros IDPaciente e Importe
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y commitearla
            cursor = db.cursor();
            # Usamos scaped values para evitar SQL Injection
            insert_sql = "INSERT INTO factura (idPaciente, importe) VALUES (%s, %s);"
            vals = (id_paciente, importe);
            cursor.execute(insert_sql, vals);
            db.commit();

            db.close();
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    # NO USADO (A diferencia de Paciente, en Facturas lo he hecho desde la clase per se y no desde una instancia)
    def modificar_factura(self):
        """
        Método que modifica una factura segun la instancia creada (utilizando o bien el idPaciente o bien idFactura)
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y updatear
            cursor = db.cursor();
            update_sql = "UPDATE factura SET importe=%s WHERE idPaciente = %s OR idFactura = %s";
            vals = (self.importe, self.idPaciente, self.idFactura);
            cursor.execute(update_sql, vals);
            db.commit();

            db.close();
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
    def modificar_factura_por_id(cls, new_importe:float, factura_id:int):
        """
        Método que modifica una factura segun la ID pasada
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y updatear
            cursor = db.cursor();
            update_sql = "UPDATE factura SET importe=%s WHERE idFactura = %s";
            vals = (new_importe, factura_id);
            cursor.execute(update_sql, vals);
            db.commit();

            db.close();
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    # NO USADO
    def asignar_factura_a_cliente(self):
        """
        Método que modifica una factura de un cliente segun la instancia creada (utilizando el idFactura)
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y updatear
            cursor = db.cursor();
            update_sql = "UPDATE factura SET idPaciente='%s' WHERE idFactura = %s";
            vals = (self.idPaciente, self.idFactura);
            cursor.execute(update_sql, vals);
            db.commit();

            db.close();
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");

    # NO USADO
    def eliminar_factura(self):
        """
        Método que elimina una factura segun la ID de la instancia de la Factura
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y updatear
            cursor = db.cursor();
            delete_sql = "DELETE FROM factura WHERE idFactura = %s";
            vals = (self.idFactura,);
            cursor.execute(delete_sql, vals);
            db.commit();

            db.close();
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
    def eliminar_factura_por_ID(cls, factura_id:int):
        """
        Método de clase que elimina una factura segun el ID que le pases
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y updatear
            cursor = db.cursor();
            delete_sql = "DELETE FROM factura WHERE idFactura = %s";
            vals = (factura_id,);
            cursor.execute(delete_sql, vals);
            db.commit();

            db.close();
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
    def mostrar_facturas(cls):
        """
        Método de clase que muestra la información de las facturas
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y obtener la data
            cursor = db.cursor();

            # Intentamos recuperar datos de facturas si existen
            select_sql_facturas = "SELECT f.idPaciente, f.idFactura, importe FROM factura as f INNER JOIN paciente as p ON f.idPaciente = p.idPaciente";
            cursor.execute(select_sql_facturas);
            facturas = cursor.fetchall();

            db.close();

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

    @classmethod
    def devolver_ids_factura(cls):
        """
        Método de clase que devuelve las ids con tal de poder comprobar si el ID introducido es parte de la base de datos o no (diferente forma a la que hago en pacientes)
        """
        try:
            db = connection.MySQLConnection(user='root', password='root',
            host='127.0.0.1', database='clinica');

            # Creamos el cursor para ejecutar la secuencia SQL y obtener la data
            cursor = db.cursor();

            # Intentamos recuperar datos de facturas si existen
            select_sql_facturas = "SELECT idFactura FROM factura";
            cursor.execute(select_sql_facturas);
            id_facturas = cursor.fetchall();

            # Crear lista para que sea mas facil de manipular
            lista_id_facturas:list = [];

            for id_factura in id_facturas:
                lista_id_facturas.append(id_factura[0]);

            db.close();

            return tuple(lista_id_facturas);
        except mysql.connector.Error as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print(f"{c.BRIGHTRED}ACCESO DENEGADO: INSUFICIENTES PERMISOS{c.ENDC}");
            elif (err.errno == errorcode.ER_BAD_DB_ERROR):
                print(f"{c.BRIGHTRED}ERROR: LA DB NO EXISTE{c.ENDC}");
            else:
                print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");
        except Exception as err:
            print(f"{c.BRIGHTRED}UNHANDLED ERROR: {err}{c.ENDC}");