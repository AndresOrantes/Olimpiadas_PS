#Importa la librería a utilizar

import matplotlib.pyplot as plt
import pandas as pd
import statistics
from colorama import Fore, Back, Style
import numpy as np
diccionario=pd.read_excel("noc_regions.xlsx")#se lee el excel de diccionario
medalpais=pd.read_excel("Country_Medals.xlsx")#Lee el archivo con los registros de ganadores de los juegos olímpicos

#Menú
def menu():
    print(Style.NORMAL+Fore.WHITE+Back.CYAN+'====================MENU==================')#Sale el menú con algunos diseños
    print(Fore.RESET+Back.RESET+'1. Países con más Medallas...')#Opciones para el menú(del 1 al 3 muestran gráficas y tablas)
    print('2. Comparación medallas per cápita de...')
    print('3. Participaciones de...')
    print('4. Otras funciones')#Funciones que regresan datos que no incluyen tablas ni gráficas
    print('5. Terminar')

#En esta función se mostrará el top de 5 de países con más medallas de oro, plata y
#bronce. 
def maxmedpais():
    while True:
        print('Aquí se te mostrará el top 5 de países con más medallas de oro, plata y bronce')
        print('¿Qué quieres hacer?')
        print('1. Un año en específico') 
        print('2. En general')
        print('3. Volver al menú')
        maxmedop=input('Escoge una opción: ')
        if maxmedop=='1':
            try:
                opmmpai=int(input('Introduce el año: ')) 
                opmmpas=str(opmmpai) #crea otra variable con lo mismo pero como string
                topunao=medalpais.groupby('Year').get_group(opmmpai) #Crea una tabla solo con el año que se proporcionó
                topunaoh=topunao.head(5) #Se ponen en una variable los 5 valores de más arriba de esa tabla
                print(topunaoh) #Imprime la tabla
                eje_x = topunaoh['Country_Name'] #Se crea el eje x con la columna 'Country_Name' 
                eje_y = topunaoh['Total'] #Se crea el eje y con la columna 'Total'
                plt.bar(eje_x, eje_y) # Se pone que sea una gráfica de barras con los ejes que se pusieron anteriormente
                plt.ylabel('Total de medallas') #Se escoge el nombre del eje y
                plt.xlabel('Países')#Se escoge el nombre del eje x
                titulotop=('Top 5 países con más medallas en el año '+ opmmpas) #Se crea el título de la gráfica
                plt.title(titulotop) #Se selecciona el título
                plt.show() #Se muestra la gráfica
            except ValueError:
                print('Introduzca un año en el que hayan sucedido los juegos olímpicos')
            except KeyError:
                print('Introduzca un año en el que hayan sucedido los juegos olímpicos')                
        elif maxmedop=='2': 
            medallassuma=medalpais.groupby("Country_Name")[['Total']].sum() #Se suman los valores de la columna total agrupando los datos con el mismo nombre en la columna "Country_Name"
            medallassuma=medallassuma.reset_index()#A la tabla anterior se le resetean los índices para que se muestren, ya que de otra forma se desconfigura
            topmedallasagrup=medallassuma.sort_values('Total', ascending=False) #Se hace que la tabla se ordene con los valores más altos hasta arriba
            topmedallasagrup=topmedallasagrup.head(5) #Se crea una tabla solo con los 5 valores de hasta arriba
            print(topmedallasagrup) #imprime la tabla
            eje_y = topmedallasagrup['Total']#Se crea el eje y con la columna 'Total'
            eje_x = topmedallasagrup["Country_Name"]#Se crea el eje x con la columna 'Country_Name' 
            plt.bar(eje_x, eje_y)#Se selecciona el tipo de gráfica de barras, con los ejes de arriba
            plt.ylabel('Total de medallas')#Se escoge el nombre del eje y
            plt.xlabel('Países')#Se escoge el nombre de x
            plt.title('Top 5 países con más medallas en la historia')#Se selecciona el título
            plt.show()#Muestra la tabla
        elif maxmedop=='3':
            print('Se te redirigirá al menú principal...')#Imprime un texto antes de mandarte al menú principal
            break
        else:
            print('Ingresa una opción válida')

#Esta función hace el recuento de medallas totales que tiene un país(escogido por el usuario)
#y divide el total de medallas entre el número de habitantes a la fecha del 2020
#Para obtener las medallas per cápita y compararlos con otras medallas per cápita
def medpercap():
    while True:
        try: #Hace lo de abajo si no se presenta un tipo de error especificado
            compmedpercap=int(input('¿Cuántos países quieres comparar? '))
            if compmedpercap>0:
                contador=0
                tablapercap=pd.DataFrame() #Se crea un dataframe
                tablapercap['País'] = None #Se crea la primera columna del dataframe
                tablapercap['Medallas per Cápita']= None #Se crea la segunda columna del dataframe
                while compmedpercap!=contador:# mientras el contador no sea igual a la variable compmedpercap
                    medpercappais=input('Ingresa el país del que quieres saber las medallas per cápita: ')#variable con el nombre de algún país a incluir en la comparación
                    medpercappais=medpercappais.title() #Se pone que las primeras letras se pongan en mayúsculas
                    if medpercappais in diccionario.values: #Verifica que el nombre este en la base de datos
                        medparasum=medalpais.groupby('Country_Name').get_group(medpercappais)# Obtiene la tabla con los nombres del país
                        medasuma=(medparasum['Total']).sum() #Suma la columna de total de la tabla que se creó anteriormente y el número se almacena en una variable
                        print('La cantidad total de medallas que ha obtenido ',medpercappais,' en sus participaciones en los Juegos Olímpicos es de ',medasuma)
                        pobparasum=diccionario.groupby('region').get_group(medpercappais) #encuentra la población del país en la base de datos de diccionario
                        pobparasumint=(pobparasum['Población 2020'].values[0])#Transforma el dato en un integer
                        print('La población de ', medpercappais ,' es de ', pobparasumint, 'al año 2020')
                        medpercapita=medasuma/pobparasumint#Calcula las medallas per cápita dividiendo las medallas entre la población del país
                        print('La cantidad de medallas per cápita del país al año 2020 es de ', medpercapita)
                        nuevafila = pd.Series([medpercappais, medpercapita], index=tablapercap.columns) # se crean series
                        tablapercap = tablapercap.append(nuevafila, ignore_index=True) #Las series se agregan al datafram
                        contador+=1                    #El contador aumenta en 1
                    else:
                        print('Ingresa el nombre correcto la próxima vez')
                print(tablapercap)
                eje_y = tablapercap['Medallas per Cápita'] #Se crea el eje y de la gráfica
                eje_x = tablapercap["País"]#Se crea el eje x de la gráfica
                plt.bar(eje_x, eje_y) #Se crea el tipo de gráfica
                plt.ylabel('Medallas per Cápita')#Se crea la etiqueta del eje y
                plt.xlabel('Países') #Se crea la etiqueta del eje X
                plt.title('Comparación de medallas per cápita entre países') #Se crea el título
                plt.show()#Se muestra la gráfica
            else:
                print('No puedes comparar 0 países')
        except ValueError:#Cuando hay un ValueError se imprime lo de abajo
            print('Favor de ingresar un número entero')
        opregmen=input('¿Deseas regresar al menú principal?(Y/N)') #Una vez hecha la comparación te pregunta si quieres regresar al menú principal
        uopregmen=opregmen.upper()
        if uopregmen=='Y': #Si pones Y regresa
            break
        elif uopregmen=='N': #Si pones N puedes seguir
            continue
        else: 
            print('Seleccione una opción válida')
            
    
def part():
    while True:
        partpais=input('Ingresa el nombre del país(en inglés): ') #Se crea una nueva variable
        partpais=partpais.title() #Se pone con mayúsculas la primera letra de las palabras que se pusieron
        cuenpart=0 #contador
        if partpais in diccionario.values:#Se busca en el diccionario el nombre del país
            tablaparticipaciones=medalpais.groupby('Country_Name').get_group(partpais)#Se crea una tabla con solo ese país
            print(tablaparticipaciones.drop(columns=['Country_Code','Host_city']))#Se imprime la tabla sin las columnass 'Country_Code' y 'Host_City'
            print(partpais,' ha ganado medallas en ',len(tablaparticipaciones.index),'  Juegos Olímpicos')
            eje_y = tablaparticipaciones['Total'] #Se crea un eje y con la columna total
            eje_x = tablaparticipaciones["Year"] #Se crea un eje x con la columna "year"
            plt.plot(eje_x, eje_y) #Se crea la gráfica de dispersión con puntos conectados
            plt.ylabel('Medallas')#Etiqueta en el eje y
            plt.xlabel('Año')#etiqueta en el eje x
            titulopart=('Medallas por año de ' + partpais)#Se crea el título de la gráfica
            plt.title(titulopart)#Se selecciona el título para la gráfica
            plt.show()#Se muestra la gráfica
            eje_yy = tablaparticipaciones['Gold']#Se escogen los datos que se usarán en el eje y se usa la columna'Gold'
            eje_yyy=tablaparticipaciones['Silver']#Se escogen los datos que se usarán en el eje y se usa la columna'Silver'
            eje_yyyy=tablaparticipaciones['Bronze']#Se escogen los datos que se usarán en el eje y se usa la columna'Bronze'
            eje_xx = tablaparticipaciones["Year"] #Se escogen los datos que se usarán en el eje x se usa la columna "Year"
            plt.plot(eje_xx,eje_yy,color='gold',linestyle='-', label='Oro') #Se crea la gráfica con colores, estilo de línea y etiquetas para la leyenda
            plt.plot(eje_xx,eje_yyy,color='silver',linestyle='--', label='Plata')#Se crea la gráfica con colores, estilo de línea y etiquetas para la leyenda
            plt.plot(eje_xx,eje_yyyy,color='darkgoldenrod',linestyle='-', label='Bronce') #Se crea la gráfica con colores, estilo de línea y etiquetas para la leyenda
            plt.ylabel('Medallas') #Se crea la etiqueta para el eje y
            plt.xlabel('Año')#Se crea la etiqueta para el eje x
            plt.legend() #Se pone que se muestre la leyenda
            titulopart=('Medallas por año de ' + partpais)#Se crea el título
            plt.title(titulopart)#Se selecciona el título
            plt.show()#Muestra la gráfica
        else: #Si no está el nombre en el diccionario pasa esto
            print('Ingresa el nombre correcto la próxima vez')
        opreg=input('¿Deseas regresar al menú principal?(Y/N)') #Pregunta si quieres volver l menú principal
        uopreg=opreg.upper()#Pone la variable con mayúsculas al principio de la palabra
        if uopreg=='Y':#vuelve al menú
            break
        elif uopreg=='N':#Se repite el ciclo
            continue
        else: 
            print('Seleccione una opción válida')
#submenú para opciones que retornan valores
def submenu():
    print('1.Medallas de un país y su porcentaje')
    print('2.Próximos... Juegos Olímpicos')
    print('3.¿Cuántas veces ha sido anfitrión de los Juegos Olímpicos...?')
    print('4.Volver al menú principal')
#función para calcular años que faltan para los juegos olímpicos
def medallas(pais):
    tabladepais=medalpais.groupby('Country_Name').get_group(pais)#Crea una tabla con todas las veces que se repite el país
    numeromedallas=tabladepais['Total'].sum()#Suma la columna "total" de la tabla
    return numeromedallas #regresa la suma de la línea de arriba

def porcentaje(pais):
    numeromedallastotal=medalpais['Total'].sum()#Suma todos los valores de la columna "total"
    tabladepais=medalpais.groupby('Country_Name').get_group(pais) #Crea una tabla con todas las veces que se repite el país
    numeromedallas=tabladepais['Total'].sum() #Suma la columna "total" de la tabla
    porcentaje=(numeromedallas/numeromedallastotal)*100 #Divide las medallas del país entre todas las medallas otorgadas y lo multiplica por cien para obtener el porcentaje
    return porcentaje #Retorna el porcentaje que se obtuvo

def proximas(veces):
    suma=0 #Crea un contador
    count=0 #Crea un acumulador
    for suma in range(veces): #Suma pasa la cantidad de veces necesarias en "veces"
        count+=1 #aumenta uno cada que pasa suma
        print('Los próximos Juegos olímpicos son en ', 2020+(count*4)) #Se imprimer ese texto y se pone también el año 2020 más el contador por 4
def host(pais):
    contador=0
    tabladepais=medalpais.groupby('Country_Name').get_group('United States')#Usamos esto, ya que Estados Unidos ha estado en todos los Juegos olímpicos que han sido celebrados hasta la fecha
    tabladehost=tabladepais.groupby('Host_country').get_group(pais)
    for pais in tabladehost['Host_country']:
        contador+=1
    return contador


def main():
    print('Bienvenido en este programa podrás revisar tablas, estadísticas y gráficas')
    print('de los Juegos Olímpicos. Los datos de los Juegos Olímpicos que se tienen')
    print('son desde Atenas 1896 hasta Tokyo 2020.')
    print('Se recomienda buscar los nombres de los países en la siguiente liga: ')
    print('https://en.wikipedia.org/wiki/National_Olympic_Committee')
    while True:
        menu()
        opcion=input('Selecciona una opción: ')
        if opcion=='1':
            print('====================================================================================')
            print('************************************************************************************')
            print('====================================================================================')
            maxmedpais() #Llama la función

        elif opcion=='2':
            print('====================================================================================')
            print('************************************************************************************')
            print('====================================================================================')
            print('Aquí podrás ver la comparación de las medallas que tiene un país por habitante.')
            medpercap()#Llama la función

        elif opcion=='3':
            print('====================================================================================')
            print('************************************************************************************')
            print('====================================================================================')
            print('Aquí podrás ver las participaciones del país que elijas, toma en cuenta que')
            print('Es posible que no aparezcan todas debido a posibles cambios de nombre')
            part()#Llama la función
        elif opcion=='4':
            print('====================================================================================')
            print('************************************************************************************')
            print('====================================================================================')
            print('Aquí podrás ver opciones diferentes que no incluyen gráficas ni tablas como las del menú')
            submenu()#Llama la función
            opcionsub=input('Escoge una opción: ')
            if opcionsub=='1':
                print('===============================================================================')
                paispmed=input('Introduzca el país: ')
                paispmed=paispmed.title() #Pone mayúsculas al inicio de las palabras en la variable
                if paispmed in diccionario.values: #Busca el país en el diccionario
                    print(paispmed, ' tiene un total de ', medallas(paispmed), ' medallas.') #Llama la función y le da datos e imprime lo que retorna
                    openpaispmed=input('¿Deseas conocer el porcentaje de que representa este número?(Y/N)')
                    if openpaispmed.upper()=='Y':
                        print('Y tiene el ', round(porcentaje(paispmed),5), '% de todas las medallas que han sido otorgadas en los Juegos Olímpicos desde 1896')#Llama la función y le da datos e imprime lo que retorna
                    elif openpaispmed.upper()=='N':
                        print('De acuerdo, regresando al menú...')
                    else:
                        print('Selecciona una opción válida')
                else:
                    print('Introduzca un nombre correcto')    
            elif opcionsub=='2':
                print('===============================================================================')
                print('Aquí sabrás los años del número de siguientes olimpiadas que quieras')
                try:
                    cuantas=int(input('¿Los años de cuántas olimpiadas quieres saber? '))
                    proximas(cuantas)#Llama la función y le da datos e imprime lo que retorna
                except ValueError:
                    print('Ingresa un número válido')
            elif opcionsub=='3':
                print('===============================================================================')
                print('Aquí sabrás cuantas veces un país ha tenido a los Juegos Olímpicos')
                try:
                    pais=input('Escoge el país:')
                    pais=pais.title()
                    print(pais,' ha hospedado los Juegos Olímpicos ',host(pais), ' veces')#Llama la función y le da datos e imprime lo que retorna
                except ValueError:
                    print('Ingresa un pais válido')
                except KeyError:
                    print('Ingresa un país')
            elif opcionsub=='4':
                print('De regreso al menú principal...')

        elif opcion=='5':
            break
        else:
            print('Escoge una opción válida')
main()
