import json
import pandas as pd

class PruebaSubsistema:
    def __init__(self,estado_inicio,mechanismo,alcance):
        self.ESTADO_INICIO = estado_inicio
        self.CONDICIONES = len(estado_inicio)*'1'
        self.mechanismo = mechanismo
        self.alcance = alcance

    def __str__(self):
        return f"Estado Inicial: {self.ESTADO_INICIO}, Condiciones: {self.CONDICIONES}, Mecanismo: {self.mechanismo}, Alcance: {self.alcance}"
        


class FormatExcel:
    def __init__(self, url,sistema_candidato):
        self.url = url  # Ruta del archivo Excel
        self.lista_valores_sin_formato = []
        self.lista_valores_con_formato = []
        self.sistema_candidato = sistema_candidato
        self.ConstruirLista()
        self.FormatoLista()


    def ConstruirLista(self):
        HojaSeleccionada = 0
        # Cargar el archivo Excel
        df = pd.read_excel(self.url,sheet_name=HojaSeleccionada, engine="openpyxl", header=None)
        # Seleccionar la columna B y extraer los valores desde B5 hasta B103, saltando de 2 en 2
        excel = pd.ExcelFile(self.url)  
 
        self.lista_valores_sin_formato = df.iloc[4:103:2, 2].dropna().tolist()

    def FormatoLista(self):
        for i in self.lista_valores_sin_formato:
            part1 = i.split("|")[0].split('_')[0].strip()
            part2 = i.split("|")[1].split('_')[0].strip()
            self.lista_valores_con_formato.append([self.__FormatoEntero__(part1), self.__FormatoEntero__(part2)])
    
    def __FormatoEntero__(self, valor):
        valor_entero = ''
        for i in self.sistema_candidato:
            if i in valor:
                valor_entero += '1'
            else: 
                valor_entero += '0'
        return valor_entero
    
    
    def CargarValores(self, lista, fila):
        # Cargar el archivo Excel
        df = pd.read_excel(self.url, engine="openpyxl", header=None)
        # Insertar los valores en la columna B desde la fila inicio hasta la fila fin
        df.at[fila, 6] = lista[0]
        df.at[fila, 7] = lista[1]
        df.at[fila, 8] = lista[2]
        # Guardar el archivo Excel
        df.to_excel(self.url, index=False, header=False, engine="openpyxl")
   


class ControladorSubsistema:
    def __init__(self, URL, sistema_candidato,estado_inicio):
        self.formateo= FormatExcel(URL, sistema_candidato)
        self.listaObjetos = []
        self.CrearListaObjetos(estado_inicio)
        self.ObjectToJson()

    def CrearListaObjetos(self,estado_inicio):
        for i in self.formateo.lista_valores_con_formato:
            self.listaObjetos.append(PruebaSubsistema(estado_inicio,i[1], i[0]))


    def ObjectToJson(self, filename="ahiTiene.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([obj.__dict__ for obj in self.listaObjetos], file, indent=4) 

    def __str__(self):
        for i in self.listaObjetos:
            print(i.__str__())




# Uso de la clase
URL = "/home/liceth/Descargas/PruebasIniciales20 (1).xlsx"  # Cambia esto ypor la ruta de tu archivo
my_excel = ControladorSubsistema(URL, 'ABCDEFGHIJ','1000000000')
#my_excel.ObjectToJson()
#print(my_excel)



