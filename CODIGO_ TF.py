import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def columnas():
        lista = np.arange(2004,2024).tolist()
        lista.insert(0, "Contenido")
        return lista

def graficador_lineas_tendencias( dataframes, opcion , ano_A, ano_B, ):
        match opcion:
            case 'S':
                plt.title(f"SALIDAS")
                dataframe = dataframes["salidas_segun_continente"]
            case 'E':
                plt.title(f"ENTRADA")
                dataframe  =  dataframes["entradas_segun_continente"]
        indices = list(range(dataframe.columns.to_list().index(ano_A), dataframe.columns.to_list().index(ano_B)+1))
        filtracion_datos = dataframe.iloc[1:,indices]
        valores_continentes = [ filtracion_datos.where(dataframe["Contenido"]==valor).dropna().iloc[0]/100 for valor in dataframe.iloc[np.arange(1,9).tolist(), 0]]
        leyenda = []
        for indice, valor in enumerate(valores_continentes, start=1):
            plt.plot(np.arange(ano_A, ano_B+1).tolist(),valor)
            leyenda.append(f"{dataframe.iloc[indice, 0]}")
        plt.legend(leyenda)
        plt.ylabel("Cientos de salida")
        plt.xlabel("Año")
        plt.show()
def graficar_barras_continente(dataframes,continente):
        plt.title(f"Continente  {continente}")
        datos = [
            [dataframes["salidas_segun_continente"].where(dataframes["salidas_segun_continente"]["Contenido"]==continente).dropna()[2023] /100,       
             dataframes["entradas_segun_continente"].where(dataframes["entradas_segun_continente"]["Contenido"]==continente).dropna()[2023] /100],
            ["Salidas", "Entradas" ],
            ["#C70039", "#DAF7A6"]
        ]
        for indice in range(len(datos)-1):
           plt.bar(datos[1][indice], datos[0][indice], color=datos[2][indice])
        plt.legend(["Salida", "Entrada"])
        plt.ylabel("Cientos")
        plt.show()
        

def graficar_barras_continente_diago( dataframes, continente):
        plt.title(f"Continente  {continente}")

        #datos = [salidas_segun_continente.where(salidas_segun_continente["Contenido"]=="América").dropna()[2021] , 
                         # entradas_segun_continente.where(entradas_segun_continente["Contenido"]=="América").dropna()[2021]]
        datos = [dataframes["salidas_segun_continente"][2021][dataframes["salidas_segun_continente"]["Contenido"]==continente].to_list()[0]/100, 
                dataframes["entradas_segun_continente"][2021][dataframes["entradas_segun_continente"]["Contenido"]==continente].to_list()[0]/100]
        #plt.barh("Salidas",  salidas_continente[ano], )
        #plt.barh("Entradas",  entradas_continente[ano])
        #plt.barh(np.array(["Salidas","Entradas" ]),  datos)
        #plt.barh(y=["xd","xdd"], width=datos)
        plt.barh(y=["Salidas", "Entradas"], width=datos, color=   ["#C70039", "#DAF7A6"])
        plt.xlabel(f"Cantidad en cientos")
        plt.show()
def validar_continente(dataframes):
        continente =""
        continentes = dataframes["salidas_segun_continente"]["Contenido"].iloc[1:].values.tolist()
        while not (continente in list(range( len(continentes)))):
            for indice, continente_m in enumerate(continentes):
                print(indice, continente_m)
            try:
                continente = int(input("Ingrese opcion continente que quiere ver: ")) 
            except Exception:
                pass
        return continentes[continente]
def reportes(dataframes):
    opcion =  -1
    while not( opcion == 4):
        print("""
        1. Lineas de tendencia salida y entrada
        2. Barra horizontales continente especifico
        3. Barra diagonales continente especifico
            """)
        try:
            opcion = int(input(f"Seleccione alguna opcion: "))
        except Exception:
            pass
        match opcion:
            case 1:
                ano_A= 0
                dataframe_opcion = ''
                ano_B= 0
                while not((ano_A and ano_B in columnas()[1:]) and dataframe_opcion in ['S', 'E']):
                    try:
                        dataframe_opcion, ano_A, ano_B = tuple(input("""
                                                   Seleccione salidas o entradas y los años intervalo en el siguiente formato
                                                   S: SALIDA
                                                   E: ENTRADA
                                                   S|E:20xx:20xx
                                                   """).split(":"))
                        dataframe_opcion = dataframe_opcion.upper()
                        ano_A = int(ano_A)
                        ano_B = int(ano_B)
                    except Exception:
                        pass
                graficador_lineas_tendencias(dataframes, dataframe_opcion, ano_A=ano_A, ano_B=ano_B)
            case 2:
                continente = validar_continente(dataframes)
                graficar_barras_continente(dataframes,  continente)    
            case 3:
                continente = validar_continente(dataframes)
                graficar_barras_continente_diago(dataframes, continente)
            case _:
                  pass
            


def histograma_porcentajes(dataframes):
    continente = validar_continente(dataframes=dataframes)
    indice_continente = dataframes["salidas_segun_continente"][ dataframes["salidas_segun_continente"].loc[:, "Contenido"]== continente].index
    valores = [
        (
            (dataframes["salidas_segun_continente"].iloc[indice_continente, 1:] * 100) /
            dataframes["salidas_segun_continente"].iloc[0, 1:], "Salidas", "skyblue"
        ),
        (
            (dataframes["entradas_segun_continente"].iloc[indice_continente, 1:] * 100) /
            dataframes["entradas_segun_continente"].iloc[0, 1:], "Entradas", "purple"
        )
    ]
    for tupla in valores:
        plt.hist(tupla[0].values.flatten(), label=f"{tupla[1]}", color=tupla[2], edgecolor= "black")
    
    plt.legend()
    plt.title(f"histograma de porcentaje de Salidas y entradas de {continente}")
    plt.show()

def sustentacion(dataframes):
    plt.figure(figsize=(15,9))

    plt.scatter(dataframes["poblacion_estimada"]["Total"].apply(lambda x: int(x.replace('.',''))) /100 , dataframes["salidas_segun_continente"].iloc[0, 1:] /10 )
    plt.ylabel("Salidas en decenas", fontdict={"color": "orange",
                                           "fontsize":22, 
                                           "fontweight": "bold"})
    plt.xlabel("estimacion de poblacion en cientos", fontdict={"color": "green",
                                           "fontsize":22, 
                                           "fontweight": "bold"})

    plt.title(f"No se puede representaer una buena regresion lineal debido a que falta lineabilidad en los datos :v")
    plt.show()
def estadisticas(dataframes):
    opcion = -1
    while not(opcion ==3):
        print(f"""
            1. Fundamentacion de por que la regresion lineal esa no funciona por que si uwuwuwuwuuuwuwwuwu
            2. Histograma de porcentajes de salida y entrada de acuerdo a continente :V
            """)
        try:
             opcion = int(input("Ingrese su seleccion: "))
        except Exception:
             pass
        
        match opcion:
            case 1:
                  sustentacion(dataframes=dataframes)
            case 2:
                  histograma_porcentajes(dataframes=dataframes)

def main():


    migracion_internacional = pd.read_excel("caso9_migracion_internacional_clear.xlsx", sheet_name="hoja1", usecols=np.arange(0,21)).dropna().reset_index(drop=True)
    dataframes = {
        "salidas_segun_continente": migracion_internacional.iloc[1:10,:].set_axis(columnas(), axis="columns").reset_index(drop=True),
        "entradas_segun_continente":migracion_internacional.iloc[12:-1,:].set_axis(columnas(), axis="columns").reset_index(drop=True),
        "poblacion_estimada": pd.read_csv("crecimiento_estimado_inei.csv", sep=";").iloc[np.arange(24,44), :]

    }



    opcion= -1
    while not (opcion == 5):
        print("""
            1. reportes
            2. Estadisticas
            3. Exportar datos
            """)
        try:
            opcion = int(input("Ingrese opcion: "))
        except Exception:
            pass
        match opcion:
            case 1:
                reportes(dataframes=dataframes)
            case 2: 
                estadisticas(dataframes= dataframes)
            case _:
                pass


main()
