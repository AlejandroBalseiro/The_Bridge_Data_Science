#########################
# Juego de hundir la flota hecho por Alejandro Balseiro
# Ejercicio para The Bridge terminado el día 30 Nov 2020 en su v1
#########################

#########################
# Importaciones
#########################
import json
import random

#########################
# Definición de funciones
#########################

def primer_jugador(jugadores):
    #Hacemos el soreto de jugador inicial

    jug1 = random.choice(jugadores)

    if jugadores.index(jug1) == 0:
        jug2 = jugadores[1]
    else:
        jug2 = jugadores[0]

    players = [jug1,jug2]
    print("Player 1:\t", players[0],"\nPlayer 2:\t", players[1])

    return players
    

def player (ply,nombre = "partida 1",turno = 1): 
    # Metemos el jugador adecuado en el dicc, pasandole un list con los nombres, creamos el archivo de los jugadores
    # ply una lista con los nombres de jugador, "nombre" es el nombre de la partida y "turno" es el turno actual
    # "ply1_ply1":["tablero player 1 para player 1"]
    # "ply1_ply2":["tablero player 1 para player 2"]
    # "ply2_ply2":["table play2 for ply2"]
    # "ply2_ply1":["play 2 tabl for play1"]
    # "ply1_exitos:" Número de exitos de jugador 1
    # "ply2_exitos:" Número de exitos de jugador 2
    
    tablero = tablero_blanco()


    partida ={"ply1":"","ply2":"","turno":0,"ply1_ply1":tablero,"ply1_ply2":tablero,"ply2_ply2":tablero,"ply2_ply1":tablero,"ply1_exitos":0,"ply2_exitos":0}
    partida["ply1"] = ply[0]
    partida["ply2"] = ply[1]
    partida["turno"] = turno

    saver(partida,nombre)
    
    return partida

def load (archivo):
    # Función para llamar al archivo "archivo" .json y poder trabajar con él posteriormente

    archivo = archivo + ".json"
    with open (archivo) as json_file:
        archivo = json.load(json_file)
    
    return archivo

def saver (data,archivo):
    # Función para guardar lo trabajado  y almacenado en un diccionario "data" en el archivo "archivo" .json

    nombre_partida = archivo + ".json"

    with open(nombre_partida,'w') as json_file:
        json.dump(data,json_file)

    

def conversor_tablero (tab): 
    # Hacemos una visualización sencilla del tablero "tab" por terminal

    linea = ["    1 2 3 4 5 6 7 8 9 10"]
    for x in range(10):
        aux = ""
        for y in range(len(tab)):
            aux = aux + tab[x][y]
        if x < 9:
            linea.append(str(x+1)+"  "+aux)
        else:
            linea.append(str(x+1)+" "+aux)    

    
    for x in range(11):
        print(linea[x])  


def tablero_inicial (ply,archivo):
    # Generamos el tablero inicial para el jugador "ply" y lo guardamos en el "archivo"

    tablero = tablero_blanco()

    conversor_tablero(tablero)

    lista = ["2x1a","2x1b","2x1c","2x1d","3x1a","3x1b","3x1c","4x1a","4x1b","5x1"]
    archivo_juego = load(archivo) 

    PlyId = ply[0:4]
    
    x = 0
    while x <= 9: #Guardamos las coordendas de los barcos
        pos = input("{plyer} introduzca donde quiere poner el barco {bar}".format(plyer = archivo_juego[PlyId],bar = lista[x]))
        checker_1 = check_medida(pos,lista[x])
        if checker_1 != False:
            checker_2 = check_flota(pos,tablero)

        if checker_1 != False and checker_2 != False:
            tablero = checker_2
            conversor_tablero(tablero)
            x += 1
        else:
            print("No permitido, vuelva a introducir la posición")
  
     
    archivo_juego[ply] = tablero
    
    saver(archivo_juego,archivo)

    return archivo_juego

def check_medida (pos,lista): 
    # Comprobamos la longitud del barco introducido

    pos = pos.lower()
    try:
        if pos[1] == "h" or pos[2] == "h":
            direc = pos.split("h")
            dim = direc[1].split(":")
        else:
            direc = pos.split("v")
            dim = direc[1].split(":")

        if abs(int(dim[1])-int(dim[0])+1) != int(lista[0]):
            return False
    except:
        return False

def check_flota(barco,tablero): 
    # Sirve para definir el tablero y chequear que no hay posiciones asignadas ya

    try:
        bar = barco.lower()
        if bar[1] == "h" or bar[2] == "h":  #Hay que tener en cuenta que 10 tiene 2 digitos
            direc = bar.split("h")
            dim = direc[1].split(":")
            
            if int(dim[0]) < 1 or int(dim[0]) > 10 or int(dim[1]) < 0 or int(dim[1]) > 10:
                print ("\nFuera de rango\n")
                return False

            fil= int(direc[0])-1
            
            if dim[0] < dim [1]:
                cc = int(dim[0])-1
                ccfin = int(dim[1])-1
            else:
                ccfin = int(dim[0])-1
                cc = int(dim[1])-1

            print("\nBarco:",barco[0],"dirección: Horizontal\nFila:",fil+1,"Posición inicial:",cc+1,"posición final:",ccfin+1)

            while cc <= ccfin: #comprobamos
                if tablero[fil][cc] == " *":      
                    print("\n\tPosición ya ocupada en fila",fil+1,"y columna:",cc+1) 
                    return False
                cc += 1   

            if dim[0] < dim [1]:
                cc = int(dim[0])-1
                ccfin = int(dim[1])-1
            else:
                ccfin = int(dim[0])-1
                cc = int(dim[1])-1

            while cc <= ccfin: #guardamos     
                tablero[fil][cc] = " *"            
                cc += 1                                                                                                                                                                                                                                
            
        elif bar[1] == "v" or bar[2] == "v":  #Hay que tener en cuenta que 10 tiene 2 digitos  
            direc = bar.split("v")
            dim = direc[1].split(":")

            if int(dim[0]) < 1 or int(dim[0]) > 10 or int(dim[1]) < 0 or int(dim[1]) > 10:
                print ("\nFuera de rango\n")
                return False
            
            colum = int(direc[0])-1
            
            if dim[0] < dim [1]:
                ff = int(dim[0])-1
                filfin = int(dim[1])-1
                
            else:
                filfin = int(dim[0])-1
                ff = int(dim[1])-1
            
            print("\nBarco:",barco[0],"dirección: Vertical\nColumna:",colum+1,"Posición inicial:",ff+1,"posición final:",filfin+1)

            while ff <= filfin: #Comprobamos
                if tablero[ff][colum] == " *":      
                    print("\n\tPosición ya ocupada en fila",ff+1,"y columna:",colum+1)
                    return False            
                ff += 1  
            
            if dim[0] < dim [1]:
                ff = int(dim[0])-1
                filfin = int(dim[1])-1
                
            else:
                filfin = int(dim[0])-1
                ff = int(dim[1])-1
            
            while ff <= filfin:
                tablero[ff][colum] = " *"                
                ff += 1                        
                        
        else:
            print("\tdirección no permitida")
            return False
        
        return tablero

    except:
        return False

def check_jugada(tablero,tablero_contrincante,jugada): 
    #Chequeador de jugadas
    #tablero: Tablero que visualiza el actual jugador
    #tablero_contrincante: Tablero oculto del jugador que es atacado
    #jugada: string con la jugada
    try:
        jugada.lower()
        coordenadas = jugada.split("x")
        x = int(coordenadas[0])-1
        y = int(coordenadas[1])-1

        if tablero_contrincante[x][y] == " ~":
            print ("\nAGUA!\n")
            tablero[x][y] = " o"
            return False
        else:
            print ("\nTOCADO!\n")
            tablero[x][y] = " X"
            return True
    except:
        print("Jugada mal introducida, repita por favor")
        return 1

def tablero_blanco():
    # Tablero en blanco
    tablero = [[' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~'], [' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~', ' ~']]
    return tablero


#########################
# Código
#########################

jugadores = []
archivo_partida = {}
Lista = ["ply1","ply2","turno","ply1_ply1","ply1_ply1","ply2_ply2","ply2_ply1","ply1_exitos","ply2_exitos"]

continuar = input("¿Quiere continuar alguna partida guardada? (si/no)")
continuar = continuar.lower()


if continuar == "si":    
    juego = input("introduzca el nombre de la partida que desea cargar")
    archivo_partida = load(juego)
    print("\nPlayer 1:\t",archivo_partida["ply1"],"\nPlayer 2:\t",archivo_partida["ply2"],"\nTurno actual:\t",archivo_partida["turno"])
else:
    for x in range(2):
        ply = input("Introduzca su nombre jugador")
        ply = ply.replace(" ","_")
        jugadores.append(ply)
    
    print("Sorteo de jugador inicial\n-------------\nOrden de jugadores:")

    jugadores = primer_jugador(jugadores)
    print("------------")

    juego = input("introduzca el nombre de la partida")
    juego = juego.replace(" ","_")
    # generamos el archivo donde vamos a ir guardando la partida 
    archivo_partida = player(jugadores,juego)
    tablero_inicial ("ply1_ply1",juego)
    tablero_inicial ("ply2_ply2",juego)


archivo_partida = load(juego)
it = archivo_partida["turno"]
while True:
    if it%2 != 0:
        print("\n----------------- JUGADA {} -------------------".format(it))
        print("Juega:\t",archivo_partida["ply1"])
        print ("\nTU TABLERO\n")
        conversor_tablero(archivo_partida["ply1_ply1"])
        print ("\nTABLERO CONTRINCANTE\n")
        conversor_tablero(archivo_partida["ply2_ply1"])

        jugada = input("Donde quieres atacar? (escribe 'Exit' para terminar)")
        

        if jugada.lower() != "exit":
            exito = check_jugada(archivo_partida["ply2_ply1"],archivo_partida["ply2_ply2"],jugada)
            conversor_tablero(archivo_partida["ply2_ply1"])
            if exito == True:
                archivo_partida["ply1_exitos"] += 1
                if archivo_partida["ply1_exitos"] == 30:
                    print("\n #########################################\n ¡{jug} HAS GANADO A {jug2} EN {ite} MOVIMIENTOS!\n #########################################".format(jug = archivo_partida["ply1"].upper(),jug2 = archivo_partida["ply2"].upper(), ite = int(it/2)))
                    archivo_partida["turno"] = it
                    saver(archivo_partida,juego)
                    break

            elif exito == 1:
                print("-----------------------")
            
            it += 1
            archivo_partida["turno"] = it
            saver(archivo_partida,juego)
        else:
            break
    else:
        print("\n----------------- JUGADA {} -------------------".format(it))
        print("Juega:\t",archivo_partida["ply2"])
        print ("\nTU TABLERO\n")
        conversor_tablero(archivo_partida["ply2_ply2"])
        print ("\nTABLERO CONTRINCANTE\n")
        conversor_tablero(archivo_partida["ply1_ply2"])

        jugada = input("Donde quieres atacar? (escribe 'Exit' para terminar)")

        if jugada.lower() != "exit":
            exito = check_jugada(archivo_partida["ply1_ply2"],archivo_partida["ply1_ply1"],jugada)
            conversor_tablero(archivo_partida["ply1_ply2"])
            if exito == True:
                archivo_partida["ply2_exitos"] += 1
                if archivo_partida["ply2_exitos"] == 30:
                    print("\n #########################################\n ¡{jug} HAS GANADO A {jug2} EN {ite} MOVIMIENTOS!\n #########################################".format(jug = archivo_partida["ply2"].upper(),jug2 = archivo_partida["ply1"].upper(), ite = int(it/2)))
                    archivo_partida["turno"] = it
                    saver(archivo_partida,juego)
                    break

            elif exito == 1:
                print("-----------------------")
            
            it += 1
            archivo_partida["turno"] = it
            saver(archivo_partida,juego)
        else:
            break