#InstaStalk 
#Hecho por Pablo Sierra Sanz
#
#Para su instalación se necesita la libreria instabot
#Para instalarla ejecuta el siguiente comando
#
#pip install instabot
#
#Si no funciona el comando, necesita instalar el comando pip en su sistema, ejecute el siguiente comando:
#
#sudo apt install python3-pip
#
#Para usar instastalk necesita una cuenta de instagram, ya que se utiliza la API de instagram
#y esta requiere de iniciar sesión
#
#
#
from instabot import Bot
import getpass

def pedirUsuario():
    salir = False
    while not salir :
        user = input("Introduce el nombre de usuario (obligatorio cuenta pública o privada que sigas): ")

        if user == "":
            continue
        
        id = mi_bot.get_user_id_from_username(user)
        salir = True

    return id


def option1(mi_bot):
    print("Has utilizado la opcion 1")
    
    menu = """¿Quiere obtener todos los comentarios o solo los últimos??

    [1] Todos los comentarios
    [2] Últimos comentarios
    [99] Volver al menú principal

    """
    try:
        opcion = int(input(menu))
    except (ValueError, TypeError):
        print("Debe introducir un número entero, vuelta al menú")

    
    #Comprobación de salida
    if opcion == 99:
        return

    if opcion != 1 and opcion != 2:
        print("Opción incorrecta, vuelta al menú\n")
        return
    
    #Proceso de introducir link
    salir = False
    while not salir :
        link = input("Introduce el link de la publicación: ")

        if link == "":
            continue

        id = mi_bot.get_media_id_from_link(link)
        salir = True

    #Proceso de obtener comentarios
    
    if opcion == 1:
        try:
            comments = mi_bot.get_media_comments_all(id, True)
        except:
            print("El link no es correcto, vuelta al menú")
            return
    else:
        try:
            comments = mi_bot.get_media_comments(id, True)
        except:
            print("El link no es correcto, vuelta al menú")
            return

    print("Se mostrarán: " + str(len(comments)))
    #Mostrar comentarios
    for comment in comments:
        print(comment)

    

def option2(mi_bot):
    print("Has utilizado la opcion 2")

    id = pedirUsuario()
    
    #Proceso de obtener las fotos
    fotos = mi_bot.get_user_medias(id, filtration=False)
    
    for foto in fotos:
        print(mi_bot.get_link_from_media_id(foto))




def option3(mi_bot):
    print("Has utilizado la opcion 3")
    #Se pedirá la cuenta de instagram con sus controles correspondientes
    #Se pedirá también un nombre para el diccionario (por defecto diccionario.txt)

    id = pedirUsuario()

    filename = input("Introduce el nombre que tendrá el diccionario (si está vacío se usará diccionario.txt): ")

    if filename == "":
        filename = "diccionario.txt"

    aditionalwords = []
    print("""Finalmente, introduce palabras que creas que faltan para completar el diccionario
    
    Te dejo aquí una lista con recomendaciones:
    
    -Edad                       -Artista favorito
    -Año de nacimiento          -Ciudad/pueblo donde vive
    -Pelicula favorita          -Ciudad/pueblo donde nació
    -Nombre de mascota          -Libro preferido
    -Serie favorita             -Comida preferida
    -Personaje favorito
    
    Recuerda no poner espacios, es raro que alguien lo ponga en su contraseña""")

    salir = False
    while not salir:
        add = input("Introduce end (en minúsculas) para terminar de poner palabras: ")
        
        if add == "end":
            salir = True
            continue

        if add == "":
            continue

        aditionalwords.append(add)
        

    #Proceso de creación
    info = mi_bot.get_user_info(id)
    phrases = info["biography"]
    phrases = phrases.split("\n")
    words = []
    for phrase in phrases:
        wordsAux = phrase.split(" ")
        words.append(wordsAux)
    
    #La estructura que se genera es una matriz, habiendo en cada fila las palabras que forman una frase
    
    #Filtramos y juntamos en un único array todo
    correctwords = []

    for phrase in words:
            for word in phrase:
                if len(word) > 3:
                    #Eliminamos posibles comas
                    pos = word.find(",")
                    if pos != -1:
                        if pos == 0:
                            word = word[1:]
                        else:
                            word = word[:-1]

                    #Eliminamos posibles parentesis
                    pos = word.find("(")
                    if pos != -1:
                        word = word[1:]

                    pos = word.find(")")
                    if pos != -1:
                        word = word[:-1]

                    correctwords.append(word)

    for word in aditionalwords:
        correctwords.append(word)

    #Escribimos en el fichero
    try:
        diccionario = open(filename, "w")

        #Añadimos las palabras anteriores
        for word in correctwords:
            diccionario.write(word+"\n")
            diccionario.write(word + str(1) + "\n")
            diccionario.write(word + str(12) + "\n")
            diccionario.write(word + str(123) + "\n")

        #Hacemos una mezcla de parejas
        for word1 in correctwords:
            for word2 in correctwords:
                if word1 != word2:
                    word = word1 + word2
                    diccionario.write(word+"\n")


    finally:
        diccionario.close()

    print("\n\nDiccionario creado! Almacenado en la misma ruta del fichero .py con el nombre: " + filename)


def option4(mi_bot):
    print("Has utilizado la opción 4")
    #Para el punto 4 obtener lista de seguidos y de que nos siguen, y de ahí filtrar
    salir = False
    while not salir :
        user = input("Introduce tu nombre de usuario (si introduces el de otro obtendrá los datos de ese usuario): ")

        if user == "":
            continue
        
        id = mi_bot.get_user_id_from_username(user)
        salir = True
    
    seguidos = mi_bot.get_user_following(id)
    nosSiguen = mi_bot.get_user_followers(id)

    malaspersonas = []
    print("Lista de personas que sigues y no te siguen (es un proceso largo, espere un momento)")
    for seguido in seguidos:
        if not seguido in nosSiguen:
            malapersona = mi_bot.get_username_from_user_id(seguido)
            print(malapersona)

def option5(mi_bot):
    print("Has utilizado la opción 5")
    mi_bot.unfollow_non_followers()

def option6(mi_bot):
    print("Has utilizado la opción 6")
    
    id = pedirUsuario()
    
    mi_bot.follow_followers(id)

def option7(mi_bot):
    print("Has utilizado la opción 7")
    
    id = pedirUsuario()

    textoCompleto = []
    salir = False
    while not salir:
        frase = input("""Introduce el texto que quiere enviar (solo un posible mensaje): """)

        if frase == "":
            continue


        salir = True
        textoCompleto.append(frase)

    seguidores = mi_bot.get_user_following(id)
    for mensaje in textoCompleto:
        mi_bot.send_message(mensaje, userid)
    
def option8(mi_bot):
    print("Has utilizado la opción 8")
    id = pedirUsuario()

    salir = False
    while not salir:
        frase = input("""Introduce el texto que quiere comentar (solo un posible comentario): """)

        if frase == "":
            continue

        salir = True
        
    
    seguidos = mi_bot.get_user_following(id)
    for seguido in seguidos:
        fotos = mi_bot.get_user_medias(seguido, False)
        mi_bot.comment(fotos[0], frase)
        


def help():
    print("Has utilizado la opción 9")
    print(""" InstaStalk 
    Hecho por Pablo Sierra Sanz

    Para su instalación se necesita la libreria instabot
    Para instalarla ejecuta el siguiente comando

    pip install instabot

    Si no funciona el comando, necesita instalar el comando pip en su sistema, ejecute el siguiente comando:

    sudo apt install python3-pip

    Para usar instastalk necesita una cuenta de instagram, ya que se utiliza la API de instagram
    y esta requiere de iniciar sesión
    
    Gracias por descargar y probar esta herramienta :)""")
    

mi_bot = Bot()
print("""Para poder usar instastalk necesita iniciar sesión en instagram, ya que se usa la API de instagram,
la cuál pide una cuenta para poder acceder a los datos

Para saber más sobre el uso de la aplicación le aconsejo acceder al apartado Como usar instastalk
""")



salida = mi_bot.login(username = input("Introduce usuario de instagram: "), password = getpass.getpass("Introduce contraseña: "))

titulo = """
 _           _            _        _ _    
(_)         | |          | |      | | |   
 _ _ __  ___| |_ __ _ ___| |_ __ _| | | __
| | '_ \/ __| __/ _` / __| __/ _` | | |/ /
| | | | \__ \ || (_| \__ \ || (_| | |   < 
|_|_| |_|___/\__\__,_|___/\__\__,_|_|_|\_\ 


by Pablo Sierra Sanz

[1] Obtener comentarios a partir de un link de una publicación
[2] Mostrar links de últimas publicaciones de un usuario
[3] Crear diccionario a partir de biografia de un usuario
[4] Obtener usuarios que sigues y no te siguen
[5] Dejar de seguir a las cuentas que no te siguen (CUIDADO, IRREVERSIBLE)
[6] Seguir a seguidores de una cuenta
[7] Mandar mensajes privados a seguidores de una cuenta (CUIDADO, POSIBLE BANEO)
[8] Comentar en las últimas fotos de las cuentas que sigue una cuenta
[80] Como usar instastalk
[99] exit
"""


userInput = 0
while userInput != 99 :
    print(titulo)
    try:
        userInput = int(input())
    except (TypeError, ValueError):
        print("ERROR Debe introducir números enteros")
        continue

    if userInput == 1 :
        option1(mi_bot)
    elif userInput == 2:
        option2(mi_bot)
    elif userInput == 3:
        option3(mi_bot)
    elif userInput == 4:
        option4(mi_bot)
    elif userInput == 5:
        option5(mi_bot)
    elif userInput == 6:
        option6(mi_bot)
    elif userInput == 7:
        option7(mi_bot)
    elif userInput == 8:
        option8(mi_bot)
    elif userInput == 80:
        help()      
    else:
        
        continue


print("Gracias por usar instastalk ;)")




