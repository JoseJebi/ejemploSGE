from contextlib import nullcontext
from datetime import datetime

import pandas as pd

from Administrador import Administrador
from Constantes import QUERY_CLIENTES_ACTIVOS, QUERY_VUELOS_BY_PASAJERO, QUERY_DIRECCION_BY_PASAJERO, QUERY_VUELOS, \
    QUERY_PASAJEROS_BY_VUELO, QUERY_UPDATE_PASAJEROS, UPDATE_PASAJEROS_MUERTOS, UPDATE_VUELO
from Empleados import Empleados
from Log import escribirError, msjPermisos, msjConsulta1, msjConsulta3, msjConsulta2, escribirInfo, msjUpdate, msjMenu, \
    errDato, errUserPermisos, errUserNull
from Recepcionista import Recepcionista
from db import PostgreSQLConnection


def menu():
    empleados = Empleados()
    empleados.empleados.append(Administrador("Admin", "admin@admin.com", 0))
    empleados.empleados.append(Recepcionista("Recepcionista", "recep@gmail.com", 0))

    while True:
        print("\n--- MENÚ ---")
        print("1. Mostrar los vuelos de un cliente")
        print("2. Mostrar la dirección de un usuario")
        print("3. Vuelo de los pasajeros")
        print("4. Actualización de muertos")
        print("5. Salir")
        while True:
            try:
                opcion = int(input("Opcion elegida: "))
                break
            except ValueError:
                escribirError(msjMenu, errDato)
                print("Opcion no valida")
        if opcion == 1:
            user = comprobar_usuario(empleados.empleados)
            if user != None :
                if isinstance(user, Recepcionista):
                    mostrar_vuelos()
                    user.num_consultas += 1
                    escribirInfo(msjConsulta1)
                else:
                    escribirError(msjPermisos, errUserNull)
                    print("Usuario invalido")
            else:
                escribirError(msjPermisos, errUserPermisos)
                print("El usuario no existe")
        elif opcion == 2:
            user = comprobar_usuario(empleados.empleados)
            if user != None:
                if isinstance(user, Recepcionista):
                    mostrar_direccion()
                    user.num_consultas += 1
                    escribirInfo(msjConsulta2)
                else:
                    escribirError(msjPermisos, errUserNull)
                    print("Usuario invalido")
            else:
                escribirError(msjPermisos, errUserPermisos)
                print("El usuario no existe")

        elif opcion == 3:
            user = comprobar_usuario(empleados.empleados)
            if user != None:
                if isinstance(user, Recepcionista):
                    mostrar_pasajeros()
                    user.num_consultas += 1
                    escribirInfo(msjConsulta3)
                else:
                    escribirError(msjPermisos, errUserNull)
                    print("Usuario invalido")
            else:
                escribirError(msjPermisos, errUserPermisos)
                print("El usuario no existe")

        elif opcion == 4:
            user = comprobar_usuario(empleados.empleados)
            if user != None:
                if isinstance(user, Administrador):
                    actualizar_muertos(5)
                    user.num_actualizaciones += 1

                    actualizar_muertos(7)
                    user.num_actualizaciones += 1
                    escribirInfo(msjUpdate)
                else:
                    escribirError(msjPermisos, errUserNull)
                    print("Usuario invalido")
            else:
                escribirError(msjPermisos, errUserPermisos)
                print("El usuario no existe")

        elif opcion == 5: break
        else:
            print("Opcion no valida")

def comprobar_usuario(empleados):
    nick = input("Introduce el usuario: ")
    for emp in empleados:
        if emp.nick == nick:
            return emp
    print(f"No existe ningun soldado con el nombre {nick}")
    return None

def mostrar_vuelos():
    usuarios_activos()
    while True:
        try:
            id = int(input("Introduce el id del pasajero: "))
            break
        except ValueError:
            escribirError(msjConsulta1, errDato)
            print("Introduce un numero entero")
    result, column_names = db_connection.execute_query(QUERY_VUELOS_BY_PASAJERO, {'id_pasajero': id})
    if result:
        df = pd.DataFrame(result, columns=column_names)
        print(df)

def mostrar_direccion():
    usuarios_activos()
    while True:
        try:
            id = int(input("Introduce el id del pasajero: "))
            break
        except ValueError:
            escribirError(msjConsulta2, errDato)
            print("Introduce un numero entero")
    result, column_names = db_connection.execute_query(QUERY_DIRECCION_BY_PASAJERO, {'id_pasajero': id})
    if result:
        print(f"Calle: {result[0][0]} - CP: {result[0][1]}")


def mostrar_pasajeros():
    todos_los_vuelos()
    while True:
        try:
            id = int(input("Introduce el id del vuelo: "))
            break
        except ValueError:
            escribirError(msjConsulta3, errDato)
            print("Introduce un numero entero")
    result, column_names = db_connection.execute_query(QUERY_PASAJEROS_BY_VUELO, {'id_vuelo': id})
    if result:
        df = pd.DataFrame(result, columns=column_names)
        print(df)
        menu_opcion3(df)

def actualizar_muertos(vuelo):
    result, column_names = db_connection.execute_query(QUERY_UPDATE_PASAJEROS, {'id_vuelo': vuelo})
    if result:
        for cliente in result:
            db_connection.execute_query(UPDATE_PASAJEROS_MUERTOS, {'id_cliente': cliente[0]})
        db_connection.execute_query(UPDATE_VUELO, {'id_vuelo': vuelo})
    print("Pasajeros y vuelos modificados")





def todos_los_vuelos():
    result, column_names = db_connection.execute_query(QUERY_VUELOS)
    if result:
        df = pd.DataFrame(result, columns=column_names)
        print(df)

def usuarios_activos():
    result, column_names = db_connection.execute_query(QUERY_CLIENTES_ACTIVOS)
    if result:
        df = pd.DataFrame(result, columns=column_names)
        print(df)

def menu_opcion3(df):
    while True:
        print("\n--- MENÚ ---")
        print("1. Usuario que más ha pagado")
        print("2. Usuario que menos ha pagado")
        print("3. Media del precio de los billetes")
        print("4. Salir")
        while True:
            try:
                opcion = int(input("Opcion elegida: "))
                break
            except ValueError:
                escribirError(msjConsulta3, "TIPO DE DATO INTRODUCIDO INCORRECTO")
                print("Opcion no valida")
        if opcion == 1:
            print(df[df['Precio_billete']==df.Precio_billete.max()])
        elif opcion == 2:
            print(df[df['Precio_billete']==df.Precio_billete.min()])
        elif opcion == 3:
            print(f"Media de precios del billete: {df.Precio_billete.mean()}")
        elif opcion == 4: break
        else:
            print("Opcion no valida")



if __name__ == "__main__":
    db_connection = PostgreSQLConnection()
    db_connection.connect()

    menu()

    db_connection.disconnect()
