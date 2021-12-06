# _*_ coding: utf-8 _*_
import subprocess
from colorama import Fore,init
from prettytable import PrettyTable

'''se obtiene toda la informacion soltada por el comando correspondiente de CMD '''
def obtenerPerfiles():
    perfiles =  subprocess.run("netsh wlan show profiles",stdout=subprocess.PIPE,shell=True,universal_newlines=True)
    return perfiles.stdout.splitlines()

'''se verifica si hay por lo menos un perfil'''
def verificarPerfiles(listaPerfiles):
    cont = 0
    for x in listaPerfiles:
        if x == "    <Ninguno>":
            cont += 1    
    if cont <= 1:
        return True
    return False 

'''obtencion de los nombres de red guardados'''
def obtenerSSID(perfiles):
    puntero = ""
    lista_de_perfiles = []
    final = 9
    indice_guia = len(perfiles) - 10
    final += indice_guia 
    for x in range(9,final):
        puntero = perfiles[x]
        lista_de_perfiles.append(puntero[39:])
    return lista_de_perfiles

'''se obtienen los passwords de redes guardadas'''
def obtenerPassword(lista_de_perfiles):
    lista_de_contraseñas = []
    puntero = ""
    indice_guia = len(lista_de_perfiles)
    for x in range(indice_guia):
        password = subprocess.run("netsh wlan show profile name=\"" + str(lista_de_perfiles[x]) + "\" key=clear",stdout=subprocess.PIPE,shell=True,universal_newlines=True)
        aux = password.stdout.splitlines()
        puntero = aux[32]     
        lista_de_contraseñas.append(puntero[29:])
    return lista_de_contraseñas

'''muestra la informacion obtenida'''
def crearTabla(listaP,listaC):
    table = PrettyTable(["SSID","PASSWORD"])
    for ssid, password in zip(listaP,listaC):
        if password != "":
            table.add_row([ssid,password])
    return table 

    
def main():
    perfiles = obtenerPerfiles()
    if verificarPerfiles(perfiles):
        lista_de_perfiles = obtenerSSID(perfiles)
        lista_de_contraseñas = obtenerPassword(lista_de_perfiles)
        tabla = crearTabla(lista_de_perfiles,lista_de_contraseñas)
        print(tabla)
    else:
        print()
        print(Fore.LIGHTRED_EX + "*"*10 + Fore.RED + " No hay perfiles guardados anteriormente " + Fore.LIGHTRED_EX + "*"*10)
        print()
    
if __name__ == '__main__':
    main()
    



